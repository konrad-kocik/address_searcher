from time import sleep

from exceptbool import except_converter
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

from nicelka.engine.web_page import WebPage
from nicelka.exceptions.exceptions import KrkgwPageException
from nicelka.logger.logger import Logger


class KrkgwPage(WebPage):
    def __init__(self, executable_path):
        super(KrkgwPage, self).__init__(executable_path=executable_path)
        self._name = 'krkgw_page'
        self._url = 'https://krkgw.arimr.gov.pl/'

    def search(self, city_name):
        self._enter_query(city_name)
        return self._get_results()

    def _enter_query(self, city_name):
        Logger.debug(self, "Searching for city name: '{}'".format(city_name))

        try:
            search_input = self._find_element_by_id('kgw')
            search_input.clear()
            search_input.send_keys(city_name)

            sleep(0.3)
            search_button = self._find_element_by_id('search')
            search_button.click()
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            Logger.error(self, e, self._enter_query.__name__)
            raise KrkgwPageException('Failed to enter query')

    def _get_results(self):
        results = []

        if not self._is_result_present():
            self._close_alert()
            return results

        results.extend(self._get_results_from_current_page())
        page_links = self._get_page_links()

        if not page_links:
            return results
        else:
            page_links.pop(0)

        for page_number, page_link in enumerate(page_links, start=2):
            try:
                page_link = self._find_element_by_link_text(str(page_number))
                page_link.click()
            except (NoSuchElementException, ElementClickInterceptedException) as e:
                Logger.error(self, e, self._get_results.__name__)
                continue
            else:
                results.extend(self._get_results_from_current_page())

        return results

    def _is_result_present(self, timeout=10):
        if self._is_alert_present():
            return False
        with except_converter(exc=TimeoutException) as result:
            self._wait_for_element_by_xpath('//*[@id="kgwTable"]/tbody/tr/td[5]/button', timeout=timeout)
            return result

    def _close_alert(self):
        self._driver.switch_to.alert.accept()

    def _get_page_links(self):
        page_links = []
        try:
            page_links = self._find_elements_by_class_name('page-link')
        except NoSuchElementException as e:
            Logger.error(self, e, self._get_page_links.__name__)
        finally:
            return [page_link for page_link in page_links if page_link.text not in ('<<', '<', '>', '>>')]

    def _get_results_from_current_page(self):
        results = []
        i = 0
        while True:
            i += 1
            try:
                info_button_xpath = '//*[@id="kgwTable"]/tbody/tr[{}]/td[5]/button'.format(i)
                self._wait_for_clickability_by_xpath(info_button_xpath, timeout=3)
                info_button = self._find_element_by_xpath(info_button_xpath)
                info_button.click()

                name, address = self._get_result_details()
                results.append(name + '\n' + self._format_address(address) + '\n')

                self._close_details()
            except ElementClickInterceptedException as e:
                Logger.error(self, e, self._get_results_from_current_page.__name__)
            except KrkgwPageException as e:
                Logger.error(self, e, self._get_results_from_current_page.__name__)
                self._close_details()
            except (TimeoutException, NoSuchElementException):
                break
        return results

    def _get_result_details(self):
        try:
            name_output_xpath = '//*[@id="zawartosc"]/table[1]/tbody/tr[3]/td[2]'
            self._wait_for_visibility_by_xpath(name_output_xpath, timeout=10)
            name_output = self._find_element_by_xpath(name_output_xpath)
            name = name_output.text

            address_output_xpath = '//*[@id="zawartosc"]/table[1]/tbody/tr[4]/td[2]'
            self._wait_for_visibility_by_xpath(address_output_xpath, timeout=10)
            address_output = self._find_element_by_xpath(address_output_xpath)
            address = address_output.text
        except (TimeoutException, NoSuchElementException) as e:
            Logger.error(self, e, self._get_result_details.__name__)
            raise KrkgwPageException('Failed to get result details')
        return name, address

    @staticmethod
    def _format_address(address):
        return address.replace(', ', '\n')

    def _close_details(self):
        try:
            close_button_xpath = '//*[@id="myModal"]/div/div/div[1]/button'
            self._wait_for_clickability_by_xpath(close_button_xpath)
            sleep(0.3)
            close_button = self._find_element_by_xpath(close_button_xpath)
            close_button.click()
            sleep(1)
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            Logger.error(self, e, self._get_results.__name__)
            raise KrkgwPageException('Failed to close details')
