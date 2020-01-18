from time import sleep

from exceptbool import except_converter
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from nicelka.engine.web_page import WebPage
from nicelka.logger.logger import Logger


class KrkgwPage(WebPage):
    def __init__(self, executable_path):
        super(KrkgwPage, self).__init__(executable_path=executable_path)
        self._name = 'krkgw_page'
        self._url = 'https://krkgw.arimr.gov.pl/'

    def search(self, city_name):
        Logger.debug(self, "Searching for city name: '{}'".format(city_name))
        self._enter_query(city_name)
        return self._get_results()

    def _enter_query(self, city_name):
        search_input = self._find_element_by_id('kgw')
        search_input.clear()
        search_input.send_keys(city_name)
        sleep(0.3)
        search_button = self._find_element_by_id('search')
        search_button.click()

    def _close_cookies_info(self):
        close_button_xpath = '/html/body/div[1]/div/a'
        try:
            self._wait_for_clickability_by_xpath(close_button_xpath, timeout=0.2)
            close_button = self._find_element_by_xpath(close_button_xpath)
            close_button.click()
        except (TimeoutException, NoSuchElementException):
            pass
        except Exception as e:
            Logger.error(self, e)

    def _get_results(self):
        results = []

        if not self._is_result_present():
            self._close_alert()
            return results

        i = 0
        while True:
            i += 1
            try:
                info_button_xpath = '//*[@id="kgwTable"]/tbody/tr[{}]/td[5]/button'.format(i)
                self._wait_for_clickability_by_xpath(info_button_xpath, timeout=5)
                info_button = self._find_element_by_xpath(info_button_xpath)
                info_button.click()

                name_output_xpath = '//*[@id="zawartosc"]/table[1]/tbody/tr[3]/td[2]'
                self._wait_for_visibility_by_xpath(name_output_xpath, timeout=10)
                name_output = self._find_element_by_xpath(name_output_xpath)

                address_output_xpath = '//*[@id="zawartosc"]/table[1]/tbody/tr[4]/td[2]'
                self._wait_for_visibility_by_xpath(address_output_xpath, timeout=10)
                address_output = self._find_element_by_xpath(address_output_xpath)

                results.append(name_output.text + '\n' + self._format_address(address_output.text) + '\n')

                self._close_details()
            except TimeoutException:
                break
            except Exception as e:
                Logger.error(self, e)
                break

        return results

    def _is_result_present(self, timeout=10):
        if self._is_alert_present():
            return False
        with except_converter(exc=TimeoutException) as result:
            self._wait_for_element_by_xpath('//*[@id="kgwTable"]/tbody/tr/td[5]/button', timeout=timeout)
            return result

    def _close_alert(self):
        self._driver.switch_to.alert.accept()

    @staticmethod
    def _format_address(address):
        return address.replace(', ', '\n')

    def _close_details(self):
        close_button_xpath = '//*[@id="myModal"]/div/div/div[1]/button'
        self._wait_for_clickability_by_xpath(close_button_xpath)
        close_button = self._find_element_by_xpath(close_button_xpath)
        close_button.click()
        sleep(1)
