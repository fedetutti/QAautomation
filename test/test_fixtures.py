import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def aceptar_cookies(driver):
    try:
        boton_aceptar = driver.find_element(By.XPATH, '//*[@id="L2AGLb"]/div')
        boton_aceptar.click()
    except:
        pass

@pytest.fixture(params=["Playwright", "Selenium", "Cypress"])
def termino_de_busqueda(request):
    return request.param

@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Evita que navigator.webdriver sea true
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    driver.get("https://www.google.com")
    aceptar_cookies(driver)
    yield driver
    driver.quit()

def test_google_busqueda(browser, termino_de_busqueda):
    search_box = browser.find_element("name", "q")
    search_box.send_keys(termino_de_busqueda + Keys.RETURN)

    results = browser.find_element("id", "search")
    assert (
        len(results.find_elements("xpath", ".//div")) > 0
    ), "Hay resultados de búsqueda"
