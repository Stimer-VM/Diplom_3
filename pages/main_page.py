import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
from urls import BASE_URL


class MainPage(BasePage):

    CONSTRUCTOR = (
        By.XPATH,
        "//p[text()='Конструктор']"
    )

    ORDERS_FEED = (
        By.XPATH,
        "//p[text()='Лента Заказов']"
    )

    FIRST_INGREDIENT = (
        By.XPATH,
        "(//a[contains(@href, '/ingredient/')])[1]"
    )

    MODAL = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]"
    )

    MODAL_CLOSE = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]//button"
    )

    INGREDIENT_COUNTER = (
        By.XPATH,
        "(//a[contains(@href, '/ingredient/')])[1]"
        "//parent::div//p[contains(@class, 'counter_counter')]"
    )

    CONSTRUCTOR_INGREDIENT = (
        By.XPATH,
        "//section[contains(@class, 'BurgerConstructor_basket')]"
        "//li[contains(@class, 'BurgerConstructor')]"
    )

    ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Оформить заказ')]"
    )

    ORDER_NUMBER = (
        By.XPATH,
        "//h2[contains(@class, 'text_type_digits-large')]"
    )

    ORDER_MODAL_CLOSE = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal') and "
        ".//h2[contains(@class, 'text_type_digits-large')]]"
        "//button[contains(@class, 'Modal_modal__close')]"
    )

    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        self.open(BASE_URL)

    @allure.step("Закрыть модальное окно, если оно есть")
    def close_modal_if_present(self):
        try:
            close_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.MODAL_CLOSE)
            )
            close_button.click()

            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.MODAL)
            )
        except Exception:
            pass

    @allure.step("Кликнуть по «Конструктор»")
    def click_constructor(self):
        self.close_modal_if_present()

        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]"))
        )

        self.click(self.CONSTRUCTOR)

    @allure.step("Кликнуть по «Лента заказов»")
    def click_orders_feed(self):
        self.close_modal_if_present()

        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]"))
        )

        self.click(self.ORDERS_FEED)

    @allure.step("Кликнуть по первому ингредиенту")
    def click_first_ingredient(self):
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]"))
        )
        self.close_modal_if_present()
        self.click(self.FIRST_INGREDIENT)

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        self.click(self.MODAL_CLOSE)
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]"))
        )

    @allure.step("Проверить видимость модального окна")
    def is_modal_visible(self):
        try:
            return self.driver.find_element(
                *self.MODAL
            ).is_displayed()
        except Exception:
            return False

    @allure.step("Получить счётчик ингредиента")
    def get_ingredient_counter(self):
        return self.get_text(self.INGREDIENT_COUNTER)

    @allure.step("Добавить первый ингредиент в заказ")
    def add_first_ingredient_to_order(self):
        ingredient = self.find_element(
            self.FIRST_INGREDIENT
        )

        order_area = self.find_element(
            (
                By.XPATH,
                "//section[contains(@class, 'BurgerConstructor_basket')]"
            )
        )

        ActionChains(self.driver).drag_and_drop(
            ingredient,
            order_area
        ).perform()

    @allure.step("Проверить видимость ингредиента в заказе")
    def is_ingredient_in_order(self):
        try:
            return self.driver.find_element(
                *self.CONSTRUCTOR_INGREDIENT
            ).is_displayed()
        except Exception:
            return False

    @allure.step("Кликнуть по кнопке «Оформить заказ»")
    def click_order_button(self):
        self.click(self.ORDER_BUTTON)

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        order_number = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                self.ORDER_NUMBER
            )
        )

        return order_number.text

    @allure.step("Создать заказ")
    def create_order(self):
        self.add_first_ingredient_to_order()
        self.click_order_button()

        return self.get_order_number()

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        close_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ORDER_MODAL_CLOSE)
        )
        self.driver.execute_script("arguments[0].click();", close_button)

        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Modal_modal')]"))
        )
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]"))
        )

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url