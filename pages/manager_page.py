from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from .base_page import BasePage

class ManagerPage(BasePage):
    """
    Класс, описывающий страницу менеджера и ее элементы.
    """
    # --- Локаторы ---
    ADD_CUSTOMER_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='addCust()']")
    CUSTOMERS_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='showCust()']")
    
    # Форма "Add Customer"
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='fName']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='lName']")
    POST_CODE_INPUT = (By.CSS_SELECTOR, "input[ng-model='postCd']")
    ADD_CUSTOMER_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Таблица "Customers"
    CUSTOMER_SEARCH_INPUT = (By.CSS_SELECTOR, "input[ng-model='searchCustomer']")
    FIRST_NAME_HEADER = (By.XPATH, "//thead/tr/td[1]/a")
    TABLE_ROWS = (By.XPATH, "//tbody/tr")
    
    def go_to_add_customer_tab(self):
        self.click(self.ADD_CUSTOMER_TAB_BUTTON)

    def go_to_customers_tab(self):
        self.click(self.CUSTOMERS_TAB_BUTTON)

    def add_new_customer(self, first_name, last_name, post_code):
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POST_CODE_INPUT, post_code)
        self.click(self.ADD_CUSTOMER_SUBMIT_BUTTON)
        self.accept_alert()

    def accept_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            print("Alert не был найден.")
            
    def get_customers_data(self) -> list[dict]:
        """Собирает данные всех видимых клиентов из таблицы."""
        rows = self.find_elements(self.TABLE_ROWS)
        customers = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                customers.append({
                    "first_name": cells[0].text,
                    "last_name": cells[1].text,
                    "post_code": cells[2].text,
                })
        return customers

    def sort_by_first_name(self):
        self.click(self.FIRST_NAME_HEADER)

    def search_customer(self, query):
        self.send_keys(self.CUSTOMER_SEARCH_INPUT, query)

    def delete_customer(self, first_name):
        delete_button_locator = (By.XPATH, f"//td[text()='{first_name}']/following-sibling::td/button")
        self.click(delete_button_locator)
