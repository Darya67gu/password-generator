"""
Тесты верификации для генератора паролей.
Проверяем, что основные функции работают корректно.
"""
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем тестируемые функции из корня программы (password_manager.py)
from password_manager import generate_single_password, generate_passwords


def test_verify_password_length():
    """Верификация: пароль имеет правильную длину"""
    password = generate_single_password(length=10, use_lower=True, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    assert len(password) == 10, f"Ожидалась длина 10, получена {len(password)}"
    print("✓ Тест пройден: длина пароля корректна")


def test_verify_password_string_type():
    """Верификация: результат генерации - строка"""
    password = generate_single_password(length=8, use_lower=True, 
                                        use_upper=True, use_digits=True, 
                                        use_symbols=False)
    assert isinstance(password, str), f"Ожидался тип str, получен {type(password)}"
    print("✓ Тест пройден: тип результата - строка")


def test_verify_empty_chars_fallback():
    """Верификация: если ничего не выбрано, используются строчные буквы"""
    password = generate_single_password(length=12, use_lower=False, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    assert len(password) == 12, "Пароль должен быть сгенерирован"
    assert all(c.islower() for c in password), "Все символы должны быть строчными буквами"
    print("✓ Тест пройден: при отсутствии выбора используются строчные буквы")


def test_verify_only_lowercase():
    """Верификация: только строчные буквы"""
    password = generate_single_password(length=15, use_lower=True, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    assert all(c.islower() for c in password), "Все символы должны быть строчными буквами"
    print("✓ Тест пройден: только строчные буквы")


def test_verify_only_uppercase():
    """Верификация: только заглавные буквы"""
    password = generate_single_password(length=15, use_lower=False, 
                                        use_upper=True, use_digits=False, 
                                        use_symbols=False)
    assert all(c.isupper() for c in password), "Все символы должны быть заглавными буквами"
    print("✓ Тест пройден: только заглавные буквы")


def test_verify_only_digits():
    """Верификация: только цифры"""
    password = generate_single_password(length=15, use_lower=False, 
                                        use_upper=False, use_digits=True, 
                                        use_symbols=False)
    assert all(c.isdigit() for c in password), "Все символы должны быть цифрами"
    print("✓ Тест пройден: только цифры")


def test_verify_only_symbols():
    """Верификация: только спецсимволы"""
    symbols_set = set("!@#$%^&*()_+-=[]{}|;:,.<>?/~`")
    password = generate_single_password(length=15, use_lower=False, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=True)
    assert all(c in symbols_set for c in password), "Все символы должны быть спецсимволами"
    print("✓ Тест пройден: только спецсимволы")


def test_verify_multiple_passwords_count():
    """Верификация: генерация списка паролей - правильное количество"""
    passwords = generate_passwords(count=5, length=10, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=False)
    assert len(passwords) == 5, f"Ожидалось 5 паролей, получено {len(passwords)}"
    print("✓ Тест пройден: количество паролей в списке корректно")


def test_verify_multiple_passwords_all_strings():
    """Верификация: все элементы списка - строки"""
    passwords = generate_passwords(count=3, length=8, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=True)
    assert all(isinstance(p, str) for p in passwords), "Все пароли должны быть строками"
    print("✓ Тест пройден: все пароли в списке - строки")


def test_verify_multiple_passwords_lengths():
    """Верификация: все пароли в списке имеют правильную длину"""
    passwords = generate_passwords(count=10, length=16, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=True)
    assert all(len(p) == 16 for p in passwords), "Все пароли должны иметь длину 16"
    print("✓ Тест пройден: все пароли имеют правильную длину")


def test_verify_no_duplicates_in_small_set():
    """Верификация: при малом количестве паролей они не повторяются (вероятностный тест)"""
    passwords = generate_passwords(count=5, length=8, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=True)
    assert len(set(passwords)) == len(passwords), "Обнаружены дубликаты паролей"
    print("✓ Тест пройден: дубликаты паролей не обнаружены")


def run_all_verification_tests():
    """Запуск всех тестов верификации"""
    print("=" * 50)
    print("ЗАПУСК ТЕСТОВ ВЕРИФИКАЦИИ ГЕНЕРАТОРА ПАРОЛЕЙ")
    print("=" * 50)
    
    tests = [
        test_verify_password_length,
        test_verify_password_string_type,
        test_verify_empty_chars_fallback,
        test_verify_only_lowercase,
        test_verify_only_uppercase,
        test_verify_only_digits,
        test_verify_only_symbols,
        test_verify_multiple_passwords_count,
        test_verify_multiple_passwords_all_strings,
        test_verify_multiple_passwords_lengths,
        test_verify_no_duplicates_in_small_set,
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
            print(f"  Ошибка: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"РЕЗУЛЬТАТЫ: пройдено {passed}/{len(tests)}, провалено {failed}/{len(tests)}")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_verification_tests()
    sys.exit(0 if success else 1)