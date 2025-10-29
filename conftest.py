import pytest
from selenium import webdriver
from pages.manager_page import ManagerPage

@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации и закрытия драйвера браузера.
    Scope='function' означает, что новый браузер будет запускаться для каждого теста.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def manager_page(driver):
    """
    Фикстура для инициализации страницы менеджера и открытия URL.
    """
    url = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager"
    page = ManagerPage(driver)
    page.open(url)
    return page
