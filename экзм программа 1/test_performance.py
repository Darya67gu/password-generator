"""
Тесты производительности для генератора паролей.
Замеряем скорость работы и потребление памяти при разных нагрузках.
"""
import sys
import os
import time
import tracemalloc
import gc

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем тестируемые функции из корня программы
from password_manager import generate_single_password, generate_passwords


def measure_performance(func, *args, **kwargs):
    """Замеряет время выполнения и потребление памяти для функции"""
    # Очищаем память перед замером
    gc.collect()
    
    # Запускаем трейсер памяти
    tracemalloc.start()
    
    # Замер времени
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    
    # Замер памяти
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time = end_time - start_time
    memory_current_kb = current / 1024  # Переводим в КБ
    memory_peak_kb = peak / 1024
    
    return {
        'result': result,
        'time_sec': execution_time,
        'memory_current_kb': memory_current_kb,
        'memory_peak_kb': memory_peak_kb,
    }


def format_time(seconds):
    """Форматирует время в читаемый вид"""
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} мкс"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} мс"
    else:
        return f"{seconds:.4f} с"


def test_performance_single_password_lengths():
    """Производительность: генерация одного пароля разной длины"""
    print("\n" + "=" * 70)
    print("ТЕСТ 1: ОДИН ПАРОЛЬ — РАЗНАЯ ДЛИНА")
    print("=" * 70)
    print(f"{'Длина':<10} {'Время':<15} {'Память (тек.)':<15} {'Память (пик.)':<15}")
    print("-" * 55)
    
    lengths = [6, 8, 10, 16, 32, 64, 128, 256, 512, 1024]
    
    for length in lengths:
        metrics = measure_performance(
            generate_single_password, length, 
            True, True, True, True
        )
        
        print(f"{length:<10} {format_time(metrics['time_sec']):<15} "
              f"{metrics['memory_current_kb']:.2f} КБ{'':<8} "
              f"{metrics['memory_peak_kb']:.2f} КБ")
    
    print("✓ Замеры для разной длины пароля выполнены")


def test_performance_multiple_passwords_count():
    """Производительность: генерация разного количества паролей"""
    print("\n" + "=" * 70)
    print("ТЕСТ 2: РАЗНОЕ КОЛИЧЕСТВО ПАРОЛЕЙ (длина 16)")
    print("=" * 70)
    print(f"{'Кол-во':<10} {'Время':<15} {'Память (тек.)':<15} {'Память (пик.)':<15}")
    print("-" * 55)
    
    counts = [1, 5, 10, 50, 100, 500, 1000, 5000, 10000]
    
    for count in counts:
        metrics = measure_performance(
            generate_passwords, count, 16, 
            True, True, True, True
        )
        
        print(f"{count:<10} {format_time(metrics['time_sec']):<15} "
              f"{metrics['memory_current_kb']:.2f} КБ{'':<8} "
              f"{metrics['memory_peak_kb']:.2f} КБ")
    
    print("✓ Замеры для разного количества паролей выполнены")


def test_performance_different_symbol_sets():
    """Производительность: разные комбинации наборов символов"""
    print("\n" + "=" * 70)
    print("ТЕСТ 3: РАЗНЫЕ НАБОРЫ СИМВОЛОВ (1000 паролей × длина 16)")
    print("=" * 70)
    print(f"{'Наборы':<20} {'Время':<15} {'Память (тек.)':<15} {'Память (пик.)':<15}")
    print("-" * 55)
    
    configs = [
        ("только строчные", True, False, False, False),
        ("только заглавные", False, True, False, False),
        ("только цифры", False, False, True, False),
        ("только спецсимволы", False, False, False, True),
        ("строчные+заглавные", True, True, False, False),
        ("строчные+цифры", True, False, True, False),
        ("буквы+цифры", True, True, True, False),
        ("все наборы", True, True, True, True),
    ]
    
    for desc, lower, upper, digits, symbols in configs:
        metrics = measure_performance(
            generate_passwords, 1000, 16, 
            lower, upper, digits, symbols
        )
        
        print(f"{desc:<20} {format_time(metrics['time_sec']):<15} "
              f"{metrics['memory_current_kb']:.2f} КБ{'':<8} "
              f"{metrics['memory_peak_kb']:.2f} КБ")
    
    print("✓ Замеры для разных наборов символов выполнены")


