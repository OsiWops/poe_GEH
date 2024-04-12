# Версия v.1.3 от 20.01.2024, 22:02
import os
import datetime
import time
import tkinter as tk
from tkinter import filedialog
import configparser
import pygetwindow
import keyboard
import threading
from PIL import Image, ImageTk
import re
from pystray import Icon, MenuItem as item

from configuration import Configuration

class Exit_flag:
    def __init__(self):
        self.val = False
    def false(self):
        self.val = True
    def get_val(self):
        return self.val

exit_flag = Exit_flag()
cfg = Configuration()

current_utc_time = datetime.datetime.now(datetime.timezone.utc)
current_time = (current_utc_time + datetime.timedelta(hours=3)).strftime("%H:%M:%S")

# Добавьте определение переменной previous_lines
previous_lines = set()

def close_window_after_1min(window):
    window.after(60000, window.destroy)

def handle_choice(choice):
    if choice == "Участвую":
        game_window = pygetwindow.getWindowsWithTitle('Path of Exile')[0]
        game_window.activate()
        keyboard.send('enter')
        keyboard.write('%Участвую')
        keyboard.send('enter')
        root.after(1000, close_window)

    print(choice)

def close_window():
    root.destroy()

def show_choice_window(time_date, message):
    global root
    root = tk.Tk()
    root.attributes("-alpha", 1)
    root.title("Оповещение события")
    root.attributes('-topmost', True)

    
    main_frame = tk.Frame(root)
    main_frame.pack()



    label_date = tk.Label(main_frame, text=f"Дата и время: {time_date}", font=("Arial", 14))
    label_date.pack()

    # Используем регулярные выражения для извлечения информации из строки события
    match = re.search(r'(.+?): .*событие: (.+?)\..*требования: (.+?)\..*цена: (.+?)\.? (.+?)\..?', message)
    
    if match:
        message_autor = re.search(r'(.+?)\:', message)
        print(f"автор {message_autor.group(0)}")
        message_requirements = re.search(r'событие:(.+?) требования',message)
        print(f"автор {message_requirements.group(0)}")
        message_price = re.search(r'цена:(.+?)\.',message)
        print(f"цена {message_price.group(1)}")
        author = match.group(1)
        event = match.group(2)
        requirements = match.group(3)
        price = match.group(4) + ' ' + match.group(5) if match.group(4) else "0"

        # Выделение важных моментов оповещения
        label_author = tk.Label(main_frame, text=f"<< {author} >>", font=("Arial", 24), padx=10, pady=10)
        label_author.configure(bg="red")
        label_author.pack(fill=tk.X)

        label_event = tk.Label(main_frame, text=f"{event}", font=("Arial",33), padx=10, pady=10)
        label_event.configure(bg='yellow')
        label_event.pack(fill=tk.X)

        label_price = tk.Label(main_frame, text=f"ЦЕНА: {price}", font=("Arial", 33), padx=10, pady=10)
        label_price.configure(bg="green")
        label_price.pack(fill=tk.X)

        label_requirements = tk.Label(main_frame, text=f"ТРЕБОВАНИЯ: {requirements}", font=("Arial", 33), fg='white',  padx=10, pady=10)
        label_requirements.configure(bg="blue")
        label_requirements.pack(fill=tk.X)
    else:
        label_message = tk.Label(main_frame, text=f"ОПИСАНИЕ: {message}", font=("Arial", 24), wraplength=300)
        label_message.pack()

    button_frame = tk.Frame(main_frame)
    button_frame.pack()

    participate_button = tk.Button(button_frame, text="Участвую", padx=10, pady=10, command=lambda: handle_choice("Участвую"))
    participate_button.pack(side=tk.LEFT)

    decline_button = tk.Button(button_frame, text="Отказаться", padx=10, pady=10, command=root.destroy)
    decline_button.pack(side=tk.RIGHT)

    close_window_after_1min(root)
    root.bind("<Return>", lambda event: handle_choice("Участвую"))

    # Устанавливаем положение окна в левый верхний угол
    root.geometry("+10+10")

    root.mainloop()

def on_exit_clicked(icon, item):
    icon.stop()
    exit_flag.false()

def home_folder(icon, item):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    os.startfile(current_directory)

