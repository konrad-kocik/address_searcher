from time import sleep

from exceptbool import except_to_bool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class WebBrowser:
    def __init__(self, executable_path='D:\Program Files\chromedriver.exe'):
        self._executable_path = executable_path
        self._driver = None

    def start(self):
        self._driver = webdriver.Chrome(executable_path=self._executable_path)
        self._driver.maximize_window()

    def stop(self):
        self._driver.close()
        self._driver = None

    def search(self, city, key):
        self._enter_query(city, key)
        return self._get_single_result() if self._is_single_result() else self._get_multiple_results()

    def _enter_query(self, city, key):
        sleep(1)
        self._driver.get(url='https://google.pl')
        search_input = self._driver.find_element_by_name('q')
        search_input.send_keys('{} {} adres'.format(city, key))
        search_input.send_keys(Keys.ENTER)

    @except_to_bool(exc=Exception)
    def _is_single_result(self):
        self._driver.find_element_by_class_name('LrzXr')

    def _get_single_result(self):
        name_output = self._driver.find_element_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/span')
        address_output = self._driver.find_element_by_class_name('LrzXr')
        return [name_output.text + '\n' + self._format_address(address_output.text) + '\n']

    def _get_multiple_results(self):
        max_results_count = 3
        results = []

        for i in range(max_results_count):
            try:
                try:
                    xpath = '//*[@id="rso"]/div[1]/div/div/div[2]/div/div[4]/div[1]/div[1]/div/div/a[1]/div/div/span' if i == 0 else \
                            '//*[@id="rso"]/div[1]/div/div/div[2]/div/div[4]/div[1]/div[{}]/div[2]/div/a[1]/div/div/span'.format(i + 1)
                    name, address = self._get_one_of_multiple_results(xpath)
                except NoSuchElementException:
                    xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[1]/div[1]/div[2]/div/a[1]/div/div/span' if i == 0 else \
                            '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[1]/div[{}]/div/div/a[1]/div/div/span'.format(i + 1)
                    name, address = self._get_one_of_multiple_results(xpath)

                results.append(name + '\n' + address + '\n')
                self._back()
            except Exception:
                pass

        return results

    def _get_one_of_multiple_results(self, xpath):
        name_output = self._driver.find_element_by_xpath(xpath)
        name = name_output.text
        name_output.click()
        sleep(1)
        address_output = self._wait_for_element_by_class_name('LrzXr')
        address = self._format_address(address_output.text)
        return name, address

    @staticmethod
    def _format_address(address):
        return address.replace(', ', '\n')

    def _wait_for_element_by_class_name(self, class_name):
        try:
            return self._driver.find_element_by_class_name(class_name)
        except NoSuchElementException:
            sleep(0.5)
            return self._driver.find_element_by_class_name(class_name)

    def _back(self):
        self._driver.back()
        sleep(1)
