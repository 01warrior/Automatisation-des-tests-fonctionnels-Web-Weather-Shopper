# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session") # ou scope="function" si tu préfères
def driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("detach", True)

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver_instance = webdriver.Chrome(service=service, options=chrome_options)

    yield driver_instance

    # Optionnel: Ferme le driver seulement si 'detach' n'est pas activé
    should_quit = True
    if chrome_options.experimental_options and \
       chrome_options.experimental_options.get("detach"):
        should_quit = False
    
    if should_quit:
        driver_instance.quit()