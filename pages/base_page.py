import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу по URL")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Найти элемент")
    def find_element(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Кликнуть по элементу")
    def click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    @allure.step("Получить текст элемента")
    def get_text(self, locator):
        return self.find_element(locator).text