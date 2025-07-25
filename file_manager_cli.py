import os
import shutil
import PIL.Image
from bs4 import BeautifulSoup
import urllib.request
import gdown
import pyautogui
import threading

def copyORmove():
    listoffilepath = []
    
    files_to_be_moved = []
    for num in range(100000):
        i = input('Enter the file names:\n>>')
        if i== '':
            break
        elif '.' in i:
           files_to_be_moved.append(i)
        else:
            files_to_be_moved.append(i + '.')
    source = input('Enter Source folder path:\n>>').replace('"','')
    destination = input('Enter destination:\n>>').replace('"','')
    for tuple in os.walk(source):
        for filename in tuple[2]:
            filepath = tuple[0] + "\\" + filename
            listoffilepath.append(filepath)
    np = 0
    for line in files_to_be_moved:
        def th():
            stripped_line = line.strip()
            for path in listoffilepath:
                components = path.split('\\')
                if components[-1].startswith(stripped_line) :
                    if Operation == 'copy':
                      shutil.copy(path,destination)
                    else:
                        shutil.move(path,destination)
                    break
        tho = threading.Thread(target=th)
        tho.start()
        np+=1
        if np%100 == 0:
            tho.join()

def copyORmoveANDsegregate():
    files_and_folders = []
    for i in range(100000):
        f = input('Enter filenames & folders separated by tab: ')
        if f == '':
            break
        else:
            if '.' in f:
               files_and_folders.append(f.replace('	','*#@',1).replace('	','\\'))
            else:
                files_and_folders.append(f.replace('	','.*#@',1).replace('	','\\'))
    source = input('Enter Source folder path:\n>>').replace('"','')
    destination = input('Enter destination:\n>>').replace('"','')
    listoffilepath = []
    for tuple in os.walk(source):
        for filename in tuple[2]:
            filepath = tuple[0] + "\\" + filename
            listoffilepath.append(filepath)
    for line in files_and_folders:
        stripped_line = line.strip()
        separate = stripped_line.split('*#@')
        folders = separate[1].split('\\')
        a = destination
        for folder in folders:
            a += '\\' + folder
            try:
                os.mkdir(a)
            except:
          
              pass  
    np = 0
    for line in files_and_folders:
        def th():
            stripped_line = line.strip()
            separate = stripped_line.split('*#@')
            for path in listoffilepath:
                components = path.split('\\')
                if components[-1].startswith(separate[0]):
                    if Operation == 'copy':
                       shutil.copy(path,destination + '\\' + separate[1])
                    else:
                        shutil.move(path,destination + '\\' + separate[1])
                    break
        tho = threading.Thread(target=th)
        tho.start()
        np+=1
        if np%100 == 0:
            tho.join()

def rename():
    old_and_new = []
    for i in range(100000):
        on = input('Enter the old path and new names separated by tab: ')
        if on == '':
            break
        else:
            if on.endswith('.jpg') or on.endswith('.png') or on.endswith('.pdf') or on.endswith('.jpeg') or on.endswith('.'):
                old_and_new.append(on.replace('	','*#@'))
            else:
                old_and_new.append(on.replace('	','*#@')+'.jpg')
    for line in old_and_new:
        separate = line.split('*#@')
        old_name = separate[0]
        components_list = separate[0].split('\\')
        components_list.pop()
        path = ''
        for component in components_list:
            path += component +'\\'
        new_name = path + separate[1]
        try:
            os.rename(old_name.strip(),new_name.strip())
        except:
            pass

def resize():
    listoffilepath = []
    target = input('Enter the target folder:\n>>').replace('"','')
    W = int(input('minimum width should be:\n>>'))
    H = int(input('minimum height should be:\n>>'))
    for tuple in os.walk(target):
        for filename in tuple[2]:
            filepath = tuple[0] + "/" + filename
            a=filepath.replace("\\","/")
            listoffilepath.append(a)   
    np=0
    for line in listoffilepath:
        def res():
            try:
                file_path = line.strip()
                im =PIL.Image.open(file_path)
                width,height = im.size
                if width < W:
                    ratio = height/width
                    new_width =W
                    new_height = int(ratio*new_width)
                    if new_height < H:
                        new_ratio = new_width/new_height
                        final_height = H
                        final_width = int(new_ratio*final_height) 
                        resized_im = im.resize((final_width,final_height))
                        os.remove(file_path)
                        resized_im.save(file_path)
                        print(file_path + "-->(" + str(final_width) + "," + str(final_height) + ") Resized!")
                    else:
                        resized_im = im.resize((new_width,new_height))
                        os.remove(file_path)
                        resized_im.save(file_path)
                        print(file_path + "-->(" + str(new_width) + "," + str(new_height) + ") Resized!")
                elif height < H:
                    ratio = width/height
                    new_height = H
                    new_width = int(ratio*new_height)
                    resized_im = im.resize((new_width,new_height))
                    os.remove(file_path)
                    resized_im.save(file_path)
                    print(file_path + "-->(" + str(new_width) + "," + str(new_height) + ") Resized!")
                else:
                    print(file_path + "-->(" + str(width) + "," + str(height) + ") Already Proper sized!")
            except:
                print("sorry")
        th = threading.Thread(target=res)
        th.start()
        np+=1
        if np%15 == 0:
            th.join()


