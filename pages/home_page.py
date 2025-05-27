import re
from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    # Locators
    TEMPERATURE_TEXT = (By.ID, "temperature")
    MOISTURIZERS_BUTTON = (By.XPATH, "//button[contains(text(), 'Buy moisturizers')]")
    SUNSCREENS_BUTTON = (By.XPATH, "//button[contains(text(), 'Buy sunscreens')]")

    def __init__(self, driver):
        super().__init__(driver) # le constructeur de BasePage

    def open(self):
        """Ouvre la page d'accueil."""
        self._visit()

    def get_temperature(self) -> int:
        """Récupère la température actuelle affichée et la retourne en entier."""
        temp_text = self._get_text(self.TEMPERATURE_TEXT)
        # Utilise une expression régulière pour extraire le nombre
        match = re.search(r"(\d+)", temp_text)
        if match:
            return int(match.group(1))
        raise ValueError(f"Could not parse temperature from text: '{temp_text}'")

    def go_to_moisturizers(self):
        """Clique sur le bouton pour aller à la page des hydratants."""
        self._click(self.MOISTURIZERS_BUTTON)


    def go_to_sunscreens(self):
        """Clique sur le bouton pour aller à la page des écrans solaires."""
        self._click(self.SUNSCREENS_BUTTON)
       