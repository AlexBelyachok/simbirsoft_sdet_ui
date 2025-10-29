from pages.manager_page import ManagerPage
from utils.helpers import (
    generate_post_code,
    generate_first_name_from_post_code,
)

class TestBanking:
    """Класс с тестами для банковского проекта."""

    def test_add_customer(self, manager_page: ManagerPage):
        """Тест-кейс 1: Создание клиента."""
        # 1. Подготовка данных
        last_name = "Granger" # Фамилия для примера
        post_code = generate_post_code()
        first_name = generate_first_name_from_post_code(post_code)
        
        # 2. Создание клиента
        manager_page.go_to_add_customer_tab()
        manager_page.add_new_customer(first_name, last_name, post_code)
        
        # 3. Проверка
        manager_page.go_to_customers_tab()
        manager_page.search_customer(first_name)
        customers = manager_page.get_customers_data()
        
        assert len(customers) == 1, f"Клиент {first_name} не найден или найдено больше одного"
        
        new_customer = customers[0]
        assert new_customer["first_name"] == first_name
        assert new_customer["last_name"] == last_name
        assert new_customer["post_code"] == post_code
