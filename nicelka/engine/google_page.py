from time import sleep

from exceptbool import except_to_bool
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

from nicelka.engine.web_page import WebPage
from nicelka.logger.logger import Logger


class GooglePage(WebPage):
    def __init__(self, executable_path):
        super(GooglePage, self).__init__(executable_path=executable_path)
        self._name = 'google_page'
        self._url = 'https://google.pl'

    def search(self, city, key):
        Logger.debug(self, "Searching for city: '{}' key: '{}'".format(city, key))
        self._enter_query(city, key)
        return self._get_results()

    def _enter_query(self, city, key):
        sleep(1)
        self._driver.get(url=self._url)
        search_input = self._find_element_by_name('q')
        search_input.send_keys('{} {} adres'.format(city, key))
        search_input.send_keys(Keys.ENTER)

    def _get_results(self):
        return self._get_single_result() if self._is_single_result() else self._get_multiple_results()

    @except_to_bool(exc=Exception)
    def _is_single_result(self):
        self._find_element_by_class_name('LrzXr')

    def _get_single_result(self):
        result = []

        try:
            name_output_xpath = '//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/span'
            self._wait_for_element_by_xpath(name_output_xpath, timeout=2)
            name_output = self._find_element_by_xpath(name_output_xpath)

            address_output_class = 'LrzXr'
            self._wait_for_element_by_class_name(address_output_class, timeout=2)
            address_output = self._find_element_by_class_name(address_output_class)

            result.append(name_output.text + '\n' + self._format_address(address_output.text) + '\n')
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            pass

        return result

    def _get_multiple_results(self):
        results = []

        try:
            self._open_map()

            for result_link in self._find_elements_by_class_name('dbg0pd'):
                name, address = self._get_one_of_multiple_results(result_link)
                results.append(name + '\n' + self._format_address(address) + '\n')
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            pass

        return results

    def _open_map(self):
        map_link = self._wait_for_element_by_class_name('i0vbXd')
        map_link.click()

    def _get_one_of_multiple_results(self, result_link):
        result_link.click()
        sleep(1)

        name_output_xpath = '/html/body/div[6]/div[3]/div[9]/div[1]/div[3]/div/div[2]/async-local-kp/div/div/' \
                            'div[1]/div/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/span'
        self._wait_for_element_by_xpath(name_output_xpath, timeout=1)
        name_output = self._find_element_by_xpath(name_output_xpath)

        address_output_class = 'LrzXr'
        self._wait_for_element_by_class_name(address_output_class, timeout=1)
        address_output = self._find_element_by_class_name(address_output_class)

        return name_output.text, address_output.text

    @staticmethod
    def _format_address(address):
        return address.replace(', ', '\n')
