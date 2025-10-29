import allure
from pages.manager_page import ManagerPage
from utils.helpers import (
    generate_post_code,
    generate_first_name_from_post_code,
    find_customer_to_delete
)

@allure.feature("Функционал менеджера")
class TestBanking:
    """Класс с тестами для банковского проекта."""

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 1: Успешное создание нового клиента")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_customer(self, manager_page: ManagerPage):
        """Тест-кейс 1: Создание клиента."""
        with allure.step("1. Подготовка тестовых данных"):
            last_name = "Granger"
            post_code = generate_post_code()
            first_name = generate_first_name_from_post_code(post_code)
        
        with allure.step("2. Создание нового клиента через UI"):
            manager_page.go_to_add_customer_tab()
            manager_page.add_new_customer(first_name, last_name, post_code)
        
        with allure.step("3. Проверка, что клиент появился в таблице"):
            manager_page.go_to_customers_tab()
            manager_page.search_customer(first_name)
            customers = manager_page.get_customers_data()
            
            assert len(customers) == 1, f"Клиент {first_name} не найден или найдено больше одного"
            
            new_customer = customers[0]
            assert new_customer["first_name"] == first_name
            assert new_customer["last_name"] == last_name
            assert new_customer["post_code"] == post_code

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 2: Сортировка клиентов по имени")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_customers_by_first_name(self, manager_page: ManagerPage):
        """Тест-кейс 2: Сортировка клиентов по имени."""
        manager_page.go_to_customers_tab()
        
        with allure.step("1. Получение исходного списка имен"):
            initial_names = [c['first_name'] for c in manager_page.get_customers_data()]
        
        with allure.step("2. Сортировка по убыванию и проверка"):
            manager_page.sort_by_first_name()
            sorted_desc = [c['first_name'] for c in manager_page.get_customers_data()]
            assert sorted_desc == sorted(initial_names, reverse=True), "Сортировка по убыванию неверна"

        with allure.step("3. Сортировка по возрастанию и проверка"):
            manager_page.sort_by_first_name()
            sorted_asc = [c['first_name'] for c in manager_page.get_customers_data()]
            assert sorted_asc == sorted(initial_names), "Сортировка по возрастанию неверна"

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 3: Удаление клиента по заданной логике")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_customer(self, manager_page: ManagerPage):
        """Тест-кейс 3: Удаление клиента."""
        manager_page.go_to_customers_tab()
        
        with allure.step("1. Получение списка клиентов до удаления"):
            customers_before = manager_page.get_customers_data()
            assert len(customers_before) > 0, "Нет клиентов для выполнения теста на удаление"
            names_before = [c['first_name'] for c in customers_before]
        
        with allure.step("2. Определение клиента для удаления"):
            name_to_delete = find_customer_to_delete(names_before)
            allure.attach(f"Выбрано имя для удаления: {name_to_delete}", name="Имя для удаления")
        
        with allure.step("3. Удаление клиента"):
            manager_page.delete_customer(name_to_delete)
        
        with allure.step("4. Проверка, что клиент удален из списка"):
            customers_after = manager_page.get_customers_data()
            names_after = [c['first_name'] for c in customers_after]
            
            assert len(customers_after) == len(customers_before) - 1, "Количество клиентов не уменьшилось"
            assert name_to_delete not in names_after, f"Клиент {name_to_delete} не был удален"