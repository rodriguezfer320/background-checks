from abc import ABC, abstractmethod
from os import getcwd

class BackgroundWeb(ABC):

    def __init__(self, driver, description):
        self._data_web = None
        self._driver = driver
        self._description = description
        self._dir_download = getcwd() + r'/app/static/download/'
    
    # Getters    
    @property
    def driver(self):
        return self._driver

    @property
    def description(self):
        return self._description

    @property
    def dir_download(self):
        return self._dir_download

    # Setters
    @driver.setter
    def driver(self, driver):
        self._driver = driver
        
    @description.setter
    def description(self, description):
        self._description = description

    @dir_download.setter
    def dir_download(self, dir_download):
        self._dir_download = dir_download

    @abstractmethod
    def get_background_information(self, data):
        pass
    
    @abstractmethod
    def process_information(self, data):
        pass