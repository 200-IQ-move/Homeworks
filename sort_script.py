from pathlib import Path
import os, shutil, re, sys, glob
path:str=sys.argv[1]
frmt_dict:dict={'image':['jpeg', 'png', 'jpg', 'svg'],'video':['avi', 'mp4', 'mov', 'mkv'],'documents':['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],'audio':['mp3', 'ogg', 'wav', 'amr'],'archives':['zip', 'gz', 'tar','rar','7z']}
PATH_DICT={}
ignore_=['image','video','documents','audio','archives']
cyr='АaБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЫыЬьЭэЮюЯя'
lat=['A','a','B','b','V','v','G','g','D','d','E','e','Yo','yo','J','j','Z','z','I','i','Y','y','K','k','L','l','M','m','N','n','O','o','P','p','R','r','S','s','T','t','U','u','F','f','H','h','C','c','Ch','ch','Sh','sh','Sch','sch','YY','yy','"','"','E','e','Yu','yu','Ya','ya']

def normalize_path(path):#Дозволяє корегувати шлях при неправильному вводі в аргумент при запуску
    path=re.sub(r'[^\w]',' ',path).strip().split(' ')
    if path[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        path[0]=path[0]+':'
        path='/'.join(path)
    else:
        path='/'.join(path)
        path='/'+path
    path=Path(path)
    if path.is_dir()==True:
        return path
    else:
        return 0
    
def create_some_folders(path,frmt_dict,PATH_DICT):#Створює необхідний набір папок для сортування
    if path!=0:
        print('Path is correct...creating folders')
        for key in frmt_dict.keys():
            try:
                dir_path=Path(Path(f'{path}/{key}'))    
                os.makedirs(dir_path)
                PATH_DICT.update({key:dir_path})
            except FileExistsError:
                print('Direcory is exist')
                continue
    else:
        print('Incorrect path, try again')           
    return 0

def normalize_name(file_name):#Складає мапу траслітерації; Перебирає і замінює в строці назви файлу гліфи, які не відповідають критеріям
    trnslt_map={}
    cyr='АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЫыЬьЭэЮюЯя'
    lat=['A','a','B','b','V','v','G','g','D','d','E','e','Yo','yo','J','j','Z','z','I','i','Y','y','K','k','L','l','M','m','N','n','O','o','P','p','R','r','S','s','T','t','U','u','F','f','H','h','C','c','Ch','ch','Sh','sh','Sch','sch','YY','yy','"','"','E','e','Yu','yu','Ya','ya']

    for ch in cyr:
        trnslt_map.update({ord(ch): lat[0]})
        lat.pop(0)
    new_name=file_name.translate(trnslt_map)
    new_str=''
    for ch in new_name:
        print(ord(ch))
        if ord(ch) != 46 and ord(ch) not in range(97,123) and ord(ch) not in range(48,58) and ord(ch) not in range(65,91):
            new_str=new_str+'_'
        else:
            new_str+=ch
    new_name=new_str
    print(trnslt_map)
    return new_name

def sort_file(path,frmt_dict,PATH_DICT,ignore_):#Сортувальна функція
    print('Sorting has been initiliazed')
    file_list=os.listdir(path)
    #Перевірка на вміст папки, якщо пуста - видалення
    if file_list:
        for file_name in file_list:
            print(f'Sorting...{file_name}')
            src_old=Path(f'{path}/{file_name}')
            #Приведення файлнейму до критеріїв
            file_name=normalize_name(file_name)
            print(file_name)
            src=Path(f'{path}/{file_name}')
            #Перейменування файлів
            os.rename(src_old,src)
            check=src.is_dir()
            #Перевірка по критерію: чи є файл папкою, якщо файл - папка, чи є назва в ігнор лісті, якщо ні, то рекурсія, якщо файл - продовжуємо
            if check==False:
                src_format=re.search(r'[.]\w{2,}',file_name).group().strip('.')
                arc_frmt=frmt_dict.get('archives')
                #Перевірка по критерію: чи є файл архівом, якщо архів - створення папки з назвою та розархівування
                if src_format in arc_frmt:
                    print(f'{file_name} is archive')
                    acr_dir_path=PATH_DICT.get('archives')
                    arc_name=re.sub(r'[.]\w{2,}','',file_name)
                    dst=Path(f'{acr_dir_path}/{arc_name}')
                    os.makedirs(dst)
                    print('Unpacking archive...')
                    shutil.unpack_archive(src,dst,src_format)
                    os.remove(src)
                else:
                    for key,value in frmt_dict.items():
                        if src_format in value:
                            dst=Path(PATH_DICT.get(key))
                            shutil.move(src,dst)
            elif file_name in ignore_:
                continue
            else:
                print(f'{file_name} is directory...Entering')
                sort_file(src,frmt_dict,PATH_DICT,ignore_)
    else:
        print(f'Empty folder {path} deleted')
        # os.remove(path)
    print('Sorting has been finished')                      
    return 0


normalize_path(path)
create_some_folders(path,frmt_dict,PATH_DICT)
sort_file(path,frmt_dict,PATH_DICT,ignore_)
