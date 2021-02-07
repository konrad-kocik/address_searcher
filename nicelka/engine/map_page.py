from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from nicelka.engine.web_page import WebPage
from nicelka.exceptions.exceptions import MapPageException
from nicelka.logger.logger import Logger


class MapPage(WebPage):
    def __init__(self, executable_path):
        super(MapPage, self).__init__(executable_path=executable_path)
        self._name = 'map_page'
        self._url = 'https://www.google.com/maps/dir///@51.1656864,16.8881249,14z/data=!4m2!4m1!3e0'

    def search(self, main_city, target_city):
        self._enter_query(main_city, target_city)
        return self._get_result()

    def _enter_query(self, main_city, target_city):
        Logger.debug(self, "Searching distance from main city: '{}' to target city: '{}'".format(
            main_city, target_city))
        sleep(2)

        try:
            from_input = self._find_element_by_xpath('//*[@id="sb_ifc50"]/input')
            from_input.clear()
            from_input.send_keys(main_city)
            to_input = self._find_element_by_xpath('//*[@id="sb_ifc51"]/input')
            to_input.clear()
            to_input.send_keys(target_city)
            to_input.send_keys(Keys.ENTER)
        except NoSuchElementException as e:
            Logger.error(self, e, self._enter_query.__name__)
            raise MapPageException('Failed to enter query')

    def _get_result(self):
        Logger.debug(self, 'Getting result...')
        sleep(2)

        try:
            distance_output_xpath = '//*[@id="section-directions-trip-0"]/div/div[1]/div[1]/div[2]/div'
            self._wait_for_element_by_xpath(distance_output_xpath, timeout=10)
            distance_output = self._find_element_by_xpath(distance_output_xpath)
            return distance_output.text.strip()
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException,
                StaleElementReferenceException) as e:
            Logger.error(self, e, self._get_result.__name__)
            raise MapPageException('Failed to get result')
