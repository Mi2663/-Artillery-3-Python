#!/usr/bin/env python3
"""
Artillery 3 (WAR3) - Python Port
Ported from the original BASIC game from "More BASIC Computer Games"
Original by Creative Computing, Morristown, New Jersey
"""

import math
import random
import sys

def get_input(prompt):
    """Wrapper for input to allow mocking in tests."""
    return input(prompt)

def print_header():
    print(" " * 22 + "ARTILLERY 3")
    print(" " * 20 + "CREATIVE COMPUTING")
    print(" " * 18 + "MORRISTOWN, NEW JERSEY")
    print("\n" * 3)

def show_instructions():
    print("\nTHIS IS A WAR GAME. TWO OR THREE PLAYERS ARE GIVEN")
    print("(THEORETICAL) CANNONS WITH WHICH THEY ATTEMPT TO SHOOT EACH")
    print("OTHER. THE PARAMETERS FOR DISTANCES AND MUZZLE VELOCITIES ARE")
    print("SET AT THE BEGINNING OF THE GAME. THE SHOTS ARE FIRED BY")
    print("GIVING A FIRING ANGLE, EXPRESSED IN DEGREES FROM HORIZONTAL")
    print()
    print("THE COMPUTER WILL KEEP TRACK OF THE GAME AND REPORT ALL")
    print("MOVES. A 'HIT' IS SCORED BY FIRING A SHOT WITHIN 5% OF THE")
    print("TOTAL DISTANCE FIRED OVER. GOOD LUCK")
    print()

