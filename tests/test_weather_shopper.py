
import pytest
import time
from pages.home_page import HomePage
from pages.moisturizers_page import MoisturizersPage
from pages.sunscreens_page import SunscreensPage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage

# Constantes pour les conditions de température
TEMP_THRESHOLD_MOISTURIZER = 19
TEMP_THRESHOLD_SUNSCREEN = 34

# Constantes pour les identifiants de produits
MOISTURIZER_TYPE_1 = "Aloe"
MOISTURIZER_TYPE_2 = "Almond"
SUNSCREEN_TYPE_1 = "SPF-30"
SUNSCREEN_TYPE_2 = "SPF-50"

# Constantes pour les détails de paiement Stripe (Test)
STRIPE_EMAIL = "test@example.com"
STRIPE_CARD_NUMBER = "4242424242424242" 
STRIPE_EXPIRY = "12/25" 
STRIPE_CVC = "123"
STRIPE_ZIP = "12345"


@pytest.mark.weather_shop
class TestWeatherShopper:

    def test_complete_purchase_flow(self, driver):
        """
        Teste le parcours utilisateur complet :
        1. Lire la température.
        2. Aller à la page produit appropriée.
        3. Sélectionner les deux produits les moins chers selon les critères.
        4. Ajouter au panier.
        5. Vérifier le panier (2 articles, total correct).
        6. Procéder au paiement et vérifier le succès.
        """
        home_page = HomePage(driver)
        home_page.open()

        temperature = home_page.get_temperature()
        print(f"Current temperature: {temperature}°C")

        product_page = None
        price1 = 0
        price2 = 0

        if temperature < TEMP_THRESHOLD_MOISTURIZER:
            print("Temperature < 19°C. Buying moisturizers.")
            home_page.go_to_moisturizers()
            product_page = MoisturizersPage(driver)
            print(f"Adding cheapest '{MOISTURIZER_TYPE_1}' moisturizer...")
            price1 = product_page.add_cheapest_product_containing(MOISTURIZER_TYPE_1)
            print(f"Price of {MOISTURIZER_TYPE_1}: {price1}")
            time.sleep(1)
            print(f"Adding cheapest '{MOISTURIZER_TYPE_2}' moisturizer...")
            price2 = product_page.add_cheapest_product_containing(MOISTURIZER_TYPE_2)
            print(f"Price of {MOISTURIZER_TYPE_2}: {price2}")

        elif temperature > TEMP_THRESHOLD_SUNSCREEN:
            print("Temperature > 34°C. Buying sunscreens.")
            home_page.go_to_sunscreens()
            product_page = SunscreensPage(driver)
            print(f"Adding cheapest '{SUNSCREEN_TYPE_1}' sunscreen...")
            price1 = product_page.add_cheapest_product_containing(SUNSCREEN_TYPE_1)
            print(f"Price of {SUNSCREEN_TYPE_1}: {price1}")
            time.sleep(1)
            print(f"Adding cheapest '{SUNSCREEN_TYPE_2}' sunscreen...")
            price2 = product_page.add_cheapest_product_containing(SUNSCREEN_TYPE_2)
            print(f"Price of {SUNSCREEN_TYPE_2}: {price2}")
        else:
            print(f"Temperature ({temperature}°C) is between 19°C and 34°C. No action required.")
            pytest.skip("Temperature is within normal range, test scenario for shopping skipped.")
            return # pour sortir du test

        # --- Aller au panier et vérifier ---
        print("Going to cart...")
        product_page.go_to_cart()
        cart_page = CartPage(driver)

        expected_item_count = 2
        actual_item_count = cart_page.get_item_count()
        print(f"Expected item count: {expected_item_count}, Actual: {actual_item_count}")
        assert actual_item_count == expected_item_count, \
            f"Cart should have {expected_item_count} items, but found {actual_item_count}"

        expected_total_price = price1 + price2
        actual_total_price = cart_page.get_total_price()
        print(f"Expected total price: {expected_total_price}, Actual: {actual_total_price}")
        assert actual_total_price == expected_total_price, \
            f"Cart total price should be {expected_total_price}, but found {actual_total_price}"

        time.sleep(1) 

        # --- Procéder au paiement ---
        print("Proceeding to payment...")
        cart_page.click_pay_with_card()
        
        payment_page = PaymentPage(driver)
       
        payment_page.switch_to_stripe_iframe()

        # Remplir les détails de paiement
        payment_page.fill_payment_details(
            STRIPE_EMAIL,
            STRIPE_CARD_NUMBER,
            STRIPE_EXPIRY,
            STRIPE_CVC,
            STRIPE_ZIP
        )
        time.sleep(1) # Pause
        
        # Soumettre le paiement
        payment_page.submit_payment_in_iframe()

        # Quitter l'iframe pour vérifier le message de succès sur la page principale
        payment_page.switch_back_from_iframe()
        
        # Vérifier le message de succès
        assert payment_page.is_payment_successful(), "Payment success message was not found."

        print("Test Weather Shopper: Purchase flow completed successfully!")
