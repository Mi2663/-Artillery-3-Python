#!/usr/bin/env python3
"""
Artillery 3 - Портирование с BASIC на Python
Оригинальная игра из "More BASIC Computer Games"
Локализованная версия на русском языке с метрической системой
"""

import math
import random
import sys
import os


class Artillery3:
    def __init__(self):
        # Инициализация массивов как в оригинальном BASIC
        self.W = [0.0] * 4  # Ветер для каждого игрока (м/с)
        self.S = [0.0] * 4  # Скорость выстрела (м/с)
        self.P = [0] * 4  # Позиции игроков (метры)
        self.Q = [0] * 4  # Углы стрельбы (градусы)
        self.N = 0  # Количество игроков
        self.R = 0  # Номер раунда
        self.V = [0.0] * 4  # Случайная вариация скорости (м/с)

    def clear_screen(self):
        """Очистка экрана (кросс-платформенная)"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Вывод заголовка игры"""
        print("\n" + " " * 33 + "АРТИЛЛЕРИЯ 3")
        print(" " * 15 + "CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY")
        print(" " * 10 + "(локализованная версия - метрическая система)")
        print("\n" * 2)

    def setup_game(self):
        """Настройка параметров игры"""
        print("ДОБРО ПОЖАЛОВАТЬ В АРТИЛЛЕРИЮ 3 - НАСТОЯЩАЯ ВОЕННАЯ ИГРА.")
        print("\nВЫ НАХОДИТЕСЬ В СЕРЕДИНЕ ВОЙНЫ. БУДЬТЕ ОСТОРОЖНЫ!")
        print()

        # Получаем количество игроков
        while True:
            try:
                self.N = int(input("КОЛИЧЕСТВО ИГРОКОВ (2 ИЛИ 3)? "))
                if self.N in (2, 3):
                    break
                print("ПОЖАЛУЙСТА, ВВЕДИТЕ 2 ИЛИ 3")
            except ValueError:
                print("ПОЖАЛУЙСТА, ВВЕДИТЕ ЧИСЛО")

        # Устанавливаем позиции игроков (в метрах)
        positions = [500, 1500, 2500]  # Примерно 0.5, 1.5, 2.5 км
        for i in range(self.N):
            self.P[i] = positions[i]

        # Инициализируем ветер (м/с)
        wind_base = random.uniform(-10, 10)  # От -10 до +10 м/с
        for i in range(self.N):
            self.W[i] = wind_base + random.uniform(-2, 2)

        # Инициализируем скорости
        for i in range(self.N):
            self.V[i] = 0.0

        print("\nИГРОКИ НАХОДЯТСЯ НА ПОЗИЦИЯХ:")
        for i in range(self.N):
            print(f"ИГРОК {i + 1}: ПОЗИЦИЯ {self.P[i]} МЕТРОВ")
        print(f"\nНАЧАЛЬНЫЙ ВЕТЕР: {wind_base:.1f} М/С")
        print()

        return True

    def get_player_input(self, player_num):
        """Получение параметров выстрела от игрока"""
        print(f"\n{'=' * 60}")
        print(f"ХОД ИГРОКА {player_num + 1}")
        print(f"Позиция: {self.P[player_num]} метров")
        print(f"Ветер: {self.W[player_num]:.1f} м/с")
        print(f"{'=' * 60}")

        # Получаем угол
        while True:
            try:
                angle_input = input("УГОЛ (ГРАДУСЫ, 0-90)? ")
                angle = float(angle_input)
                if 0 <= angle <= 90:
                    self.Q[player_num] = angle
                    break
                else:
                    print("УГОЛ ДОЛЖЕН БЫТЬ ОТ 0 ДО 90 ГРАДУСОВ")
            except ValueError:
                print("ПОЖАЛУЙСТА, ВВЕДИТЕ КОРРЕКТНОЕ ЧИСЛО")

        # Получаем скорость
        while True:
            try:
                velocity_input = input("СКОРОСТЬ (М/С, 0-1000)? ")
                velocity = float(velocity_input)
                if 0 < velocity <= 1000:
                    self.S[player_num] = velocity
                    break
                else:
                    print("СКОРОСТЬ ДОЛЖНА БЫТЬ ОТ 0 ДО 1000 М/С")
            except ValueError:
                print("ПОЖАЛУЙСТА, ВВЕДИТЕ КОРРЕКТНОЕ ЧИСЛО")

        # Добавляем случайную вариацию скорости
        self.V[player_num] = random.uniform(-20, 20)  # ±20 м/с
        return True

    def calculate_shot(self, shooter, target):
        """Расчет траектории и результата выстрела"""
        # Конвертируем угол в радианы
        angle_rad = math.radians(self.Q[shooter])

        # Общая скорость со случайной компонентой
        total_v = self.S[shooter] + self.V[shooter]

        # Физические константы (метрическая система)
        g = 9.81  # Ускорение свободного падения, м/с²
        wind = self.W[shooter]  # Ветер, м/с

        # Рассчитываем время полета
        # t = (2 * v * sin(угол)) / g
        time_of_flight = (2 * total_v * math.sin(angle_rad)) / g

        # Рассчитываем горизонтальную дистанцию с учетом ветра
        # дистанция = v * cos(угол) * t + 0.5 * ветер * t²
        horizontal_distance = (total_v * math.cos(angle_rad) * time_of_flight) + \
                              (0.5 * wind * time_of_flight * time_of_flight)

        # Рассчитываем позицию падения
        start_pos = self.P[shooter]
        impact_pos = start_pos + horizontal_distance

        # Позиция цели
        target_pos = self.P[target]

        # Выводим информацию о выстреле
        print(f"\nВЫСТРЕЛ С ПОЗИЦИИ: {start_pos:.0f} МЕТРОВ")
        print(f"УГОЛ: {self.Q[shooter]:.1f}°")
        print(f"СКОРОСТЬ: {total_v:.1f} м/с (базовая: {self.S[shooter]:.0f}, вариация: {self.V[shooter]:.1f})")
        print(f"ВЕТЕР: {wind:.1f} м/с")
        print(f"ВРЕМЯ ПОЛЕТА: {time_of_flight:.1f} СЕКУНД")
        print(f"ПАДЕНИЕ СНАРЯДА: {impact_pos:.0f} МЕТРОВ")
        print(f"ЦЕЛЬ НАХОДИТСЯ: {target_pos} МЕТРОВ")

        # Проверяем попадание
        distance_to_target = abs(impact_pos - target_pos)

        if distance_to_target <= 50:  # Порог попадания - 50 метров
            print(f"\n{'*' * 60}")
            print(f"*** ПРЯМОЕ ПОПАДАНИЕ В ИГРОКА {target + 1}! ***")
            print(f"*** ИГРОК {shooter + 1} ПОБЕДИЛ! ***")
            print(f"{'*' * 60}")
            return True, impact_pos
        else:
            if impact_pos > target_pos:
                print(f"ПЕРЕЛЕТ НА {distance_to_target:.0f} МЕТРОВ")
            else:
                print(f"НЕДОЛЕТ НА {distance_to_target:.0f} МЕТРОВ")
            return False, impact_pos

    def update_wind(self):
        """Обновление условий ветра после каждого раунда"""
        print("\n" + "-" * 60)
        print("УСЛОВИЯ ВЕТРА МЕНЯЮТСЯ...")

        # Определяем количество игроков для обновления ветра
        # Если игра не инициализирована, используем значение по умолчанию
        num_players_to_update = self.N if self.N > 0 else 2

        for i in range(num_players_to_update):
            # Генерируем случайное изменение ветра от -5 до +5 м/с
            change = random.uniform(-5, 5)
            self.W[i] += change

            # Ограничиваем ветер разумными пределами (-20..+20 м/с)
            if self.W[i] > 20:
                self.W[i] = 20
            elif self.W[i] < -20:
                self.W[i] = -20

            # Определяем направление ветра для отображения
            if self.W[i] > 0:
                direction = "→ ВОСТОЧНЫЙ"
                wind_speed = self.W[i]
            elif self.W[i] < 0:
                direction = "← ЗАПАДНЫЙ"
                wind_speed = -self.W[i]  # Берем абсолютное значение
            else:
                direction = "○ ШТИЛЬ"
                wind_speed = 0

            # Выводим информацию о ветре для игрока
            print(f"Игрок {i + 1}: ветер {direction} {wind_speed:.1f} м/с")

        print("-" * 60)

    def play_round(self):
        """Играем один полный раунд"""
        self.R += 1
        print(f"\n{'#' * 70}")
        print(f"РАУНД {self.R}")
        print(f"{'#' * 70}")

        # Каждый игрок стреляет в следующего игрока
        for shooter in range(self.N):
            target = (shooter + 1) % self.N

            # Получаем ввод от стреляющего
            self.get_player_input(shooter)

            # Рассчитываем выстрел
            hit, impact_pos = self.calculate_shot(shooter, target)

            if hit:
                return True, shooter  # Игра окончена, возвращаем победителя

        # Обновляем ветер для следующего раунда
        self.update_wind()

        return False, None

    def play_game(self):
        """Основной игровой цикл"""
        self.clear_screen()
        self.print_header()

        if not self.setup_game():
            return

        game_over = False
        winner = None

        while not game_over:
            game_over, winner = self.play_round()

            if not game_over:
                # Спрашиваем, продолжать ли
                while True:
                    response = input("\nСЛЕДУЮЩИЙ РАУНД (Д/Н)? ").strip().upper()
                    if response in ('Д', 'Н', 'ДА', 'НЕТ', 'Y', 'N'):
                        if response in ('Н', 'НЕТ', 'N'):
                            print("\nСПАСИБО ЗА ИГРУ В АРТИЛЛЕРИЮ 3!")
                            return
                        break
                    print("ПОЖАЛУЙСТА, ОТВЕТЬТЕ ДА ИЛИ НЕТ")

        print(f"\n{'=' * 70}")
        print(f"ИГРА ОКОНЧЕНА! ИГРОК {winner + 1} ПОБЕДИЛ ЗА {self.R} РАУНДОВ!")
        print(f"{'=' * 70}")

        # Спрашиваем о повторной игре
        while True:
            response = input("\nИГРАТЬ СНОВА (Д/Н)? ").strip().upper()
            if response in ('Д', 'Н', 'ДА', 'НЕТ', 'Y', 'N'):
                if response in ('Д', 'ДА', 'Y'):
                    self.__init__()  # Сбрасываем игру
                    self.play_game()
                    return
                break
            print("ПОЖАЛУЙСТА, ОТВЕТЬТЕ ДА ИЛИ НЕТ")

        print("\nСПАСИБО ЗА ИГРУ В АРТИЛЛЕРИЮ 3!")
        print("ОРИГИНАЛЬНАЯ ВЕРСИЯ BASIC: MORE BASIC COMPUTER GAMES")


def main():
    """Основная точка входа"""
    print("Инициализация Артиллерии 3...")

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Тестовый режим - автоматическая игра
        print("Запуск в тестовом режиме...")
        game = Artillery3()

        # Симулируем настройку игры
        game.N = 2
        game.P = [500, 1500]
        game.W = [5.0, 5.0]
        game.Q = [45, 45]
        game.S = [300, 300]  # 300 м/с ≈ 984 фут/сек

        # Тестируем расчеты
        print("\nТестирование расчета выстрела...")
        hit, impact = game.calculate_shot(0, 1)
        print(f"Тестовый выстрел: попадание = {hit}, точка падения = {impact:.0f} м")

        # Тестируем обновление ветра
        print("\nТестирование обновления ветра...")
        print(f"Ветер до обновления: {game.W[0]:.1f} м/с, {game.W[1]:.1f} м/с")
        game.update_wind()
        print(f"Ветер после обновления: {game.W[0]:.1f} м/с, {game.W[1]:.1f} м/с")

        return

    # Обычный игровой режим
    game = Artillery3()
    game.play_game()


if __name__ == "__main__":
    main()
