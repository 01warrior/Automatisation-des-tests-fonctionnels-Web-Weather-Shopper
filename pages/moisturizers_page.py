import re
from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class MoisturizersPage(BasePage):
    # Locators
    PAGE_TITLE = (By.XPATH, "//h2[contains(text(),'Moisturizers')]") # Pour vérifier qu'on est sur la bonne page
    PRODUCT_CONTAINERS = (By.XPATH, "//div[contains(@class, 'text-center col-4')]")
    
    # Les locators suivants sont relatifs à un PRODUCT_CONTAINER
    PRODUCT_NAME_RELATIVE = (By.XPATH, ".//p[contains(@class, 'font-weight-bold')]")
    PRODUCT_PRICE_RELATIVE = (By.XPATH, ".//p[not(contains(@class, 'font-weight-bold')) and contains(text(), 'Price')]")
    ADD_BUTTON_RELATIVE = (By.XPATH, ".//button[text()='Add']")
    CART_BUTTON = (By.ID, "cart")

    def __init__(self, driver):
        super().__init__(driver, base_url=driver.current_url) 

    def _parse_price(self, price_text: str) -> int:
        """Extrait le prix numérique du texte (ex: "Price: Rs. 520" -> 520)."""
        match = re.search(r"(\d+)", price_text)
        if match:
            return int(match.group(1))
        raise ValueError(f"Could not parse price from text: '{price_text}'")

    def add_cheapest_product_containing(self, text_identifier: str) -> int:
        """
        Trouve le produit le moins cher contenant 'text_identifier' dans son nom,
        l'ajoute au panier et retourne son prix.
        """
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_CONTAINERS)) # S'assurer que les produits sont chargés
        all_products = self.driver.find_elements(*self.PRODUCT_CONTAINERS) # Notez le '*' pour déballer le tuple
        
        cheapest_product_info = None
        min_price = float('inf')

        print(f"Searching for cheapest product containing '{text_identifier}'...")

        for product_element in all_products:
            try:
                
                name_element = product_element.find_element(*self.PRODUCT_NAME_RELATIVE)
                product_name = name_element.text.lower() 

                if text_identifier.lower() in product_name:
                    price_element = product_element.find_element(*self.PRODUCT_PRICE_RELATIVE)
                    price = self._parse_price(price_element.text)
                    
                    print(f"  Found: '{product_name}', Price: {price}")

                    if price < min_price:
                        min_price = price
                        add_button = product_element.find_element(*self.ADD_BUTTON_RELATIVE)
                        cheapest_product_info = {
                            "name": product_name,
                            "price": price,
                            "button_element": add_button
                        }
            except Exception as e:
                print(f"  Error processing a product element: {e}")

                continue


        if cheapest_product_info:
            print(f"Adding cheapest '{text_identifier}' product to cart: {cheapest_product_info['name']} (Price: {cheapest_product_info['price']})")
            cheapest_product_info["button_element"].click()
            return cheapest_product_info["price"]
        else:
            raise Exception(f"No product found containing '{text_identifier}'")

    def go_to_cart(self):
        """Clique sur le bouton du panier."""
        self._click(self.CART_BUTTON)