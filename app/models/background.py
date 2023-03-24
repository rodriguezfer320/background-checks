from abc import ABC, abstractmethod

class Background(ABC):
    
    def __init__(self, driver):
        self._driver = driver
        self._text = ''

    @abstractmethod
    def search_for_background(self, data):
        pass

    #Getters
    @property
    def driver(self):
        return self._driver

    @property
    def text(self):
        return self._text

    #Setters
    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @text.setter
    def text(self, text):
        self._text = text 