def selectClientLogFileClick(icon, item):
    cfg.selectClientLogFile()

def on_open_settings_clicked(icon, item):
    os.startfile('settingsg.ini')

def create_and_run_tray_icon():
    #load_config()
    global icon
    icon = create_tray_icon()
    icon.run()
    icon.stop()

#тестовая функция, что бы не дергать чат в игре, для работы раскомментировать пункт меню тест в трее
def test(icon, item):
    print('test')
    target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    line = '2024/01/19 22:25:09 812413625 cff94598 [INFO Client 13528][as] %Чувак: Народ! /сбор/ событие: голландский штурвал. требования: в носках и кепке. цена: 2 зеркала.'
    if '%' in line and '/сбор/' in line:
        log_parts = line.split(' ')
        log_time = log_parts[1]
        if True:
            message = line.split('%')[1].strip()
            log_datetime = f"{target_date} {log_time}"
            show_choice_window(log_datetime, message)

def test2(icon, item):
    print('test')
    target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    line = '2024/01/19 22:25:09 812413625 cff94598 [INFO Client 13528][as] %Чувак: Народ! /сбор/ собираемся в баре у Гоги, будем брить ноги'
    if '%' in line and '/сбор/' in line:
        log_parts = line.split(' ')
        log_time = log_parts[1]
        if True:
            message = line.split('%')[1].strip()
            log_datetime = f"{target_date} {log_time}"
            show_choice_window(log_datetime, message)

def create_tray_icon():
    print('Иконка')
    image_path = "ico.ico"  # Замените на путь к вашему изображению
    icon = Image.open(image_path) ##.resize((30, 30), Image.BICUBIC)
    #tk_icon = ImageTk.PhotoImage(icon)

    # Сохраните изображение в формате ICO
    #icon_path = 'ico.ico'
    #icon.save(icon_path, format='ICO')

    # В душе не ебу, почему он считает False из конфига == True, заебся дебажить, да будет так
    update = cfg.get_update()
    if update == 'False':
        update = False
    else: update = True

    menu = (item('Выход', lambda icon, item: on_exit_clicked(icon, item)),
            item('Указать файл Client.txt', lambda icon, item: selectClientLogFileClick(icon, item)),
            item('Открыть папку программы', lambda icon, item: home_folder(icon, item)),
            item('Открыть настройки', lambda icon, item: on_open_settings_clicked(icon, item)),
            item('Проверять обновления', ChangeUpdateSettings, checked = lambda item: update),
            item('Тест ЛГБТ', lambda icon, item: test(icon, item)),
            item('Тест Common', lambda icon, item: test2(icon, item)))

    icon_tray = Icon("name", icon, "Оповещение", menu)
    return icon_tray

def ChangeUpdateSettings(icon, item):
    cfg.set_update(not item.checked)
    
def check_file_for_new_lines():
    global previous_lines
    target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    if cfg.get_path_to_client_log() == '':
        import sys
        icon_thread.join(0)
        exit_flag.false()
    else:
        i = 0
        try:
            client_file_path = cfg.get_path_to_client_log()
            with open(client_file_path, 'r', encoding='utf-8') as file:
                lines = set(file.readlines())
                new_lines = lines.difference(previous_lines)
                for line in new_lines:
                    i += 1
                    if '%' in line and '/сбор/' in line:
                        log_parts = line.split(' ')
                        log_time = log_parts[1]
                        if target_date == log_parts[0]:
                            if log_time >= current_time:
                                message = line.split('%')[1].strip()
                                log_datetime = f"{target_date} {log_time}"
                                show_choice_window(log_datetime, message)
                                break
                previous_lines = lines.copy()
        except Exception as e:
            pass
            #print(f"Произошла ошибка при чтении файла: {e}")

def main():
    while not exit_flag.val:     
        check_file_for_new_lines()
        time.sleep(1)

# Создаем потоки для значка трея и основного цикла проверки client.txt
icon_thread = threading.Thread(target=create_and_run_tray_icon, name = 'TrayThread')
main_thread = threading.Thread(target=main, name = "MainThread")
icon_thread.start()
main_thread.start()

# Ждем флага закрытия процесса и на всякий случай прибиваем трей
while not exit_flag.get_val():
    time.sleep(1)
icon.stop()