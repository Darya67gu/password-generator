"""
Тесты валидации для генератора паролей.
Проверяем поведение функций при граничных и некорректных входных данных.
"""
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем тестируемые функции из корня программы
from password_manager import generate_single_password, generate_passwords


def test_validation_min_length():
    """Валидация: минимальная длина пароля (1 символ)"""
    password = generate_single_password(length=1, use_lower=True, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    assert len(password) == 1, f"Ожидалась длина 1, получена {len(password)}"
    print("✓ Тест пройден: пароль из 1 символа создан")


def test_validation_max_length():
    """Валидация: максимальная длина пароля (из GUI - 32, тестируем 128)"""
    password = generate_single_password(length=128, use_lower=True, 
                                        use_upper=True, use_digits=True, 
                                        use_symbols=True)
    assert len(password) == 128, f"Ожидалась длина 128, получена {len(password)}"
    print("✓ Тест пройден: пароль из 128 символов создан")


def test_validation_zero_length():
    """Валидация: нулевая длина пароля"""
    password = generate_single_password(length=0, use_lower=True, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    assert len(password) == 0, f"Ожидалась длина 0, получена {len(password)}"
    assert password == "", "Пароль нулевой длины должен быть пустой строкой"
    print("✓ Тест пройден: пароль нулевой длины - пустая строка")


def test_validation_negative_length():
    """Валидация: отрицательная длина пароля"""
    try:
        password = generate_single_password(length=-5, use_lower=True, 
                                            use_upper=False, use_digits=False, 
                                            use_symbols=False)
        # Если функция не выбросила исключение, проверяем что вернулось
        print(f"! Функция не выбросила исключение при длине -5, вернула: '{password}'")
        assert isinstance(password, str), "Результат должен быть строкой"
        print("✓ Тест пройден: отрицательная длина обработана без краха")
    except Exception as e:
        print(f"✓ Тест пройден: отрицательная длина вызвала исключение: {type(e).__name__}: {e}")


def test_validation_zero_count():
    """Валидация: нулевое количество паролей"""
    passwords = generate_passwords(count=0, length=10, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=False)
    assert isinstance(passwords, list), "Результат должен быть списком"
    assert len(passwords) == 0, f"Ожидался пустой список, получено {len(passwords)} элементов"
    print("✓ Тест пройден: 0 паролей - пустой список")


def test_validation_negative_count():
    """Валидация: отрицательное количество паролей"""
    try:
        passwords = generate_passwords(count=-3, length=10, use_lower=True, 
                                       use_upper=True, use_digits=True, 
                                       use_symbols=False)
        print(f"! Функция не выбросила исключение при count=-3, вернула список из {len(passwords)} элементов")
        assert isinstance(passwords, list), "Результат должен быть списком"
        print("✓ Тест пройден: отрицательное количество обработано без краха")
    except Exception as e:
        print(f"✓ Тест пройден: отрицательное количество вызвало исключение: {type(e).__name__}: {e}")


def test_validation_large_count():
    """Валидация: большое количество паролей (1000)"""
    passwords = generate_passwords(count=1000, length=8, use_lower=True, 
                                   use_upper=False, use_digits=False, 
                                   use_symbols=False)
    assert len(passwords) == 1000, f"Ожидалось 1000 паролей, получено {len(passwords)}"
    assert all(isinstance(p, str) for p in passwords), "Все элементы должны быть строками"
    assert all(len(p) == 8 for p in passwords), "Все пароли должны иметь длину 8"
    print("✓ Тест пройден: сгенерировано 1000 паролей")


def test_validation_mixed_chars_present():
    """Валидация: при включении всех наборов символов они присутствуют в пароле (вероятностный тест)"""
    password = generate_single_password(length=100, use_lower=True, 
                                        use_upper=True, use_digits=True, 
                                        use_symbols=True)
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    symbols_set = set("!@#$%^&*()_+-=[]{}|;:,.<>?/~`")
    has_symbol = any(c in symbols_set for c in password)
    
    assert has_lower, "В пароле должны быть строчные буквы"
    assert has_upper, "В пароле должны быть заглавные буквы"
    assert has_digit, "В пароле должны быть цифры"
    assert has_symbol, "В пароле должны быть спецсимволы"
    print("✓ Тест пройден: все типы символов присутствуют в длинном пароле")


def test_validation_no_unwanted_chars():
    """Валидация: в пароле отсутствуют символы из невыбранных наборов"""
    password = generate_single_password(length=50, use_lower=True, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    
    assert not any(c.isupper() for c in password), "Не должно быть заглавных букв"
    assert not any(c.isdigit() for c in password), "Не должно быть цифр"
    
    symbols_set = set("!@#$%^&*()_+-=[]{}|;:,.<>?/~`")
    assert not any(c in symbols_set for c in password), "Не должно быть спецсимволов"
    print("✓ Тест пройден: невыбранные типы символов отсутствуют")


def test_validation_password_not_empty_with_chars():
    """Валидация: пароль не пустой если выбран хотя бы один набор символов"""
    password = generate_single_password(length=10, use_lower=True, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    assert len(password) > 0, "Пароль не должен быть пустым"
    assert password.strip() != "", "Пароль не должен состоять из пробелов"
    print("✓ Тест пройден: пароль не пустой")


def test_validation_return_type_consistency():
    """Валидация: функция всегда возвращает строку при любых валидных параметрах"""
    test_cases = [
        (8, True, False, False, False),
        (12, True, True, False, False),
        (16, True, True, True, False),
        (20, True, True, True, True),
        (6, False, True, False, False),
        (10, False, False, True, False),
        (14, False, False, False, True),
        (1, True, False, False, False),
        (32, True, True, True, True),
    ]
    
    for length, lower, upper, digits, symbols in test_cases:
        password = generate_single_password(length, lower, upper, digits, symbols)
        assert isinstance(password, str), f"Ожидалась строка для параметров: {length}, {lower}, {upper}, {digits}, {symbols}"
    
    print(f"✓ Тест пройден: консистентность типа возврата для {len(test_cases)} комбинаций параметров")


def test_validation_list_return_type():
    """Валидация: функция generate_passwords всегда возвращает список"""
    test_cases = [
        (1, 10, True, False, False, False),
        (5, 12, True, True, False, False),
        (10, 16, True, True, True, False),
        (3, 20, True, True, True, True),
        (0, 8, True, False, False, False),
    ]
    
    for count, length, lower, upper, digits, symbols in test_cases:
        passwords = generate_passwords(count, length, lower, upper, digits, symbols)
        assert isinstance(passwords, list), f"Ожидался список для параметров: {count}, {length}, {lower}, {upper}, {digits}, {symbols}"
    
    print(f"✓ Тест пройден: консистентность возврата списка для {len(test_cases)} комбинаций")


def test_validation_single_password_vs_list():
    """Валидация: одиночный пароль через generate_passwords(count=1) совпадает по формату с generate_single_password"""
    single = generate_single_password(length=10, use_lower=True, 
                                      use_upper=True, use_digits=True, 
                                      use_symbols=True)
    
    list_result = generate_passwords(count=1, length=10, use_lower=True, 
                                     use_upper=True, use_digits=True, 
                                     use_symbols=True)
    
    assert isinstance(list_result, list), "Результат должен быть списком"
    assert len(list_result) == 1, "В списке должен быть 1 пароль"
    assert isinstance(list_result[0], str), "Элемент списка должен быть строкой"
    assert len(list_result[0]) == 10, "Длина пароля должна быть 10"
    print("✓ Тест пройден: одиночный пароль через список корректен")


def run_all_validation_tests():
    """Запуск всех тестов валидации"""
    print("=" * 50)
    print("ЗАПУСК ТЕСТОВ ВАЛИДАЦИИ ГЕНЕРАТОРА ПАРОЛЕЙ")
    print("=" * 50)
    
    tests = [
        test_validation_min_length,
        test_validation_max_length,
        test_validation_zero_length,
        test_validation_negative_length,
        test_validation_zero_count,
        test_validation_negative_count,
        test_validation_large_count,
        test_validation_mixed_chars_present,
        test_validation_no_unwanted_chars,
        test_validation_password_not_empty_with_chars,
        test_validation_return_type_consistency,
        test_validation_list_return_type,
        test_validation_single_password_vs_list,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Тест НЕ пройден: {test.__doc__}")
            print(f"  Причина: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Тест НЕ пройден: {test.__doc__}")
            print(f"  Ошибка: {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"РЕЗУЛЬТАТЫ: пройдено {passed}/{len(tests)}, провалено {failed}/{len(tests)}")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_validation_tests()
    sys.exit(0 if success else 1)