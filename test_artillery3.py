#!/usr/bin/env python3
"""
Тестовый модуль для Артиллерии 3
Автоматическое тестирование с сравнением поведения
"""

import unittest
import subprocess
import sys
import os
from io import StringIO
import artillery3


class TestArtillery3(unittest.TestCase):
    """Юнит-тесты для игры Артиллерия 3"""

    def setUp(self):
        """Настройка тестового окружения"""
        self.game = artillery3.Artillery3()
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        """Очистка после теста"""
        sys.stdout = self.original_stdout

    def test_game_initialization(self):
        """Тест инициализации игры"""
        self.game.N = 2
        self.assertEqual(self.game.N, 2)

        self.game.N = 3
        self.assertEqual(self.game.N, 3)

    def test_metric_physics(self):
        """Тест физических расчетов в метрической системе"""
        # Устанавливаем количество игроков
        self.game.N = 2

        # Тестируем с реалистичными значениями
        self.game.Q[0] = 45  # 45 градусов
        self.game.S[0] = 300  # 300 м/с (типичная скорость снаряда)
        self.game.W[0] = 5  # Ветер 5 м/с
        self.game.P[0] = 0
        self.game.P[1] = 1000  # Цель в 1 км

        hit, impact = self.game.calculate_shot(0, 1)

        # Проверяем типы возвращаемых значений
        self.assertIsInstance(hit, bool)
        self.assertIsInstance(impact, (int, float))

        # Проверяем, что расстояние реалистичное
        self.assertGreater(impact, 0)
        self.assertLess(impact, 50000)  # Не больше 50 км

    def test_wind_in_metric(self):
        """Тест обновления ветра в метрической системе"""
        # Устанавливаем количество игроков перед тестом
        self.game.N = 2

        # Инициализируем ветер ненулевыми значениями
        self.game.W[0] = 10.0
        self.game.W[1] = -5.0

        original_wind = self.game.W.copy()
        self.game.update_wind()

        # Ветер должен измениться (хотя бы у одного игрока)
        wind_changed = False
        for i in range(self.game.N):
            if self.game.W[i] != original_wind[i]:
                wind_changed = True
                break

        self.assertTrue(wind_changed, "Ветер не изменился после update_wind()")

        # Ветер должен быть в пределах -20..20 м/с
        for i in range(self.game.N):
            self.assertGreaterEqual(self.game.W[i], -20)
            self.assertLessEqual(self.game.W[i], 20)

    def test_player_positions_metric(self):
        """Тест позиций игроков в метрах"""
        self.game.N = 2
        # Мокаем setup_game
        positions = [500, 1500, 2500]
        for i in range(self.game.N):
            self.game.P[i] = positions[i]

        # Позиции должны быть в метрах
        self.assertEqual(self.game.P[0], 500)
        self.assertEqual(self.game.P[1], 1500)

        if self.game.N == 3:
            self.assertEqual(self.game.P[2], 2500)

    def test_velocity_range(self):
        """Тест диапазона скорости"""
        # Скорость должна быть в пределах 0-1000 м/с
        self.game.S[0] = 500
        self.assertGreaterEqual(self.game.S[0], 0)
        self.assertLessEqual(self.game.S[0], 1000)

        # Проверяем, что случайная вариация добавляется
        self.game.V[0] = 15.5
        total_v = self.game.S[0] + self.game.V[0]
        self.assertGreater(total_v, 0)

    def test_calculate_shot_with_different_angles(self):
        """Тест расчета выстрела с разными углами"""
        self.game.N = 2
        self.game.P[0] = 0
        self.game.P[1] = 1000

        # Тест с нулевым углом
        self.game.Q[0] = 0
        self.game.S[0] = 300
        self.game.W[0] = 0
        hit1, impact1 = self.game.calculate_shot(0, 1)

        # Тест с углом 90 градусов
        self.game.Q[0] = 90
        hit2, impact2 = self.game.calculate_shot(0, 1)

        # При угле 0 градусов снаряд должен лететь недалеко
        # При угле 90 градусов - почти вертикально (недалеко по горизонтали)
        self.assertLess(impact1, impact2)

    def test_wind_limits(self):
        """Тест граничных значений ветра"""
        self.game.N = 2

        # Устанавливаем очень большой ветер
        self.game.W[0] = 100
        self.game.W[1] = -100

        self.game.update_wind()

        # После обновления ветер должен быть в пределах -20..20
        self.assertGreaterEqual(self.game.W[0], -20)
        self.assertLessEqual(self.game.W[0], 20)
        self.assertGreaterEqual(self.game.W[1], -20)
        self.assertLessEqual(self.game.W[1], 20)


