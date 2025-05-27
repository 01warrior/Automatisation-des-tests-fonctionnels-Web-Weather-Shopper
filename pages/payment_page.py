from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class PaymentPage(BasePage):
    # Locator pour l'IFRAME PRINCIPALE de Stripe
    STRIPE_IFRAME_MAIN = (By.XPATH, "//iframe[@name='stripe_checkout_app']") # Basé sur l'inspection du site

    # --- Champs DANS l'iframe PRINCIPALE ---
    EMAIL_INPUT = (By.ID, "email")
    CARD_NUMBER_INPUT = (By.ID, "card_number")
    EXPIRY_DATE_INPUT = (By.ID, "cc-exp")          
    CVC_INPUT = (By.ID, "cc-csc")         
    ZIP_CODE_INPUT_MAIN_IFRAME = (By.ID, "billing-zip")

    # Bouton de soumission DANS l'iframe PRINCIPALE
    SUBMIT_BUTTON_IFRAME = (By.ID, "submitButton")

    # Message de succès HORS de toute iframe
    PAYMENT_SUCCESS_MESSAGE_HEADER = (By.XPATH, "//h2[contains(text(), 'PAYMENT SUCCESS')]")

    def __init__(self, driver):
        super().__init__(driver, base_url=driver.current_url)

    def switch_to_stripe_iframe(self):
        """Bascule vers l'iframe principale de paiement Stripe."""

        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.STRIPE_IFRAME_MAIN))
        print(f"Switched to MAIN Stripe iframe: {self.STRIPE_IFRAME_MAIN}")

    def switch_back_from_iframe(self):
        """Bascule hors de toute iframe vers le contenu principal."""
        self._switch_to_default_content()

    def fill_payment_details(self, email, card_number, expiry_date, cvc, zip_code="12345"): # zip_code n'est pas utilisé ici
        """Remplit les détails de paiement dans le formulaire Stripe."""
        print("Filling payment details...")

        self._type(self.EMAIL_INPUT, email)
        print(f"Filled email: {email}")

        self._type(self.CARD_NUMBER_INPUT, card_number)
        print(f"Filled card number")

        self._type(self.EXPIRY_DATE_INPUT, expiry_date)
        print(f"Filled expiry date")

        self._type(self.CVC_INPUT, cvc)
        print(f"Filled CVC")

        self._type(self.ZIP_CODE_INPUT_MAIN_IFRAME, zip_code)
        print(f"Filled ZIP Code: {zip_code}")

    def submit_payment_in_iframe(self):
        """Clique sur le bouton de soumission DANS l'iframe PRINCIPALE Stripe."""
        self._click(self.SUBMIT_BUTTON_IFRAME)
        print("Payment submitted.")

    def is_payment_successful(self, timeout=20) -> bool:
        """Vérifie si le message de succès du paiement est affiché (HORS iframe)."""
        print("Checking for payment success message...")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.PAYMENT_SUCCESS_MESSAGE_HEADER)
            )
            print("Payment success message found.")
            return True
        except TimeoutException:
            print(f"Timeout: Payment success message not found within {timeout}s.")
            print(f"Current URL: {self.driver.current_url}")
            return False