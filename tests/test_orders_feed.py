import allure
import time

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.orders_feed_page import OrdersFeedPage
from data import EMAIL, PASSWORD


def login(driver):
    login_page = LoginPage(driver)
    login_page.login_from_main_page(EMAIL, PASSWORD)


@allure.title("Переход в раздел «Лента заказов»")
def test_orders_feed_navigation(driver):
    main_page = MainPage(driver)
    orders_feed_page = OrdersFeedPage(driver)

    main_page.open_main_page()
    main_page.click_orders_feed()

    assert orders_feed_page.is_orders_feed_opened()


@allure.title(
    "Счётчик «Выполнено за всё время» увеличивается "
    "после создания заказа"
)
def test_total_orders_counter_increases_after_order(driver):
    login(driver)

    main_page = MainPage(driver)
    orders_feed_page = OrdersFeedPage(driver)

    main_page.click_orders_feed()
    old_total = orders_feed_page.get_total_orders()

    main_page.click_constructor()
    main_page.create_order()
    main_page.close_order_modal()

    time.sleep(2)

    main_page.click_orders_feed()

    if "firefox" in driver.capabilities["browserName"].lower():
        driver.refresh()
        time.sleep(20)
        main_page.click_orders_feed()

    new_total = orders_feed_page.wait_for_total_orders_increase(old_total)
    assert new_total > old_total


@allure.title(
    "Счётчик «Выполнено за сегодня» увеличивается "
    "после создания заказа"
)
def test_today_orders_counter_increases_after_order(driver):
    login(driver)

    main_page = MainPage(driver)
    orders_feed_page = OrdersFeedPage(driver)

    main_page.click_orders_feed()
    old_today = orders_feed_page.get_today_orders()

    main_page.click_constructor()
    main_page.create_order()
    main_page.close_order_modal()

    time.sleep(2)

    main_page.click_orders_feed()

    if "firefox" in driver.capabilities["browserName"].lower():
        driver.refresh()
        time.sleep(20)
        main_page.click_orders_feed()

    new_today = orders_feed_page.wait_for_today_orders_increase(old_today)
    assert new_today > old_today


@allure.title(
    "После создания заказа его номер появляется "
    "в разделе «В работе»"
)
def test_created_order_appears_in_work(driver):
    login(driver)

    main_page = MainPage(driver)
    orders_feed_page = OrdersFeedPage(driver)

    main_page.click_orders_feed()
    old_orders = orders_feed_page.get_orders_in_work()

    main_page.click_constructor()
    main_page.create_order()
    main_page.close_order_modal()

    time.sleep(2)

    main_page.click_orders_feed()

    if "firefox" in driver.capabilities["browserName"].lower():
        driver.refresh()
        time.sleep(20)
        main_page.click_orders_feed()

    new_order = orders_feed_page.wait_for_new_order_in_work(old_orders)
    assert new_order not in old_orders