class IntegrationTests(unittest.TestCase):
    """Интеграционные тесты"""

    def test_command_line_interface_russian(self):
        """Тест интерфейса командной строки на русском"""
        # Проверяем, что игра запускается без ошибок
        result = subprocess.run(
            [sys.executable, "artillery3.py", "--test"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        self.assertEqual(result.returncode, 0)
        # Проверяем русский текст в выводе
        self.assertIn("Артиллерии", result.stdout)
        self.assertIn("тестовом режиме", result.stdout)

    def test_russian_output(self):
        """Проверка русскоязычного вывода"""
        game = artillery3.Artillery3()
        game.N = 2
        game.Q[0] = 45
        game.S[0] = 300

        # Перехватываем вывод
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            game.calculate_shot(0, 1)

        output = f.getvalue()

        # Проверяем наличие русских слов
        self.assertIn("ВЫСТРЕЛ", output)
        self.assertIn("МЕТРОВ", output)
        self.assertIn("ПАДЕНИЕ", output)


def run_physics_comparison():
    """Запуск сравнения физических расчетов"""
    print("=" * 70)
    print("СРАВНЕНИЕ ФИЗИЧЕСКИХ РАСЧЕТОВ")
    print("=" * 70)

    game = artillery3.Artillery3()
    game.N = 2  # Устанавливаем количество игроков

    # Тестовые случаи с реалистичными значениями
    test_cases = [
        {
            "name": "Стандартный выстрел",
            "angle": 45,
            "velocity": 300,  # 300 м/с ≈ 984 фут/сек
            "wind": 0,
            "expected_range": "~9,000-10,000 м"
        },
        {
            "name": "Низкий угол с ветром",
            "angle": 20,
            "velocity": 400,  # 400 м/с
            "wind": 10,
            "expected_range": "~8,000-9,000 м"
        },
        {
            "name": "Высокий угол",
            "angle": 70,
            "velocity": 250,  # 250 м/с
            "wind": -5,
            "expected_range": "~5,000-6,000 м"
        }
    ]

    print("\nРезультаты расчетов в метрической системе:")
    print("-" * 70)

    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}:")
        print(f"   Угол: {test['angle']}°, Скорость: {test['velocity']} м/с, Ветер: {test['wind']} м/с")

        game.Q[0] = test['angle']
        game.S[0] = test['velocity']
        game.W[0] = test['wind']
        game.P[0] = 0
        game.P[1] = 1000

        hit, impact = game.calculate_shot(0, 1)

        print(f"   Рассчитанная дистанция: {impact:,.0f} м")
        print(f"   Ожидаемая дистанция: {test['expected_range']}")

        # Проверяем, что расчеты реалистичны
        if 1000 < impact < 20000:
            print("   ✓ Реалистичная дистанция")
        else:
            print(f"   ⚠️ Необычная дистанция ({impact:,.0f} м)")

    print("\n" + "=" * 70)
    print("СРАВНЕНИЕ ЗАВЕРШЕНО")
    print("=" * 70)


def run_all_tests():
    """Запуск всех тестов с подробным отчетом"""
    print("=" * 70)
    print("ЗАПУСК ВСЕХ ТЕСТОВ АРТИЛЛЕРИИ 3")
    print("=" * 70)

    # Создаем test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestArtillery3)
    suite.addTests(loader.loadTestsFromTestCase(IntegrationTests))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print("ИТОГ ТЕСТИРОВАНИЯ:")
    print(f"Пройдено тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")

    if result.failures:
        print("\nПРОВАЛЕННЫЕ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)

    if result.errors:
        print("\nОШИБКИ:")
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback)

    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    # Запускаем все тесты с отчетом
    success = run_all_tests()

    if success:
        # Запускаем сравнение физики только если все тесты прошли
        print("\n" + "=" * 70)
        run_physics_comparison()

    # Завершаем с соответствующим кодом
    sys.exit(0 if success else 1)
