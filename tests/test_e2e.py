import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:8000"
# O JS tem setTimeout de 1500ms; 8 segundos cobrem a latência do servidor também
TIMEOUT = 8


@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.binary_location = "/usr/bin/google-chrome"

    chrome = webdriver.Chrome(options=opts)
    chrome.implicitly_wait(2)
    yield chrome
    chrome.quit()


class TestE2ECompra:
    def test_compra_aprovada_exibe_mensagem(self, driver):
        driver.get(BASE_URL)

        driver.find_element(By.ID, "input-produto").send_keys("teclado")
        driver.find_element(By.ID, "input-cartao").send_keys("1234 5678 9012 3456")
        driver.find_element(By.ID, "btn-comprar").click()

        mensagem = WebDriverWait(driver, TIMEOUT).until(
            EC.text_to_be_present_in_element((By.ID, "mensagem"), "Compra aprovada")
        )
        assert mensagem

        texto = driver.find_element(By.ID, "mensagem").text
        assert "Compra aprovada" in texto

    def test_produto_inexistente_exibe_erro(self, driver):
        driver.get(BASE_URL)

        driver.find_element(By.ID, "input-produto").send_keys("produto_invalido_xyz")
        driver.find_element(By.ID, "input-cartao").send_keys("1234 5678 9012 3456")
        driver.find_element(By.ID, "btn-comprar").click()

        # Aguarda o elemento não estar mais em "Processando..."
        WebDriverWait(driver, TIMEOUT).until(
            EC.text_to_be_present_in_element((By.ID, "mensagem"), "Erro")
        )

        texto = driver.find_element(By.ID, "mensagem").text
        assert "Erro" in texto
