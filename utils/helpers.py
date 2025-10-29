import random
import string

def generate_post_code() -> str:
    """Генерирует случайный Post Code из 10 цифр."""
    return "".join(random.choices(string.digits, k=10))

def generate_first_name_from_post_code(post_code: str) -> str:
    """
    Генерирует First Name на основе Post Code по заданной логике.
    Пример: "0001252667" -> "abzap"
    """
    first_name = ""
    alphabet = string.ascii_lowercase
    # Разбиваем Post Code на пары цифр
    for i in range(0, len(post_code), 2):
        part = post_code[i:i+2]
        number = int(part)
        # Находим индекс буквы в алфавите
        char_index = number % 26
        first_name += alphabet[char_index]
    return first_name

def find_customer_to_delete(names: list[str]) -> str:
    """
    Находит имя клиента, длина которого наиболее близка к среднему арифметическому
    длин всех имен в списке.
    """
    if not names:
        raise ValueError("Список имен не может быть пустым")
        
    lengths = [len(name) for name in names]
    avg_length = sum(lengths) / len(lengths)
    
    # Находим имя с минимальной разницей в длине от среднего
    closest_name = min(names, key=lambda name: abs(len(name) - avg_length))
    return closest_name
