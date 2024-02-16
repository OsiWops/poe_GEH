from pathlib import Path
import win32con
import win32console
import win32gui
import time
import threading
from PIL import Image
#from bs4 import BeautifulSoup
from pystray import Icon, MenuItem, Menu
#from requests import get
#from win11toast import toast

class Exit_flag:
    def __init__(self):
        self.val = False
    def change(self):
            self.val = True

Exit_flag  = Exit_flag()

def click(icon: Icon, item: MenuItem):
    """
    Обработка полученных значений меню. В зависимости от выбранного пункта.
    """
    if str(item) == 'Настройки':
        print(f"Открыть Настройки")
        
    elif str(item) == 'Выход':
        Exit_flag.change()
        icon.stop()
        #root.quit()

def main():
    image = Image.open(Path.cwd() / "pic" / "cat.png")
    icon = Icon('Cat Vampire', image, menu=Menu(
        MenuItem('Настройки', click),
        MenuItem('Выход', click)
    ))
    win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_HIDE)
    icon.run()

def testThread():
    while not Exit_flag.val:
        print(f'работа потока пока Exit_flag = {Exit_flag.val}')
        time.sleep(1)

thread1 = threading.Thread(target=testThread, name="Thread-1")
thread2 = threading.Thread(target=main, name="MainThread")
thread1.start()
thread2.start()
thread1.join()
thread2.join()