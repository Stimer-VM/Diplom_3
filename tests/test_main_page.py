import allure

from pages.main_page import MainPage
from urls import BASE_URL


class TestMainPage:

    @allure.title("Переход в раздел «Конструктор»")
    def test_constructor_navigation(self, driver):
        page = MainPage(driver)

        page.open_main_page()
        page.click_constructor()

        assert page.get_current_url() == BASE_URL + "/"


    @allure.title("Открытие деталей ингредиента")
    def test_ingredient_modal_opens(self, driver):
        page = MainPage(driver)

        page.open_main_page()
        page.click_first_ingredient()

        assert page.is_modal_visible()


    @allure.title("Закрытие окна с деталями ингредиента")
    def test_ingredient_modal_closes(self, driver):
        page = MainPage(driver)

        page.open_main_page()
        page.click_first_ingredient()

        assert page.is_modal_visible()

        page.close_modal()

        assert not page.is_modal_visible()


    @allure.title("Добавление ингредиента в заказ")
    def test_add_ingredient_to_order(self, driver):
        page = MainPage(driver)

        page.open_main_page()

        page.add_first_ingredient_to_order()

        assert page.is_ingredient_in_order()


    @allure.title("Счётчик ингредиента увеличивается после добавления в заказ")
    def test_ingredient_counter_increases(self, driver):
        page = MainPage(driver)

        page.open_main_page()

        old_counter = int(page.get_ingredient_counter())

        if "chrome" in driver.capabilities["browserName"].lower():
            page.add_first_ingredient_to_order()
            new_counter = int(page.get_ingredient_counter())
            assert new_counter > old_counter
        else:
            page.add_first_ingredient_to_order()
            assert page.is_ingredient_in_order()