import configparser
from tkinter import filedialog

class Configuration:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        self.path_to_game_log_file = ''
        self.check_update = bool('False')
        self.debug = False
        self.load_config_from_file()
        self.fullMessage: str = ''
        self.log_datetime: str = ''

    def set_log_datetime(self, log_datetime):
        self.log_datetime = log_datetime

    def get_log_datetime(self):
        return self.log_datetime

    def set_fullMessage(self, message:str):
        self.fullMessage = message

    def get_fullMessage(self):
        return self.fullMessage

    def clearMessage(self):
        self.log_datetime = ''
        self.fullMessage = ''

    def load_config_from_file(self):
        
        # Проверить верхнюю ноду, если нет создать
        if 'FileSettings' not in self.config:
            self.config['FileSettings'] = {}
            self.save_config_to_file(self.config)
        # Параметр дебага
        if 'debug' not in self.config['FileSettings']:
            self.debug = False
            self.config['FileSettings']['debug'] = 'False'
            self.save_config_to_file(self.config)
        else:
            self.debug = self.config['FileSettings']['debug']
        # Параметр автообновления
        if 'check_update' not in self.config['FileSettings']:
            self.check_update = bool('True')
            self.config['FileSettings']['check_update'] = 'False'
            self.save_config_to_file(self.config)
        else:
            self.check_update = self.config['FileSettings']['check_update']
        # Путь к логу клиента игры
        if 'client_file_path' not in self.config['FileSettings']:
            client_file_path = filedialog.askopenfilename(title="Выберите файл в папке Path of Exile\\logs\\Client.txt")
            if client_file_path:
                self.config['FileSettings']['client_file_path'] = client_file_path
                self.path_to_game_log_file = client_file_path
                self.save_config_to_file(self.config)
            # Открыть проводник к файлу
        else:
            self.path_to_game_log_file = self.config['FileSettings']['client_file_path']

    def selectClientLogFile(self):
        if 'FileSettings' not in self.config:
            self.config['FileSettings'] = {}
            self.save_config_to_file(self.config)
        client_file_path = filedialog.askopenfilename(title="Выберите файл в папке Path of Exile\\logs\\Client.txt")
        if client_file_path:
            self.config['FileSettings']['client_file_path'] = client_file_path
            self.path_to_game_log_file = client_file_path
            self.save_config_to_file(self.config)


    def save_config_to_file(self, config):
        self.config = config
        with open('settings.ini', 'w') as self.configfile:
            self.config.write(self.configfile)

    def get_path_to_client_log(self):
        return self.path_to_game_log_file
    
    def get_update(self):
        return self.check_update

    def set_update(self, value):
        self.check_update = value
        self.config['FileSettings']['check_update'] = str(value)
        self.save_config_to_file(self.config)


