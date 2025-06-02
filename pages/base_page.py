import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver: WebDriver, base_url="https://weathershopper.pythonanywhere.com/"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10) 

    def _visit(self, url_path=""):
        """Navigue vers une URL (base_url + url_path)"""
        full_url = self.base_url + url_path
        print(f"Visiting: {full_url}")
        self.driver.get(full_url)

    def _find(self, locator):
        """Trouve un élément en utilisant un locator (tuple: By, 'valeur')"""
        print(f"Finding element: {locator}")
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Timeout: Element not visible or not found: {locator}")
            raise # la on Relance l'exception pour que le test échoue clairement

    def _click(self, locator):
        """Clique sur un élément"""
        print(f"Clicking element: {locator}")
        self._find(locator).click()

    def _type(self, locator, text):
        print(f"Typing '{text}' into element: {locator}")
        element = self._find(locator)
        element.click() 
        element.clear()

        for character in text:
            element.send_keys(character)
            time.sleep(0.1)

    def _get_text(self, locator):
        """Récupère le texte d'un élément"""
        text = self._find(locator).text
        return text

    def _is_displayed(self, locator):
        """Vérifie si un élément est affiché"""
        try:
            return self._find(locator).is_displayed()
        except TimeoutException:
            return False

    def _wait_for_text_in_element(self, locator, text_to_find, timeout=10):
        """Attend que le texte spécifié apparaisse dans un élément."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text_to_find)
            )
            return True
        except TimeoutException:
            print(f"Timeout: Text '{text_to_find}' not found in element {locator} within {timeout}s")
            return False

    def _switch_to_iframe(self, iframe_locator, timeout=10):
        """Bascule vers une iframe."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(iframe_locator)
            )
            print(f"Switched to iframe: {iframe_locator}")
        except TimeoutException:
            print(f"Timeout: Iframe {iframe_locator} not found or could not be switched to.")
            raise

    def _switch_to_default_content(self):
        """Bascule hors de l'iframe vers le contenu principal de la page."""
        self.driver.switch_to.default_content()
        print("Switched back to default content.")
