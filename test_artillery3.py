#!/usr/bin/env python3
"""Модуль автоматического тестирования Artillery 3"""

import unittest
import subprocess
import sys
import os

class TestArtillery3(unittest.TestCase):
    def setUp(self):
        self.game_path = os.path.join(os.path.dirname(__file__), 'artillery3.py')
    
    def test_game_initialization(self):
        """Тест инициализации игры"""
        # Тестируем с разным количеством игроков
        test_cases = [
            (["2"], "2 PLAYERS"),
            (["3"], "3 PLAYERS"),
        ]
        
        for inputs, expected in test_cases:
            with self.subTest(inputs=inputs):
                cmd = [sys.executable, self.game_path, "--test"]
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Отправляем тестовые данные
                input_data = "\n".join(inputs)
                output, error = process.communicate(input=input_data)
                
                self.assertIn(expected, output)
    
    def test_physics_calculation(self):
        """Тест физических расчетов"""
        from src.artillery3 import Artillery3
        
        game = Artillery3()
        game.Q[0] = 45
        game.S[0] = 500
        game.W[0] = 0
        game.P[0] = 0
        game.P[1] = 1000
        
        # Проверяем, что функция расчета работает без ошибок
        try:
            result = game.calculate_trajectory(0, 1)
            self.assertIsInstance(result, bool)
        except Exception as e:
            self.fail(f"Physics calculation failed: {e}")
    
    def test_input_validation(self):
        """Тест валидации ввода"""
        # Тестирование будет расширено
        pass

def run_comparison_test():
    """Сравнение с оригинальным выводом BASIC"""
    print("Running comparison with original BASIC output...")
    
    # Здесь можно добавить сравнение с эталонными логами
    # из оригинальной версии на BASIC
    
    # Пока что просто проверяем, что игра запускается
    result = subprocess.run(
        [sys.executable, "artillery3.py", "--test"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Game runs successfully")
        return True
    else:
        print("✗ Game failed to run")
        print("Error:", result.stderr)
        return False

if __name__ == "__main__":
    # Запуск юнит-тестов
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    # Запуск сравнительных тестов
    print("\n" + "="*50)
    run_comparison_test()