def main():
    # Инициализация переменных, как в оригинале
    T = 0  # Round counter
    # DATA statements from original converted to a list
    distance_data = [1, 2, 2, 3, 3, 1, 1, 3, 3, 2, 2, 1, 2, 3, 3, 1, 1, 2, 0]

    print_header()
    print("WELCOME TO 'WAR3'. TWO OR THREE HUMANS MAY PLAY!")
    print("DO YOU WISH SOME ASSISTANCE", end="")
    assist_answer = get_input("? ").upper().strip()

    if assist_answer == "YES":
        show_instructions()

    # Get number of players
    while True:
        print()
        print("NO. OF PLAYERS", end="")
        try:
            N = int(get_input("? "))
        except ValueError:
            N = 0
        if N == 2 or N == 3:
            break
        print("ERROR--TWO OR THREE PLAYERS!")

    N1 = N if N == 3 else 1  # Number of distance pairs to query

    # Initialize arrays, as BASIC does (to zeros)
    V = [0.0] * 4  # Muzzle velocities (index 1-3)
    X = [0.0] * 4  # Max ranges (index 1-3)
    P = [0] * 4    # Player status (0=active, 12=defunct) (index 1-3)
    R = [[0.0] * 4 for _ in range(4)]  # Distances between players (1-3,1-3)

    # Read distances between players
    data_index = 0
    for J in range(1, N1 + 1):
        A = distance_data[data_index]
        B = distance_data[data_index + 1]
        data_index += 2
        print(f"DISTANCE (FT.) {A} TO {B}", end="")
        R[A][B] = float(get_input("? "))
        R[B][A] = R[A][B]

    # Reset data pointer for triangle validation
    data_index = 0

    # Triangle inequality check (only for 3 players)
    if N == 3:
        for J in range(1, N + 1):
            # Read three pairs that form a triangle side
            A = distance_data[data_index]
            B = distance_data[data_index + 1]
            C = distance_data[data_index + 2]
            D = distance_data[data_index + 3]
            E = distance_data[data_index + 4]
            F = distance_data[data_index + 5]
            data_index += 6

            # Triangle inequality: one side must be less than sum of other two
            if R[A][B] >= R[C][D] + R[E][F]:
                print("ERROR--ILLEGAL TRIANGLE. RE-ENTER RANGES.")
                # Reset and re-enter distances
                data_index = 0
                for J2 in range(1, N1 + 1):
                    A2 = distance_data[data_index]
                    B2 = distance_data[data_index + 1]
                    data_index += 2
                    print(f"DISTANCE (FT.) {A2} TO {B2}", end="")
                    R[A2][B2] = float(get_input("? "))
                    R[B2][A2] = R[A2][B2]
                break
        print()

    # Get muzzle velocities
    print()
    for J in range(1, N + 1):
        print(f"MUZZLE VELOCITY (FT./SEC.) OF {J}", end="")
        V[J] = float(get_input("? "))

    # Calculate max range for each player: V^2 / 32 (gravity constant)
    for J in range(1, N + 1):
        X[J] = V[J] ** 2 / 32.0

    # Check if each player can reach all others
    for A in range(1, N + 1):
        for B in range(1, N + 1):
            if A == B:
                continue
            if X[A] <= R[A][B]:
                print(f"ERROR--{A} CANNOT REACH {B}")
                print(f"WHAT IS THE MUZZLE VELOCITY OF {A}", end="")
                V[A] = float(get_input("? "))
                # Recalculate max ranges after velocity change
                for J in range(1, N + 1):
                    X[J] = V[J] ** 2 / 32.0
                # Restart checks from the beginning
                A, B = 0, 0  # Will break out of loops
                break
        else:
            continue
        break

    N1 = N  # Active players counter
    print("\n")

    # Main game loop
    while True:
        print(f"ROUND {T + 1}")
        print()

        for M in range(1, N + 1):
            # Skip defunct players
            if P[M] == 12:
                continue

            # Determine target
            if N == 2:
                C = 2 if M == 1 else 1
                print(f"PLAYER {M} SHOOTING AT {C}")
            else:  # N == 3
                if P[M] == 12:
                    continue
                while True:
                    print(f"PLAYER {M} SHOOTING AT", end="")
                    try:
                        C = int(get_input("? "))
                    except ValueError:
                        C = 0
                    if C not in [1, 2, 3]:
                        print("ERROR--PLAYERS DESIGNATED 1,2,3.")
                        continue
                    if C == M:
                        print("ERROR--CANNOT SHOOT SELF.")
                        continue
                    if P[C] == 12:
                        print(f"ERROR-- {C} IS DEFUNCT")
                        continue
                    break

            # Get firing angle
            while True:
                print("FIRING ANGLE", end="")
                try:
                    A3 = float(get_input("? "))
                except ValueError:
                    A3 = -1
                if A3 < 0 or A3 > 180:
                    print(f"ERROR--FIRED INTO GROUND. {M} NOW DEFUNCT.")
                    P[M] = 12
                    N1 -= 1
                    break  # Exit angle input loop, player is defunct
                if A3 >= 90:
                    print("ERROR--FIRED WRONG WAY, LOSE SHOT.")
                    break  # Exit angle input loop, shot is lost
                # Angle is valid
                # Calculate projectile range: (V^2/32) * sin(2*angle)
                # Note: Original uses SIN(A3*3.49064E-02) which is sin(angle * (pi/90))
                # sin(2*angle) = 2*sin(angle)*cos(angle). Original seems to use sin(angle) only.
                # Let's replicate the original calculation exactly.
                angle_rad = A3 * 3.49064E-02  # Degrees to radians (approx pi/90)
                Z = math.sin(angle_rad) * V[M] ** 2 / 32.0

                # Add random factor (simulates inaccuracy)
                X_rand = (R[M][C] / 1000.0 * random.random()) - (R[M][C] / 1000.0 * random.random())
                D = X_rand + Z  # Actual shot distance
                D1 = R[M][C] * 0.05  # 5% margin for hit

                # Evaluate shot
                if D < D1:  # Too close
                    print(f" TOO CLOSE- {M} IS DEFUNCT.")
                    P[M] = 12
                    N1 -= 1
                elif abs(D - R[M][C]) < D1:  # Hit
                    print(f" A HIT - {C} IS DEFUNCT.")
                    P[C] = 12
                    N1 -= 1
                elif D < R[M][C]:  # Undershot
                    print(f" YOU UNDERSHOT BY {abs(D - R[M][C]):.2f} FEET.")
                else:  # Overshot
                    print(f" YOU OVERSHOT BY {abs(D - R[M][C]):.2f} FEET.")
                break  # Exit angle input loop after processing shot

            # Check if game is over (only one player left)
            if N1 <= 1:
                print()
                for M1 in range(1, N + 1):
                    if P[M1] != 12:
                        print(f"GAME OVER. {M1} WINS.")
                        return  # End game
                # Should not reach here
                return

            print()

        # End of round
        T += 1
        print()

if __name__ == "__main__":
    main()
