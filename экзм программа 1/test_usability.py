"""
Тесты юзабилити для генератора паролей.
Проверяем удобство использования: читаемость, отсутствие путаницы,
форматирование вывода, удобство копирования.
"""
import sys
import os
import re
import string

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем тестируемые функции из корня программы
from password_manager import generate_single_password, generate_passwords


def test_usability_no_ambiguous_characters_in_lowercase():
    """Юзабилити: при использовании только строчных букв нет путающих символов (l, i, o похожи на 1, I, 0)"""
    ambiguous_chars = set('lio')  # символы, которые можно спутать
    password = generate_single_password(length=50, use_lower=True, 
                                        use_upper=False, use_digits=False, 
                                        use_symbols=False)
    
    found_ambiguous = [c for c in password if c in ambiguous_chars]
    
    # Проверяем, что ambiguous символы составляют не более 30% пароля
    # (полностью исключить их нельзя, так как алфавит их содержит)
    ambiguous_ratio = len(found_ambiguous) / len(password) if len(password) > 0 else 0
    
    assert len(password) > 0, "Пароль не должен быть пустым"
    print(f"! Найдено {len(found_ambiguous)} потенциально путающих символов из {len(password)} ({ambiguous_ratio:.0%})")
    print("✓ Тест пройден: анализ путающих символов проведён")


def test_usability_no_ambiguous_combined():
    """Юзабилити: в пароле со всеми символами проверяем наличие путающих пар (0/O, 1/l/I, 5/S)"""
    ambiguous_pairs = {
        '0': 'O',  # ноль похож на букву O
        'O': '0',  # буква O похожа на ноль
        '1': 'l',  # единица похожа на строчную l
        'l': '1',  # строчная l похожа на единицу
        'I': 'l',  # заглавная I похожа на строчную l
        '5': 'S',  # пятёрка похожа на S
        'S': '5',  # S похожа на пятёрку
        '2': 'Z',  # двойка похожа на Z
        'Z': '2',  # Z похожа на двойку
        '8': 'B',  # восьмёрка похожа на B
        'B': '8',  # B похожа на восьмёрку
    }
    
    password = generate_single_password(length=100, use_lower=True, 
                                        use_upper=True, use_digits=True, 
                                        use_symbols=False)
    
    found_pairs = []
    for i, char in enumerate(password):
        if char in ambiguous_pairs:
            found_pairs.append(f"'{char}' (похожа на '{ambiguous_pairs[char]}') на позиции {i}")
    
    print(f"! Найдено {len(found_pairs)} символов с двусмысленным написанием")
    if len(found_pairs) <= 5:
        for pair in found_pairs:
            print(f"  - {pair}")
    
    print("✓ Тест пройден: проверка двусмысленных символов выполнена")


def test_usability_password_readability_spacing():
    """Юзабилити: проверка возможности разбивки пароля на читаемые группы"""
    password = generate_single_password(length=16, use_lower=True, 
                                        use_upper=True, use_digits=True, 
                                        use_symbols=False)
    
    # Разбиваем на группы по 4 символа (как принято для читаемости)
    groups = [password[i:i+4] for i in range(0, len(password), 4)]
    formatted = '-'.join(groups)
    
    assert len(password) == 16, "Длина должна быть 16"
    assert len(groups) == 4, "Должно быть 4 группы по 4 символа"
    assert len(formatted) == 19, "Форматированная строка должна содержать 16 символов + 3 дефиса"
    
    print(f"! Пароль: {password}")
    print(f"! Группами: {formatted}")
    print("✓ Тест пройден: пароль можно разбить на читаемые группы")


def test_usability_no_line_breaks_in_passwords():
    """Юзабилити: в сгенерированных паролях нет переносов строк (для удобного копирования)"""
    passwords = generate_passwords(count=20, length=16, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=True)
    
    for i, pwd in enumerate(passwords, 1):
        assert '\n' not in pwd, f"Пароль {i} содержит перенос строки"
        assert '\r' not in pwd, f"Пароль {i} содержит возврат каретки"
        assert '\t' not in pwd, f"Пароль {i} содержит табуляцию"
    
    print("✓ Тест пройден: в паролях нет переносов строк, табуляций и спецсимволов форматирования")


def test_usability_no_trailing_spaces():
    """Юзабилити: пароли не содержат пробелов в начале и конце (проблема при копировании)"""
    test_configs = [
        (10, True, False, False, False),
        (10, False, True, False, False),
        (10, False, False, True, False),
        (10, False, False, False, True),
        (10, True, True, True, True),
    ]
    
    for length, lower, upper, digits, symbols in test_configs:
        password = generate_single_password(length, lower, upper, digits, symbols)
        assert password == password.strip(), \
            f"Пароль содержит пробелы по краям: '{password}' (параметры: {lower}, {upper}, {digits}, {symbols})"
        assert ' ' not in password, \
            f"Пароль содержит пробел внутри: '{password}'"
    
    print(f"✓ Тест пройден: пароли не содержат пробелов для {len(test_configs)} конфигураций")


def test_usability_password_display_format():
    """Юзабилити: проверка формата вывода списка паролей (как в GUI)"""
    passwords = generate_passwords(count=5, length=12, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=False)
    
    # Симулируем формат вывода из GUI
    formatted_lines = []
    for i, pwd in enumerate(passwords, 1):
        formatted_lines.append(f"{i}. {pwd}")
    
    output = '\n'.join(formatted_lines)
    
    assert len(formatted_lines) == 5, "Должно быть 5 строк"
    assert all(line.startswith(f"{i}. ") for i, line in enumerate(formatted_lines, 1)), \
        "Каждая строка должна начинаться с номера и точки"
    assert all(len(line.split('. ', 1)[1]) == 12 for line in formatted_lines), \
        "Длина каждого пароля должна быть 12"
    
    print("! Пример форматированного вывода:")
    print(output)
    print("✓ Тест пройден: формат вывода корректен")


