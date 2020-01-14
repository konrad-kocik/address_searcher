from time import sleep

from exceptbool import except_to_bool
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from nicelka.engine.web_page import WebPage


class GooglePage(WebPage):
    def __init__(self, executable_path):
        super(GooglePage, self).__init__(executable_path=executable_path)
        self._name = 'google_page'
        self._url = 'https://google.pl'

    def search(self, city, key):
        self._enter_query(city, key)
        return self._get_results()

    def _enter_query(self, city, key):
        sleep(1)
        self._driver.get(url=self._url)
        search_input = self._driver.find_element_by_name('q')
        search_input.send_keys('{} {} adres'.format(city, key))
        search_input.send_keys(Keys.ENTER)

    def _get_results(self):
        return self._get_single_result() if self._is_single_result() else self._get_multiple_results()

    @except_to_bool(exc=Exception)
    def _is_single_result(self):
        self._driver.find_element_by_class_name('LrzXr')

    def _get_single_result(self):
        name_output = self._driver.find_element_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/span')
        address_output = self._driver.find_element_by_class_name('LrzXr')
        return [name_output.text + '\n' + self._format_address(address_output.text) + '\n']

    def _get_multiple_results(self):
        results = []

        # try:
        try:
            map_link_xpath = '//*[@id="rso"]/div[1]/div/div/div[2]/div/div[4]/div[1]/div[1]/div/div/a[1]/div/div/span'
            self._wait_for_visibility_by_xpath(map_link_xpath, timeout=0.1)
            map_link = self._driver.find_element_by_xpath(map_link_xpath)
            map_link.click()
        except TimeoutException:
            map_link_xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[1]/div[1]/div/div/a[1]/div/div/span'
            self._wait_for_visibility_by_xpath(map_link_xpath, timeout=0.1)
            map_link = self._driver.find_element_by_xpath(map_link_xpath)
            map_link.click()

        i = 0
        while True:
            i += 1
            # try:
            details_link_xpath = '//*[@id="rl_ist0"]/div[1]/div[4]/div[{}]/div/div[2]/div/a[1]/div/span'.format(i)
            sleep(1)
            # self._wait_for_visibility_by_xpath(details_link_xpath, timeout=0.1)
            details_link = self._driver.find_element_by_xpath(details_link_xpath)
            details_link.click()

            name_output_xpath = '//*[@id="akp_tsuid8"]/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div/span'
            # self._wait_for_visibility_by_xpath(name_output_xpath, timeout=0.1)
            name_output = self._driver.find_element_by_xpath(name_output_xpath)

            address_output_xpath = '//*[@id="akp_tsuid8"]/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div/span[2]'
            # self._wait_for_visibility_by_xpath(address_output_xpath, timeout=0.1)
            address_output = self._driver.find_element_by_xpath(address_output_xpath)

            results.append(name_output.text + '\n' + self._format_address(address_output.text) + '\n')
            # except (TimeoutException, NoSuchElementException):
            #     break
        # except Exception:
        #     pass

        return results

    # def _get_one_of_multiple_results(self, xpath):
    #     name_output = self._driver.find_element_by_xpath(xpath)
    #     name = name_output.text
    #     name_output.click()
    #     sleep(1)
    #     address_output = self._wait_for_element_by_class_name('LrzXr')
    #     address = self._format_address(address_output.text)
    #     return name, address

    @staticmethod
    def _format_address(address):
        return address.replace(', ', '\n')
