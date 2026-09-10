import pytest
from selenium import webdriver

from data import EMAIL, PASSWORD
from pages.login_page import LoginPage

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Firefox()

    browser.maximize_window()

    yield browser

    browser.quit()

@pytest.fixture
def login(driver):
    login_page = LoginPage(driver)
    login_page.login_from_main_page(EMAIL, PASSWORD)
    yield login_page