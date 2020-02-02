from time import sleep

from exceptbool import except_to_bool
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

from nicelka.engine.web_page import WebPage
from nicelka.exceptions.exceptions import GooglePageException
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
        if self._is_single_result():
            return self._get_single_result()
        elif self._are_multiple_results():
            return self._get_multiple_results()
        else:
            return []

    @except_to_bool(exc=NoSuchElementException)
    def _is_single_result(self):
        self._find_element_by_class_name('LrzXr')

    @except_to_bool(exc=NoSuchElementException)
    def _are_multiple_results(self):
        self._find_element_by_class_name('i0vbXd')

    def _get_single_result(self):
        Logger.debug(self, 'Getting single result...')
        result = []

        try:
            name_output_xpath = '//div[@class="SPZz6b"]//span'
            self._wait_for_element_by_xpath(name_output_xpath, timeout=2)
            name_output = self._find_element_by_xpath(name_output_xpath)

            address_output_class = 'LrzXr'
            self._wait_for_element_by_class_name(address_output_class, timeout=2)
            address_output = self._find_element_by_class_name(address_output_class)

            result.append(name_output.text + '\n' + self._format_address(address_output.text) + '\n')
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            Logger.error(self, e, self._get_single_result.__name__)
            raise GooglePageException('Failed to get single result')

        return result

    def _get_multiple_results(self):
        Logger.debug(self, 'Getting multiple results...')
        results = []
        result_link_class = 'dbg0pd'

        try:
            self._open_map()
            self._wait_for_element_by_class_name(result_link_class, 2)

            for result_link in self._find_elements_by_class_name(result_link_class):
                name, address = self._get_one_of_multiple_results(result_link)
                results.append(name + '\n' + self._format_address(address) + '\n')
        except (TimeoutException, NoSuchElementException, GooglePageException) as e:
            Logger.error(self, e, self._get_multiple_results.__name__)

        return results

    def _open_map(self):
        try:
            map_link = self._wait_for_element_by_class_name('i0vbXd')
            map_link.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            Logger.error(self, e, self._open_map.__name__)
            raise GooglePageException('Failed to open a map')

    def _get_one_of_multiple_results(self, result_link):
        try:
            result_link.click()
            sleep(1)

            name_output_xpath = '//div[@class="SPZz6b"]//span'
            self._wait_for_element_by_xpath(name_output_xpath, timeout=2)
            name_output = self._find_element_by_xpath(name_output_xpath)

            address_output_class = 'LrzXr'
            self._wait_for_element_by_class_name(address_output_class, timeout=1)
            address_output = self._find_element_by_class_name(address_output_class)
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            Logger.error(self, e, self._get_one_of_multiple_results.__name__)
            raise GooglePageException('Failed to get one of multiple results')

        return name_output.text, address_output.text

    @staticmethod
    def _format_address(address):
        return address.replace(', ', '\n')
