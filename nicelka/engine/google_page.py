from time import sleep

from exceptbool import except_to_bool
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
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
        self._enter_query(city, key)
        return self._get_results()

    def _enter_query(self, city, key):
        Logger.debug(self, "Searching for city: '{}' key: '{}'".format(city, key))
        sleep(1.2)

        try:
            self._driver.get(url=self._url)
            search_input = self._find_element_by_name('q')
            search_input.send_keys('{} {} adres'.format(city, key))
            search_input.send_keys(Keys.ENTER)
        except NoSuchElementException as e:
            Logger.error(self, e, self._enter_query.__name__)
            raise GooglePageException('Failed to enter query')

    def _get_results(self):
        if self._is_single_result():
            return self._get_single_result()
        elif self._are_multiple_results():
            return self._get_multiple_results()
        else:
            return []

    @except_to_bool(exc=TimeoutException)
    def _is_single_result(self):
        self._wait_for_element_by_class_name('LrzXr', timeout=2)

    @except_to_bool(exc=TimeoutException)
    def _are_multiple_results(self):
        self._wait_for_element_by_xpath('//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[1]/div/div/a[1]/div/div/span', timeout=2)

    def _get_single_result(self):
        Logger.debug(self, 'Getting single result...')
        result = []

        try:
            name_output_xpath = '//div[@class="SPZz6b"]//span'
            self._wait_for_element_by_xpath(name_output_xpath, timeout=2)
            name_output = self._find_element_by_xpath(name_output_xpath)
            name = name_output.text

            address_output_class = 'LrzXr'
            self._wait_for_element_by_class_name(address_output_class, timeout=2)
            address_output = self._find_element_by_class_name(address_output_class)
            address = address_output.text

            result.append(name + '\n' + self._format_address(address) + '\n')
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            Logger.error(self, e, self._get_single_result.__name__)
            raise GooglePageException('Failed to get single result')

        return result

    def _get_multiple_results(self):
        Logger.debug(self, 'Getting multiple results...')
        results = []

        name_1_xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[1]/div/div/a[1]/div/div/span'
        address_1_xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[1]/div/div/a[1]/div/span/div[2]/span/span'

        name_2_xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/a[1]/div/div/span'
        address_2_xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/a[1]/div/span/div[2]/span/span'

        name_3_xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[3]/div[2]/div/a[1]/div/div/span'
        address_3_xpath = '//*[@id="rso"]/div[2]/div/div/div[2]/div/div[4]/div[3]/div[2]/div/a[1]/div/span/div[2]/span/span'

        xpaths = ((name_1_xpath, address_1_xpath),
                  (name_2_xpath, address_2_xpath),
                  (name_3_xpath, address_3_xpath))

        for name_xpath, address_xpath in xpaths:
            try:
                name, address = self._get_one_of_multiple_results(name_xpath, address_xpath)
                results.append(name + '\n' + self._format_address(address) + '\n')
            except GooglePageException as e:
                Logger.error(self, e, self._get_multiple_results.__name__)

        return results

    def _get_one_of_multiple_results(self, name_xpath, address_xpath):
        try:
            self._wait_for_element_by_xpath(name_xpath, timeout=2)
            name_output = self._find_element_by_xpath(name_xpath)
            name = name_output.text

            self._wait_for_element_by_xpath(address_xpath, timeout=1)
            address_output = self._find_element_by_xpath(address_xpath)
            address = address_output.text
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            Logger.error(self, e, self._get_one_of_multiple_results.__name__)
            raise GooglePageException('Failed to get one of multiple results')

        return name, address

    @staticmethod
    def _format_address(address):
        return address.replace(', ', '\n')