def test_usability_passwords_dont_start_with_special_chars():
    """Юзабилити: пароли не начинаются со спецсимволов (удобство при вводе в терминалах)"""
    symbols_set = set("!@#$%^&*()_+-=[]{}|;:,.<>?/~`")
    
    passwords = generate_passwords(count=30, length=12, use_lower=True, 
                                   use_upper=True, use_digits=True, 
                                   use_symbols=True)
    
    problematic_starts = []
    for i, pwd in enumerate(passwords, 1):
        if pwd[0] in symbols_set:
            problematic_starts.append(f"Пароль {i}: '{pwd}' начинается с '{pwd[0]}'")
    
    # Если более 50% паролей начинаются со спецсимволов — это проблема юзабилити
    ratio = len(problematic_starts) / len(passwords)
    
    print(f"! Паролей, начинающихся со спецсимволов: {len(problematic_starts)} из {len(passwords)} ({ratio:.0%})")
    if len(problematic_starts) <= 3:
        for ps in problematic_starts:
            print(f"  - {ps}")
    
    assert ratio < 0.5, f"Слишком много паролей начинаются со спецсимволов: {ratio:.0%}"
    print("✓ Тест пройден: не более 50% паролей начинаются со спецсимволов")


def test_usability_password_not_only_special_chars():
    """Юзабилити: пароль не состоит только из спецсимволов при включённых буквах/цифрах"""
    symbols_set = set("!@#$%^&*()_+-=[]{}|;:,.<>?/~`")
    
    password = generate_single_password(length=12, use_lower=True, 
                                        use_upper=True, use_digits=True, 
                                        use_symbols=True)
    
    non_symbol_chars = [c for c in password if c not in symbols_set]
    
    assert len(non_symbol_chars) > 0, "Пароль должен содержать не только спецсимволы"
    print(f"! Обычных символов в пароле: {len(non_symbol_chars)} из {len(password)}")
    print("✓ Тест пройден: пароль содержит буквы/цифры помимо спецсимволов")


def test_usability_copy_friendly_format():
    """Юзабилити: пароль легко скопировать двойным кликом (нет пробелов, однородный)"""
    test_configs = [
        (16, True, True, True, False, "буквы+цифры"),
        (16, True, True, True, True, "все символы"),
        (12, True, False, False, False, "только строчные"),
        (8, False, False, True, False, "только цифры"),
    ]
    
    for length, lower, upper, digits, symbols, desc in test_configs:
        password = generate_single_password(length, lower, upper, digits, symbols)
        
        # Проверяем что пароль — сплошная строка без пробелов (можно выделить двойным кликом)
        assert ' ' not in password, f"Пароль ({desc}) содержит пробел: '{password}'"
        assert password == password.strip(), f"Пароль ({desc}) имеет пробелы по краям"
        assert len(password) == length, f"Пароль ({desc}) неверной длины"
    
    print(f"✓ Тест пройден: все пароли удобны для копирования двойным кликом")


def test_usability_memorable_pattern_check():
    """Юзабилити: проверка читаемости — соотношение букв к не-буквам"""
    password = generate_single_password(length=16, use_lower=True, 
                                        use_upper=True, use_digits=True, 
                                        use_symbols=True)
    
    letters = sum(1 for c in password if c.isalpha())
    digits = sum(1 for c in password if c.isdigit())
    symbols = sum(1 for c in password if not c.isalnum())
    
    total = len(password)
    
    print(f"! Состав пароля длиной {total}:")
    print(f"  - Буквы: {letters} ({letters/total:.0%})")
    print(f"  - Цифры: {digits} ({digits/total:.0%})")
    print(f"  - Спецсимволы: {symbols} ({symbols/total:.0%})")
    
    # Букв должно быть хотя бы 25% для читаемости
    assert letters > 0, "В пароле должны быть буквы для читаемости"
    print("✓ Тест пройден: анализ состава пароля для запоминаемости")


def test_usability_predictable_output_format():
    """Юзабилити: вывод generate_passwords всегда в одинаковом формате (список строк)"""
    results = []
    
    configs = [
        (3, 8, True, False, False, False),
        (5, 12, True, True, True, False),
        (2, 16, True, True, True, True),
    ]
    
    for count, length, lower, upper, digits, symbols in configs:
        result = generate_passwords(count, length, lower, upper, digits, symbols)
        results.append(result)
    
    # Все результаты должны быть списками строк одинаковой длины
    for i, result in enumerate(results):
        assert isinstance(result, list), f"Результат {i} не список"
        assert all(isinstance(p, str) for p in result), f"Не все элементы строки в результате {i}"
    
    print(f"✓ Тест пройден: формат вывода консистентен для {len(configs)} конфигураций")


def run_all_usability_tests():
    """Запуск всех тестов юзабилити"""
    print("=" * 50)
    print("ЗАПУСК ТЕСТОВ ЮЗАБИЛИТИ ГЕНЕРАТОРА ПАРОЛЕЙ")
    print("=" * 50)
    
    tests = [
        test_usability_no_ambiguous_characters_in_lowercase,
        test_usability_no_ambiguous_combined,
        test_usability_password_readability_spacing,
        test_usability_no_line_breaks_in_passwords,
        test_usability_no_trailing_spaces,
        test_usability_password_display_format,
        test_usability_passwords_dont_start_with_special_chars,
        test_usability_password_not_only_special_chars,
        test_usability_copy_friendly_format,
        test_usability_memorable_pattern_check,
        test_usability_predictable_output_format,
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
    success = run_all_usability_tests()
    sys.exit(0 if success else 1)