from selenium.webdriver.common.by import By
from .moisturizers_page import MoisturizersPage # pour utiliser héritage de MoisturizersPage car la structure est la même

class SunscreensPage(MoisturizersPage): # Hérite de MoisturizersPage
    PAGE_TITLE = (By.XPATH, "//h2[contains(text(),'Sunscreens')]")

    def __init__(self, driver):
        super().__init__(driver)
        print("On Sunscreens Page")