def download():
    a = []
    link_and_filename = []
    for i in range(100000):
        lnk = input('Enter the link and filenames separated by tab')
        if lnk == '':
            break
        else:
            if lnk.endswith('.jpg'):
               link_and_filename.append(lnk.replace('	','*#@'))
            else:
                link_and_filename.append(lnk.replace('	','*#@') + '.jpg')
    dest =  input('enter the destination: ')
    for line in link_and_filename:
        try:
            def dow():
                a = []
                if 'http' in line.strip():
                    stripped_line = line.strip()
                else:
                    stripped_line = 'https://'+ line.strip()
                separate=stripped_line.split("*#@")
                filename = separate[1]
                if "drive.google.com" in separate[0]:
                    img_url = 'https://drive.google.com/uc?id='+separate[0].split('/')[5]
                    gdown.download(img_url.strip(), dest + '\\' + filename, quiet=False)
                    print(filename + " downloaded successfully !")
                    img_url = ""
                elif ".jpg" in separate[0] or ".png" in separate[0] or ".jpeg" in separate[0] or ".webp" in separate[0] or "duckduckgo" in separate[0] or "flickr" not in separate[0]:
                    img_url=separate[0]
                    print("if")
                    urllib.request.urlretrieve(img_url.strip(),dest + '\\' + filename)
                    print(filename + " downloaded successfully !")
                    img_url = ""
                else:
                    url = separate[0].strip()
                    r = requests.get(url)
                    soup = BeautifulSoup(r.text,'html.parser')
                    images= soup.find_all('img')
                    for image in images:
                        if ".jpg" in image['src']:
                            a.append(image['src'])
                    for item in a:
                        if "https:" not in item:
                            img_url= "https:" + item
                        else:
                                img_url= item
                    a = []
                    urllib.request.urlretrieve(img_url.strip(),dest + '\\' + filename)
                    print(filename + " downloaded successfully !")
                    img_url = ""
            t = threading.Thread(target=dow)
            t.start()
        except:
            print('sorry')

def delete_files():
    listoffilepath = []
    files_to_be_deleted = []
    for num in range(100000):
        i = input('Enter file names to be deleted:\n>>')
        if i== '':
            break
        elif '.' in i:
           files_to_be_deleted.append(i)
        else:
            files_to_be_deleted.append(i + '.')
    source = input('Enter Source folder path:\n>>').replace('"','')
    for tuple in os.walk(source):
        for filename in tuple[2]:
            filepath = tuple[0] + "\\" + filename
            listoffilepath.append(filepath)
    for line in files_to_be_deleted:
        stripped_line = line.strip()
        for path in listoffilepath:
            components = path.split('\\')
            if components[-1].lower().startswith(stripped_line.lower()):
                try:
                   os.remove(path)
                except:
                    pass
                break

def Mkdir():
    file = []
    for num in range(100000):
        i = input('Enter the directories to be made:\n>>')
        if i== '':
            break
        else:
            file.append(i)
    destination = input('Enter destination:\n>>').replace('"','')
    for line in file:
        stripped_line = line.strip()
        folders = stripped_line.split('\\')
        a = destination
        for folder in folders:
            a += '\\' + folder
            try:
                os.mkdir(a)
            except:
                pass
 
def Rmdir():
    listofFolders = []
    source = input('Enter the source folder path:\n>>')
    for tuple in os.walk(source):
        listofFolders.append(tuple[0])
    for i in range(20):
        for folder in listofFolders:
            try:
                os.rmdir(folder)
            except:
                pass  

def maps():
    file = open("google_maps_image_links.txt","w")
    i = input('hover the mouse on next button and press Enter')
    nextx,nexty = pyautogui.position()
    i = input('hover the mouse on url bar and press Enter')
    urlx,urly = pyautogui.position()
    def cliking():
        prev_link =''
        cliks = int(input('enter the number of photos: '))
        for i in range(cliks):
            pyautogui.click(urlx,urly)
            pyautogui.hotkey('ctrl','c')
            pyautogui.hotkey('alt','tab')
            pyautogui.hotkey('ctrl','v')
            pyautogui.hotkey('enter')
            link = input('link: ')
            if link == prev_link:
                pass
            else:
                prev_link = link
                try:
                    file.write(link + '\n')
                except:
                    pass
            pyautogui.click(nextx,nexty)
        any_more_link = input('Are there more photos(Y/N): ')
        if any_more_link.lower() == 'y':
            cliking()
        elif any_more_link.lower() == 'n':
            pass
        else:
            print('sorry i do not understand!')
    cliking()
    file.close()

def asking_query():
    global Operation
    Query = input('What do you want to do? \n(a)copy           (b)move                 (c)rename  \n(d)resize         (e)download files       (f)delete files\n(g)make folders   (h)remove empty folders (i)get google maps image links\n(j)quit \n>>').lower()
    if Query == 'c':
        rename() 
    elif Query == 'd':
        resize()
    elif Query == 'a' or Query == 'b':
        if Query == 'a':
          Operation = 'copy'
        else:
          Operation = 'move'
        prompt = input('Do you want any segregation? (Y/N):  ')
        if prompt == 'y':
           copyORmoveANDsegregate()
        elif prompt == 'n':
           copyORmove()
        else:
            print('sorry I can not understand')
            asking_query()
    # elif Query == 'e':
    #     download() 
    elif Query == 'f':
        delete_files()
    elif Query == 'g':
        Mkdir()
    elif Query == 'h':
        Rmdir()
    # elif Query == 'i':
    #     maps()
    elif Query == 'j':
        print('thank you!')
    else:
        print('sorry I can not understand')
        asking_query()
asking_query()