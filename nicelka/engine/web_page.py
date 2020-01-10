from time import sleep
from abc import abstractmethod

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class WebPage:
    def __init__(self, executable_path='D:\\Program Files\\chromedriver.exe'):
        self._executable_path = executable_path
        self._driver = None

    def start(self):
        self._driver = webdriver.Chrome(executable_path=self._executable_path)
        self._driver.maximize_window()

    def stop(self):
        self._driver.close()
        self._driver = None

    @abstractmethod
    def search(self, *args, **kwargs):
        self._raise_not_implemented_error('search')

    def _raise_not_implemented_error(self, method_name):
        raise NotImplementedError('{} class missing required implementation of method: {}'.format(self.__class__.__name__, method_name))

    def _wait_for_element_by_class_name(self, class_name):
        try:
            return self._driver.find_element_by_class_name(class_name)
        except NoSuchElementException:
            sleep(0.5)
            return self._driver.find_element_by_class_name(class_name)

    def _back(self):
        self._driver.back()
        sleep(1)
