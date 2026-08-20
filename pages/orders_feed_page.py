from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class OrdersFeedPage(BasePage):

    ORDERS_FEED_TITLE = (
        By.XPATH,
        "//h1[contains(text(), 'Лента заказов')]"
    )

    ORDERS_TOTAL = (
        By.XPATH,
        "//div[p[contains(text(), 'Выполнено за все время')]]"
        "//p[contains(@class, 'OrderFeed_number')]"
    )

    ORDERS_TODAY = (
        By.XPATH,
        "//div[p[contains(text(), 'Выполнено за сегодня')]]"
        "//p[contains(@class, 'OrderFeed_number')]"
    )

    ORDERS_IN_WORK = (
        By.XPATH,
        "//div[contains(@class, 'OrderFeed_orderStatusBox')]"
        "//p[contains(text(), 'В работе')]/following-sibling::ul[1]/li"
    )

    def is_orders_feed_opened(self):
        return self.find_element(
            self.ORDERS_FEED_TITLE
        ).is_displayed()

    def get_total_orders(self):
        return int(
            self.get_text(self.ORDERS_TOTAL)
        )

    def get_today_orders(self):
        return int(
            self.get_text(self.ORDERS_TODAY)
        )

    def get_orders_in_work(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(
                self.ORDERS_IN_WORK
            )
        )

        return [
            order.text.strip()
            for order in self.driver.find_elements(
                *self.ORDERS_IN_WORK
            )
            if order.text.strip()
        ]

    def wait_for_total_orders_increase(self, old_total):
        WebDriverWait(self.driver, 90).until(
            lambda driver: self.get_total_orders() > old_total
        )
        return self.get_total_orders()

    def wait_for_today_orders_increase(self, old_today):
        WebDriverWait(self.driver, 90).until(
            lambda driver: self.get_today_orders() > old_today
        )
        return self.get_today_orders()

    def wait_for_new_order_in_work(self, old_orders):
        def new_order_appeared(driver):
            current_orders = self.get_orders_in_work()
            return any(order not in old_orders for order in current_orders)

        WebDriverWait(self.driver, 90).until(new_order_appeared)

        current_orders = self.get_orders_in_work()
        return next(order for order in current_orders if order not in old_orders)

    def is_order_in_work(self, order_number):
        order_number = str(order_number).strip()

        orders = self.get_orders_in_work()

        return order_number in orders