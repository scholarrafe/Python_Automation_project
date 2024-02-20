import os
from os.path import splitext
from shutil import move


# e.g 'C:/Users/User/Downloads/New folder (3)/'
dirs = input("Give any directory here : ")


for dir in os.scandir(dirs):
    if dir.is_file():
        link, extension = splitext(dir.name)
        if not os.path.exists(f"{dirs}{extension.strip('.')}-files"):
            os.mkdir(f"{dirs}{extension.strip('.')}-files")
        move(f"{dirs}{dir.name}",f"{dirs}{extension.strip('.')}-files/{dir.name}")
        
        
        


    