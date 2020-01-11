from time import sleep

from exceptbool import except_to_bool
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from nicelka.engine.engine import Engine


class WebPage(Engine):
    def __init__(self, executable_path):
        super(WebPage, self).__init__()
        self._url = None
        self._executable_path = executable_path
        self._driver = None

    def start(self):
        self._driver = Chrome(executable_path=self._executable_path)
        self._driver.maximize_window()
        if self._url is not None:
            self._driver.get(self._url)

    def stop(self):
        self._driver.close()
        self._driver = None

    def _wait_for_element_by_class_name(self, class_name):
        try:
            return self._driver.find_element_by_class_name(class_name)
        except NoSuchElementException:
            sleep(0.5)
            return self._driver.find_element_by_class_name(class_name)

    def _wait_for_element_by_xpath(self, xpath, timeout=5):
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def _wait_for_visibility_by_xpath(self, xpath, timeout=5):
        WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def _wait_for_clickability_by_xpath(self, xpath, timeout=5):
        WebDriverWait(self._driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    @except_to_bool(exc=(NoAlertPresentException, TimeoutException))
    def _is_alert_present(self, timeout=0.1):
        WebDriverWait(self._driver, timeout).until(EC.alert_is_present())

    def _back(self):
        self._driver.back()
        sleep(1)
