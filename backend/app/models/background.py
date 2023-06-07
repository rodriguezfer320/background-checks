from abc import ABC, abstractmethod
from os import getcwd

class Background(ABC):

    def __init__(self, driver):
        self._driver = driver
        self._dir_download = getcwd() + r'/app/static/download/'
        self._text = {
            'title': None,
            'date': None,
            'message': None,
            'data': None,
            'link': None
        }

    @abstractmethod
    def search_for_background(self, data):
        pass

    # Getters
    @property
    def driver(self):
        return self._driver

    @property
    def dir_download(self):
        return self._dir_download

    @property
    def text(self):
        return self._text

    # Setters
    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @dir_download.setter
    def dir_download(self, dir_download):
        self._dir_download= dir_download

    @text.setter
    def text(self, text):
        self._text = text