def test_performance_stress_test():
    """Производительность: стресс-тест на больших объёмах"""
    print("\n" + "=" * 70)
    print("ТЕСТ 4: СТРЕСС-ТЕСТ — БОЛЬШИЕ ОБЪЁМЫ")
    print("=" * 70)
    print(f"{'Нагрузка':<25} {'Время':<15} {'Память (тек.)':<15} {'Память (пик.)':<15}")
    print("-" * 55)
    
    stress_configs = [
        ("10 000 × длина 8", 10000, 8, True, True, True, False),
        ("10 000 × длина 32", 10000, 32, True, True, True, True),
        ("50 000 × длина 8", 50000, 8, True, True, True, False),
        ("100 000 × длина 6", 100000, 6, True, False, False, False),
    ]
    
    for desc, count, length, lower, upper, digits, symbols in stress_configs:
        metrics = measure_performance(
            generate_passwords, count, length, 
            lower, upper, digits, symbols
        )
        
        print(f"{desc:<25} {format_time(metrics['time_sec']):<15} "
              f"{metrics['memory_current_kb']:.2f} КБ{'':<8} "
              f"{metrics['memory_peak_kb']:.2f} КБ")
    
    print("✓ Стресс-тест выполнен")


def test_performance_memory_growth():
    """Производительность: рост потребления памяти при увеличении нагрузки"""
    print("\n" + "=" * 70)
    print("ТЕСТ 5: АНАЛИЗ РОСТА ПАМЯТИ (разная длина × 1000 паролей)")
    print("=" * 70)
    print(f"{'Длина':<10} {'Память (пик.)':<15} {'Память на 1 пароль':<20} {'Рост':<10}")
    print("-" * 55)
    
    lengths = [6, 8, 10, 16, 32, 64, 128, 256]
    previous_memory = None
    
    for length in lengths:
        metrics = measure_performance(
            generate_passwords, 1000, length, 
            True, True, True, True
        )
        
        memory_per_password = metrics['memory_peak_kb'] / 1000
        
        if previous_memory:
            growth = f"×{metrics['memory_peak_kb'] / previous_memory:.2f}"
        else:
            growth = "—"
        
        print(f"{length:<10} {metrics['memory_peak_kb']:.2f} КБ{'':<8} "
              f"{memory_per_password:.3f} КБ{'':<12} {growth:<10}")
        
        previous_memory = metrics['memory_peak_kb']
    
    print("✓ Анализ роста памяти выполнен")


def test_performance_list_vs_single():
    """Производительность: сравнение generate_passwords(1) и generate_single_password"""
    print("\n" + "=" * 70)
    print("ТЕСТ 6: СРАВНЕНИЕ ОДИНОЧНОЙ И СПИСКОВОЙ ГЕНЕРАЦИИ")
    print("=" * 70)
    
    # Прогрев
    for _ in range(100):
        generate_single_password(16, True, True, True, True)
        generate_passwords(1, 16, True, True, True, True)
    
    # Замер single
    iterations = 10000
    start = time.perf_counter()
    for _ in range(iterations):
        generate_single_password(16, True, True, True, True)
    single_time = (time.perf_counter() - start) / iterations
    
    # Замер list
    start = time.perf_counter()
    for _ in range(iterations):
        generate_passwords(1, 16, True, True, True, True)
    list_time = (time.perf_counter() - start) / iterations
    
    print(f"{'Функция':<30} {'Среднее время':<20}")
    print("-" * 50)
    print(f"{'generate_single_password':<30} {format_time(single_time):<20}")
    print(f"{'generate_passwords(1)':<30} {format_time(list_time):<20}")
    
    if list_time > 0:
        overhead = ((list_time - single_time) / single_time) * 100
        print(f"\n! Накладные расходы списковой функции: {overhead:.1f}%")
    
    print("✓ Сравнение выполнено")


def run_all_performance_tests():
    """Запуск всех тестов производительности"""
    print("=" * 70)
    print("ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ ГЕНЕРАТОРА ПАРОЛЕЙ")
    print("=" * 70)
    
    tests = [
        test_performance_single_password_lengths,
        test_performance_multiple_passwords_count,
        test_performance_different_symbol_sets,
        test_performance_stress_test,
        test_performance_memory_growth,
        test_performance_list_vs_single,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"\n✗ Ошибка в тесте: {type(e).__name__}: {e}")
    
    print("\n" + "=" * 70)
    print("ВСЕ ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ ЗАВЕРШЕНЫ")
    print("=" * 70)


if __name__ == "__main__":
    run_all_performance_tests()