import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from pages.manager_page import ManagerPage

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия драйвера браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def manager_page(driver):
    """Фикстура для инициализации страницы менеджера и открытия URL."""
    url = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager"
    page = ManagerPage(driver)
    page.open(url)
    return page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для добавления скриншота в Allure отчет при падении теста.
    """
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        if 'driver' in item.fixturenames:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=AttachmentType.PNG
            )