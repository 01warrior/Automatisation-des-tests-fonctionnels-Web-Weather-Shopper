import re
from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    # Locators
    PAGE_TITLE = (By.XPATH, "//h2[contains(text(),'Checkout')]") 
    TABLE_ROWS = (By.XPATH, "//table/tbody/tr") 
    TOTAL_PRICE_TEXT = (By.ID, "total")
    PAY_WITH_CARD_BUTTON = (By.XPATH, "//button/span[text()='Pay with Card']/parent::button")

    def __init__(self, driver):
        super().__init__(driver, base_url=driver.current_url)

    def get_item_count(self) -> int:
        """Retourne le nombre d'articles dans le panier."""
        self.wait.until(EC.visibility_of_element_located(self.TABLE_ROWS)) # Attendre que les lignes soient là
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        
        if len(rows) > 0 and "total" in rows[-1].find_element(By.XPATH, ".//td[1]").get_attribute("id"):
             return len(rows) -1 # Le nombre de lignes moins la ligne du total

        first_cell_text = ""
        if len(rows) > 0:
            try:
                first_cell_text = rows[0].find_element(By.XPATH, ".//td[1]").text.lower()
            except:
                pass 

        if "empty" in first_cell_text or len(rows) == 0:
            return 0
        
        return len(rows) 

    def get_total_price(self) -> int:
        """Retourne le montant total affiché dans le panier."""
        total_text = self._get_text(self.TOTAL_PRICE_TEXT)
        match = re.search(r"(\d+)", total_text)
        if match:
            return int(match.group(1))
        raise ValueError(f"Could not parse total price from text: '{total_text}'")

    def click_pay_with_card(self):
        """Clique sur le bouton 'Pay with Card'."""
        self._click(self.PAY_WITH_CARD_BUTTON)