#!/usr/bin/env python3
"""
Artillery 3 - портирование с BASIC на Python
Original: More BASIC Computer Games (artillery3.bas)
"""

import math
import random
import sys
import os

class Artillery3:
    def __init__(self):
        # Инициализация переменных как в оригинальном BASIC
        self.W = [0.0] * 4  # Ветер для каждого игрока
        self.S = [0.0] * 4  # Сила выстрела
        self.P = [0] * 4    # Позиции игроков
        self.Q = [0] * 4    # Углы стрельбы
        self.N = 0          # Количество игроков
        self.R = 0          # Раунд
        
    def clear_screen(self):
        """Очистка экрана (кросс-платформенная)"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Вывод заголовка игры"""
        print(" " * 33 + "ARTILLERY3")
        print(" " * 15 + "CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY")
        print("\n\n")
    
    def setup_game(self):
        """Настройка параметров игры"""
        print("WELCOME TO ARTILLERY3 - A REAL WAR GAME.")
        print("\nYOU ARE IN THE MIDDLE OF A WAR. BE CAREFUL!")
        print()
        
        while True:
            try:
                self.N = int(input("NUMBER OF PLAYERS (2 OR 3)? "))
                if self.N in (2, 3):
                    break
                print("PLEASE ENTER 2 OR 3")
            except ValueError:
                print("PLEASE ENTER A NUMBER")
        
        # Установка позиций игроков
        positions = [500, 1500, 2500]
        for i in range(self.N):
            self.P[i] = positions[i]
        
        # Инициализация ветра
        wind_base = random.uniform(-25, 25)
        for i in range(self.N):
            self.W[i] = wind_base + random.uniform(-5, 5)
        
        print("\nPLAYERS ARE AT:")
        for i in range(self.N):
            print(f"PLAYER {i+1}: POSITION {self.P[i]} YARDS")
        print()
        
    def get_input(self, player_num):
        """Получение параметров выстрела от игрока"""
        print(f"\nPLAYER {player_num + 1}'S TURN")
        
        while True:
            try:
                angle = float(input("ANGLE (DEGREES, 0-90)? "))
                if 0 <= angle <= 90:
                    self.Q[player_num] = angle
                    break
                print("ANGLE MUST BE BETWEEN 0 AND 90")
            except ValueError:
                print("PLEASE ENTER A NUMBER")
        
        while True:
            try:
                velocity = float(input("VELOCITY (FEET/SEC)? "))
                if velocity > 0:
                    self.S[player_num] = velocity
                    break
                print("VELOCITY MUST BE POSITIVE")
            except ValueError:
                print("PLEASE ENTER A NUMBER")
    
    def calculate_trajectory(self, player_num, target_num):
        """Расчет траектории снаряда"""
        angle_rad = math.radians(self.Q[player_num])
        v = self.S[player_num]
        g = 32.2  # Ускорение свободного падения
        wind = self.W[player_num]
        
        # Время полета (упрощенная формула)
        t = (2 * v * math.sin(angle_rad)) / g
        
        # Горизонтальная дистанция с учетом ветра
        distance = (v * math.cos(angle_rad) * t) + (0.5 * wind * t * t)
        
        # Позиция выстрела
        start_pos = self.P[player_num]
        impact_pos = start_pos + distance
        
        # Проверка попадания
        target_pos = self.P[target_num]
        margin = 50  # Допустимая погрешность для попадания
        
        print(f"\nSHOT FROM {start_pos:.0f} YARDS")
        print(f"IMPACT AT {impact_pos:.0f} YARDS")
        print(f"TARGET IS AT {target_pos} YARDS")
        
        if abs(impact_pos - target_pos) <= margin:
            print(f"\n*** DIRECT HIT ON PLAYER {target_num + 1}! ***")
            return True
        else:
            diff = impact_pos - target_pos
            if diff > 0:
                print(f"OVERSHOT BY {abs(diff):.0f} YARDS")
            else:
                print(f"UNDERSHOT BY {abs(diff):.0f} YARDS")
            return False
    
    def game_round(self):
        """Проведение одного раунда игры"""
        self.R += 1
        print(f"\n{'='*50}")
        print(f"ROUND {self.R}")
        print(f"{'='*50}")
        
        # Каждый игрок стреляет по следующему
        for i in range(self.N):
            target = (i + 1) % self.N
            self.get_input(i)
            
            if self.calculate_trajectory(i, target):
                print(f"\nPLAYER {i + 1} WINS THE GAME!")
                return True
        
        # Обновление ветра
        print("\nWIND CONDITIONS CHANGING...")
        for i in range(self.N):
            change = random.uniform(-10, 10)
            self.W[i] += change
            print(f"PLAYER {i+1} WIND: {self.W[i]:.1f}")
        
        return False
    
    def play(self):
        """Основной игровой цикл"""
        self.clear_screen()
        self.print_header()
        self.setup_game()
        
        game_over = False
        while not game_over:
            game_over = self.game_round()
            
            if not game_over:
                while True:
                    response = input("\nANOTHER ROUND (Y/N)? ").upper()
                    if response in ('Y', 'N'):
                        if response == 'N':
                            print("\nTHANKS FOR PLAYING!")
                            return
                        break
                    print("PLEASE ENTER Y OR N")
    
    def run_test_mode(self, test_inputs):
        """Режим автоматического тестирования"""
        # Имитация ввода для тестов
        import io
        sys.stdin = io.StringIO('\n'.join(test_inputs))
        
        # Запуск игры с тестовыми данными
        self.setup_game()
        return self.game_round()

def main():
    """Точка входа в программу"""
    game = Artillery3()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Режим тестирования
        test_inputs = [
            "2",    # Количество игроков
            "45",   # Угол для игрока 1
            "500",  # Скорость для игрока 1
            "45",   # Угол для игрока 2
            "500",  # Скорость для игрока 2
        ]
        result = game.run_test_mode(test_inputs)
        print(f"\nTEST RESULT: {result}")
    else:
        # Обычный режим игры
        game.play()

if __name__ == "__main__":
    main()
