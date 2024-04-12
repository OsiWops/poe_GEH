import requests
import psutil
import time
from tkinter import messagebox
import os

URL = 'https://raw.githubusercontent.com/OsiWops/poe_GEH/main/version.txt'
RootURL = 'https://raw.githubusercontent.com/OsiWops/poe_GEH/main'

# настройки
mainprocessname = r"firefox.exe"


def checkProcessByName(processname):
    for proc in psutil.process_iter():
        name = proc.name()
        if name == processname:
            return True
            break
    return False

def waitCloseProcessByName(processname):
    i = 0
    while True:
        if checkProcessByName(processname) == True:
            messagebox.showerror(master = None, title='Ошибка обновления GuildEventHellper',message= 'Процесс приложения не завершен, завершите его через диспетчер задач и попробуйте снова.' )
            print(f'Процесс запущен')
            break
        if i == 3:
            print(f'Процесс не существует')
            break
        i = i + 1
        time.sleep(1)

def ReadActualVersionFile():
    file = open("checkactualversion.txt", "r")
    while True:
        line = file.readline()
        path = line.split(' ')
        if not line:
            break
        path[1] = path[1].replace("\n","")
        print(f"{path[0]} and {path[1]}")
        DownloadFile(path[0])
    file.close()
        
def DownloadFile(sURLname):
    fullURL = RootURL + sURLname
    print(fullURL)
    #response = requests.get(sURLname)
    print(f'Файл сущетсвует, удаляем {sURLname}')
    if os.path.isfile(sURLname):
        print(f'Файл сущетсвует, удаляем {sURLname}')
        os.remove(sURLname)
    #open("sURLname", "wb").write(response.content)

waitCloseProcessByName(mainprocessname)
#print(f"{checkProcessByName()}")

response = requests.get(URL)

open("checkactualversion.txt", "wb").write(response.content)
ReadActualVersionFile()
os.remove("checkactualversion.txt")

#file = open('actualversion.txt',"r")
#version = file.readline()