import allure

from pages.login_page import LoginPage
from data import EMAIL, PASSWORD


class TestLogin:

    @allure.title("Вход в аккаунт")
    def test_login(self, driver):
        page = LoginPage(driver)

        page.login_from_main_page(
            EMAIL,
            PASSWORD
        )

        page.open_personal_account()

        assert page.is_logout_button_visible()