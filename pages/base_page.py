from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        """Открывает страницу по URL."""
        self.driver.get(url)

    def find_element(self, locator, time=10):
        """Находит один элемент, ожидая его появления."""
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент по локатору {locator}"
        )
    
    def find_elements(self, locator, time=10):
        """Находит все элементы, подходящие под локатор."""
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти элементы по локатору {locator}"
        )
    
    def click(self, locator, time=10):
        """Ожидает кликабельности элемента и кликает по нему."""
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент не кликабелен по локатору {locator}"
        )
        element.click()

    def send_keys(self, locator, text, time=10):
        """Находит элемент и вводит в него текст."""
        element = self.find_element(locator, time)
        element.clear()
        element.send_keys(text)
