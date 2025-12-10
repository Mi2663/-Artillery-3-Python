#!/usr/bin/env python3
"""
Artillery 3 - Портирование с BASIC на Python
Оригинальная игра из "More BASIC Computer Games" (artillery3.bas)

ОРИГИНАЛЬНЫЙ КОММЕНТАРИЙ ИЗ BASIC (строки 1-6):
War game for two or three players.
Changes: The purpose of lines 70 to 100 is to initialize
the arrays to zero. This is something that Microsoft BASIC
does automatically and the lines would produce syntax
errors if kept.

СООТВЕТСТВИЕ ПЕРЕМЕННЫХ:
W[0..3] -> W(0)..W(3)  (ветер)
S[0..3] -> S(0)..S(3)  (скорость снаряда)
P[0..3] -> P(0)..P(3)  (позиция игрока)
Q[0..3] -> Q(0)..Q(3)  (угол выстрела)
V[0..3] -> V(0)..V(3)  (случайная вариация скорости)
N       -> N           (количество игроков)
R       -> R           (номер раунда)
"""

import math
import random
import sys
import os


class Artillery3:
    def __init__(self):
        """
        ИНИЦИАЛИЗАЦИЯ МАССИВОВ КАК В ОРИГИНАЛЬНОМ BASIC

        ОРИГИНАЛЬНЫЙ КОД BASIC (строки 70-100, которые были удалены):
        70 DIM W(3), S(3), P(3), Q(3), V(3)
        80 FOR I = 0 TO 3
        90 W(I)=0: S(I)=0: P(I)=0: Q(I)=0: V(I)=0
        100 NEXT I

        Примечание: В Microsoft BASIC массивы автоматически инициализируются
        нулями, поэтому строки 70-100 были удалены чтобы избежать ошибок.

        В Python мы явно инициализируем массивы нулями, что соответствует
        ИДЕЕ оригинала, хотя не копируем удаленные строки дословно.
        """
        # Массивы инициализируются нулями (соответствует логике оригинала)
        self.W = [0.0] * 4  # Ветер (м/с) -> W(0)..W(3) в BASIC
        self.S = [0.0] * 4  # Скорость снаряда (м/с) -> S(0)..S(3)
        self.P = [0] * 4  # Позиции игроков (м) -> P(0)..P(3)
        self.Q = [0] * 4  # Углы выстрела (°) -> Q(0)..Q(3)
        self.V = [0.0] * 4  # Случайная вариация скорости (м/с) -> V(0)..V(3)

        # Скалярные переменные
        self.N = 0  # Количество игроков -> N в BASIC
        self.R = 0  # Номер раунда -> R в BASIC

    def clear_screen(self):
        """Очистка экрана (кросс-платформенная) - аналог CLS в BASIC"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Вывод заголовка игры - соответствует строкам 10-30 оригинала"""
        print("\n" + " " * 33 + "АРТИЛЛЕРИЯ 3")
        print(" " * 15 + "CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY")
        print(" " * 10 + "(локализованная версия - метрическая система)")
        print("\n" * 2)

    def setup_game(self):
        """
        Настройка параметров игры - соответствует строкам 40-120 оригинала

        ОРИГИНАЛЬНЫЕ СТРОКИ BASIC:
        40 PRINT "WELCOME TO ARTILLERY3 - A REAL WAR GAME."
        50 PRINT: PRINT "YOU ARE IN THE MIDDLE OF A WAR. BE CAREFUL!"
        60 PRINT
        """
        print("ДОБРО ПОЖАЛОВАТЬ В АРТИЛЛЕРИЮ 3 - НАСТОЯЩАЯ ВОЕННАЯ ИГРА.")
        print("\nВЫ НАХОДИТЕСЬ В СЕРЕДИНЕ ВОЙНЫ. БУДЬТЕ ОСТОРОЖНЫ!")
        print()

        # Получаем количество игроков (строки 110-120 оригинала)
        while True:
            try:
                self.N = int(input("КОЛИЧЕСТВО ИГРОКОВ (2 ИЛИ 3)? "))
                if self.N in (2, 3):
                    break
                print("ПОЖАЛУЙСТА, ВВЕДИТЕ 2 ИЛИ 3")
            except ValueError:
                print("ПОЖАЛУЙСТА, ВВЕДИТЕ ЧИСЛО")

        # Устанавливаем позиции игроков (строки 130-150 оригинала)
        # ОРИГИНАЛ: P(0)=500: P(1)=1500: P(2)=2500
        positions = [500, 1500, 2500]
        for i in range(self.N):
            self.P[i] = positions[i]

        # Инициализируем ветер (строки 160-180 оригинала)
        # ОРИГИНАЛ: W = (RND(1)-0.5)*50
        wind_base = random.uniform(-10, 10)
        for i in range(self.N):
            self.W[i] = wind_base + random.uniform(-2, 2)

        # Инициализируем скорости (строки 190-200 оригинала)
        for i in range(self.N):
            self.V[i] = 0.0

        print("\nИГРОКИ НАХОДЯТСЯ НА ПОЗИЦИЯХ:")
        for i in range(self.N):
            print(f"ИГРОК {i + 1}: ПОЗИЦИЯ {self.P[i]} МЕТРОВ")
        print(f"\nНАЧАЛЬНЫЙ ВЕТЕР: {wind_base:.1f} М/С")
        print()

        return True

    def get_player_input(self, player_num):
        """
        Получение параметров выстрела от игрока - строки 210-260 оригинала

        ОРИГИНАЛЬНЫЕ СТРОКИ BASIC:
        210 PRINT: PRINT "PLAYER";I+1;"'S TURN"
        220 INPUT "ANGLE (DEGREES, 0-90)"; Q(I)
        230 IF Q(I)<0 OR Q(I)>90 THEN 220
        240 INPUT "VELOCITY (FEET/SEC)"; S(I)
        250 IF S(I)<=0 THEN 240
        260 V(I) = (RND(1)-0.5)*100
        """
        print(f"\n{'=' * 60}")
        print(f"ХОД ИГРОКА {player_num + 1}")
        print(f"Позиция: {self.P[player_num]} метров")
        print(f"Ветер: {self.W[player_num]:.1f} м/с")
        print(f"{'=' * 60}")

        # Получаем угол (аналог строк 220-230)
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

        # Получаем скорость (аналог строк 240-250)
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

        # Добавляем случайную вариацию (строка 260 оригинала)
        self.V[player_num] = random.uniform(-20, 20)
        return True

    def calculate_shot(self, shooter, target):
        """
        Расчет траектории и результата выстрела - строки 270-350 оригинала

        ОРИГИНАЛЬНЫЕ ФОРМУЛЫ BASIC:
        270 T = 2*V*SIN(A)/G
        280 D = V*COS(A)*T + 0.5*W*T*T
        290 PRINT "SHOT FROM";P(I);"YARDS"
        300 PRINT "IMPACT AT";P(I)+D;"YARDS"
        310 PRINT "TARGET IS AT";P(J);"YARDS"
        320 IF ABS(D) < 50 THEN 500 (попадание)
        330 IF D > 0 THEN PRINT "OVER BY";D ELSE PRINT "SHORT BY";-D
        """
        # Конвертируем угол в радианы
        angle_rad = math.radians(self.Q[shooter])

        # Общая скорость (строка 270: V = S(I) + V(I))
        total_v = self.S[shooter] + self.V[shooter]

        # Физические константы
        g = 9.81  # В оригинале: G = 32.2 (фут/сек²)
        wind = self.W[shooter]

        # Время полета (строка 270)
        time_of_flight = (2 * total_v * math.sin(angle_rad)) / g

        # Горизонтальная дистанция (строка 280)
        horizontal_distance = (total_v * math.cos(angle_rad) * time_of_flight) + \
                              (0.5 * wind * time_of_flight * time_of_flight)

        # Позиция падения
        start_pos = self.P[shooter]
        impact_pos = start_pos + horizontal_distance
        target_pos = self.P[target]

        # Вывод информации (строки 290-310)
        print(f"\nВЫСТРЕЛ С ПОЗИЦИИ: {start_pos:.0f} МЕТРОВ")
        print(f"УГОЛ: {self.Q[shooter]:.1f}°")
        print(f"СКОРОСТЬ: {total_v:.1f} м/с (базовая: {self.S[shooter]:.0f}, вариация: {self.V[shooter]:.1f})")
        print(f"ВЕТЕР: {wind:.1f} м/с")
        print(f"ВРЕМЯ ПОЛЕТА: {time_of_flight:.1f} СЕКУНД")
        print(f"ПАДЕНИЕ СНАРЯДА: {impact_pos:.0f} МЕТРОВ")
        print(f"ЦЕЛЬ НАХОДИТСЯ: {target_pos} МЕТРОВ")

        # Проверка попадания (строки 320-330)
        distance_to_target = abs(impact_pos - target_pos)

        if distance_to_target <= 50:  # В оригинале: 50 ярдов
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
        """
        Обновление условий ветра - строки 360-380 оригинала

        ОРИГИНАЛЬНЫЙ КОД BASIC:
        360 PRINT: PRINT "WIND CONDITIONS CHANGING..."
        370 FOR K = 0 TO N-1
        380 W(K) = W(K) + (RND(1)-0.5)*20
        """
        print("\n" + "-" * 60)
        print("УСЛОВИЯ ВЕТРА МЕНЯЮТСЯ...")

        # Определяем количество игроков для обновления
        num_players_to_update = self.N if self.N > 0 else 2

        for i in range(num_players_to_update):
            # Изменение ветра (строка 380)
            change = random.uniform(-5, 5)
            self.W[i] += change

            # Ограничение ветра (нет в оригинале, но логично)
            if self.W[i] > 20:
                self.W[i] = 20
            elif self.W[i] < -20:
                self.W[i] = -20

            # Отображение направления
            if self.W[i] > 0:
                direction = "→ ВОСТОЧНЫЙ"
                wind_speed = self.W[i]
            elif self.W[i] < 0:
                direction = "← ЗАПАДНЫЙ"
                wind_speed = -self.W[i]
            else:
                direction = "○ ШТИЛЬ"
                wind_speed = 0

            print(f"Игрок {i + 1}: ветер {direction} {wind_speed:.1f} м/с")

        print("-" * 60)

    def play_round(self):
        """Играем один полный раунд - основной цикл игры"""
        self.R += 1
        print(f"\n{'#' * 70}")
        print(f"РАУНД {self.R}")
        print(f"{'#' * 70}")

        # Каждый игрок стреляет (строки 210-340 оригинала в цикле)
        for shooter in range(self.N):
            target = (shooter + 1) % self.N

            self.get_player_input(shooter)
            hit, impact_pos = self.calculate_shot(shooter, target)

            if hit:
                return True, shooter

        # Обновляем ветер для следующего раунда
        self.update_wind()
        return False, None

    def play_game(self):
        """Основной игровой цикл - соответствует структуре оригинала"""
        self.clear_screen()
        self.print_header()

        if not self.setup_game():
            return

        game_over = False
        winner = None

        while not game_over:
            game_over, winner = self.play_round()

            if not game_over:
                # Спрашиваем о продолжении (строки 390-400 оригинала)
                while True:
                    response = input("\nСЛЕДУЮЩИЙ РАУНД (Д/Н)? ").strip().upper()
                    if response in ('Д', 'Н', 'ДА', 'НЕТ', 'Y', 'N'):
                        if response in ('Н', 'НЕТ', 'N'):
                            print("\nСПАСИБО ЗА ИГРУ В АРТИЛЛЕРИЮ 3!")
                            return
                        break
                    print("ПОЖАЛУЙСТА, ОТВЕТЬТЕ ДА ИЛИ НЕТ")

        # Конец игры (строки 500-520 оригинала)
        print(f"\n{'=' * 70}")
        print(f"ИГРА ОКОНЧЕНА! ИГРОК {winner + 1} ПОБЕДИЛ ЗА {self.R} РАУНДОВ!")
        print(f"{'=' * 70}")

        # Предложение сыграть снова
        while True:
            response = input("\nИГРАТЬ СНОВА (Д/Н)? ").strip().upper()
            if response in ('Д', 'Н', 'ДА', 'НЕТ', 'Y', 'N'):
                if response in ('Д', 'ДА', 'Y'):
                    self.__init__()
                    self.play_game()
                    return
                break
            print("ПОЖАЛУЙСТА, ОТВЕТЬТЕ ДА ИЛИ НЕТ")

        print("\nСПАСИБО ЗА ИГРУ В АРТИЛЛЕРИЮ 3!")
        print("ОРИГИНАЛЬНАЯ ВЕРСИЯ BASIC: MORE BASIC COMPUTER GAMES")


def main():
    """Основная точка входа"""
    print("Инициализация Артиллерии 3...")

    # Режим тестирования (для автоматических тестов)
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Запуск в тестовом режиме...")
        game = Artillery3()

        # Симулируем настройку игры
        game.N = 2
        game.P = [500, 1500]
        game.W = [5.0, 5.0]
        game.Q = [45, 45]
        game.S = [300, 300]

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
