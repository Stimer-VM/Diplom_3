import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from urls import BASE_URL


class LoginPage(BasePage):

    LOGIN_BUTTON_MAIN = (
        By.XPATH,
        "//button[contains(., 'Войти в аккаунт')]"
    )

    EMAIL_INPUT = (
        By.XPATH,
        "//label[contains(text(), 'Email')]/parent::div//input"
    )

    PASSWORD_INPUT = (
        By.XPATH,
        "//label[contains(text(), 'Пароль')]/parent::div//input"
    )

    LOGIN_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Войти')]"
    )

    PERSONAL_ACCOUNT_BUTTON = (
        By.XPATH,
        "//a[contains(@href, '/account')]"
    )

    LOGOUT_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Выход')]"
    )

    MODAL_OVERLAY = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal_overlay')]"
    )

    MODAL_CLOSE_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'Modal_modal__close')]"
    )

    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        self.open(BASE_URL)

    @allure.step("Кликнуть по кнопке «Войти в аккаунт»")
    def click_login_from_main(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.LOGIN_BUTTON_MAIN
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

    @allure.step("Ввести email")
    def enter_email(self, email):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.EMAIL_INPUT
            )
        ).send_keys(email)

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.PASSWORD_INPUT
            )
        ).send_keys(password)

    @allure.step("Кликнуть по кнопке «Войти»")
    def click_login(self):
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(self.MODAL_OVERLAY)
        )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.LOGIN_BUTTON
            )
        ).click()

    @allure.step("Войти в аккаунт")
    def login_from_main_page(self, email, password):
        self.open_main_page()
        self.click_login_from_main()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    @allure.step("Закрыть модальное окно, если оно есть")
    def close_modal_if_present(self):
        try:
            close_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    self.MODAL_CLOSE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                close_button
            )

            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(
                    self.MODAL_OVERLAY
                )
            )

        except Exception:
            pass

    @allure.step("Открыть личный кабинет")
    def open_personal_account(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.PERSONAL_ACCOUNT_BUTTON
            )
        )

        self.close_modal_if_present()

        account_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.PERSONAL_ACCOUNT_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            account_button
        )

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/account")
        )

    @allure.step("Проверить видимость кнопки «Выход»")
    def is_logout_button_visible(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.LOGOUT_BUTTON
            )
        ).is_displayed()