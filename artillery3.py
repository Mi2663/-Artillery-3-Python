#!/usr/bin/env python3
"""
Artillery 3 - Port from BASIC to Python
Original game from "More BASIC Computer Games"
Ported for RTU MIREA semester project
"""

import math
import random
import sys
import os

class Artillery3:
    def __init__(self):
        # Initialize arrays as in original BASIC
        self.W = [0.0] * 4  # Wind for each player
        self.S = [0.0] * 4  # Shot velocity
        self.P = [0] * 4    # Player positions
        self.Q = [0] * 4    # Shot angles
        self.N = 0          # Number of players
        self.R = 0          # Round number
        self.V = [0.0] * 4  # Additional velocity component
        
    def clear_screen(self):
        """Clear screen cross-platform"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print game header"""
        print("\n" + " " * 33 + "ARTILLERY3")
        print(" " * 15 + "CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY")
        print("\n" * 2)
    
    def setup_game(self):
        """Setup game parameters"""
        print("WELCOME TO ARTILLERY3 - A REAL WAR GAME.")
        print("\nYOU ARE IN THE MIDDLE OF A WAR. BE CAREFUL!")
        print()
        
        # Get number of players
        while True:
            try:
                self.N = int(input("NUMBER OF PLAYERS (2 OR 3)? "))
                if self.N in (2, 3):
                    break
                print("PLEASE ENTER 2 OR 3")
            except ValueError:
                print("PLEASE ENTER A NUMBER")
        
        # Set player positions (as in original)
        positions = [500, 1500, 2500]
        for i in range(self.N):
            self.P[i] = positions[i]
        
        # Initialize wind (similar to original logic)
        wind_base = random.uniform(-25, 25)
        for i in range(self.N):
            self.W[i] = wind_base + random.uniform(-5, 5)
        
        # Initialize velocities
        for i in range(self.N):
            self.V[i] = 0.0
        
        print("\nPLAYERS ARE AT:")
        for i in range(self.N):
            print(f"PLAYER {i+1}: POSITION {self.P[i]} YARDS")
        print(f"\nINITIAL WIND: {wind_base:.1f}")
        print()
        
        return True
    
    def get_player_input(self, player_num):
        """Get shot parameters from player"""
        print(f"\n{'='*50}")
        print(f"PLAYER {player_num + 1}'S TURN")
        print(f"Position: {self.P[player_num]} yards")
        print(f"Wind: {self.W[player_num]:.1f}")
        print(f"{'='*50}")
        
        # Get angle
        while True:
            try:
                angle_input = input("ANGLE (DEGREES, 0-90)? ")
                angle = float(angle_input)
                if 0 <= angle <= 90:
                    self.Q[player_num] = angle
                    break
                else:
                    print("ANGLE MUST BE BETWEEN 0 AND 90")
            except ValueError:
                print("PLEASE ENTER A VALID NUMBER")
        
        # Get velocity
        while True:
            try:
                velocity_input = input("VELOCITY (FEET/SEC, 0-3000)? ")
                velocity = float(velocity_input)
                if 0 < velocity <= 3000:
                    self.S[player_num] = velocity
                    break
                else:
                    print("VELOCITY MUST BE BETWEEN 0 AND 3000")
            except ValueError:
                print("PLEASE ENTER A VALID NUMBER")
        
        # Add random velocity component (as in original)
        self.V[player_num] = random.uniform(-50, 50)
        return True
    
    def calculate_shot(self, shooter, target):
        """Calculate shot trajectory and result"""
        # Convert angle to radians
        angle_rad = math.radians(self.Q[shooter])
        
        # Total velocity with random component
        total_v = self.S[shooter] + self.V[shooter]
        
        # Physics constants
        g = 32.2  # Gravity ft/s^2
        wind = self.W[shooter]
        
        # Calculate time of flight (simplified projectile motion)
        # t = (2 * v * sin(angle)) / g
        time_of_flight = (2 * total_v * math.sin(angle_rad)) / g
        
        # Calculate horizontal distance with wind effect
        # distance = v * cos(angle) * t + 0.5 * wind * t^2
        horizontal_distance = (total_v * math.cos(angle_rad) * time_of_flight) + \
                             (0.5 * wind * time_of_flight * time_of_flight)
        
        # Calculate impact position
        start_pos = self.P[shooter]
        impact_pos = start_pos + horizontal_distance
        
        # Target position
        target_pos = self.P[target]
        
        # Print shot information
        print(f"\nSHOT FROM POSITION: {start_pos:.0f}")
        print(f"ANGLE: {self.Q[shooter]:.1f}°")
        print(f"VELOCITY: {total_v:.1f} ft/s (base: {self.S[shooter]:.0f}, variation: {self.V[shooter]:.1f})")
        print(f"WIND: {wind:.1f}")
        print(f"TIME OF FLIGHT: {time_of_flight:.1f} sec")
        print(f"IMPACT AT: {impact_pos:.0f} yards")
        print(f"TARGET AT: {target_pos} yards")
        
        # Check for hit
        distance_to_target = abs(impact_pos - target_pos)
        
        if distance_to_target <= 50:  # Hit threshold
            print(f"\n{'*' * 50}")
            print(f"*** DIRECT HIT ON PLAYER {target + 1}! ***")
            print(f"*** PLAYER {shooter + 1} WINS! ***")
            print(f"{'*' * 50}")
            return True, impact_pos
        else:
            if impact_pos > target_pos:
                print(f"OVERSHOT BY {distance_to_target:.0f} YARDS")
            else:
                print(f"UNDERSHOT BY {distance_to_target:.0f} YARDS")
            return False, impact_pos
    
    def update_wind(self):
        """Update wind conditions after each round"""
        print("\n" + "-" * 40)
        print("WIND CONDITIONS ARE CHANGING...")
        
        for i in range(self.N):
            change = random.uniform(-10, 10)
            self.W[i] += change
            # Keep wind within reasonable bounds
            if self.W[i] > 50:
                self.W[i] = 50
            elif self.W[i] < -50:
                self.W[i] = -50
            
            print(f"Player {i+1} wind: {self.W[i]:.1f}")
        print("-" * 40)
    
    def play_round(self):
        """Play one complete round"""
        self.R += 1
        print(f"\n{'#' * 60}")
        print(f"ROUND {self.R}")
        print(f"{'#' * 60}")
        
        # Each player shoots at the next player
        for shooter in range(self.N):
            target = (shooter + 1) % self.N
            
            # Get input from shooter
            self.get_player_input(shooter)
            
            # Calculate shot
            hit, impact_pos = self.calculate_shot(shooter, target)
            
            if hit:
                return True, shooter  # Game over, return winner
        
        # Update wind for next round
        self.update_wind()
        
        return False, None
    
    def play_game(self):
        """Main game loop"""
        self.clear_screen()
        self.print_header()
        
        if not self.setup_game():
            return
        
        game_over = False
        winner = None
        
        while not game_over:
            game_over, winner = self.play_round()
            
            if not game_over:
                # Ask to continue
                while True:
                    response = input("\nANOTHER ROUND (Y/N)? ").strip().upper()
                    if response in ('Y', 'N', 'YES', 'NO'):
                        if response.startswith('N'):
                            print("\nTHANKS FOR PLAYING ARTILLERY 3!")
                            return
                        break
                    print("PLEASE ANSWER YES OR NO")
        
        print(f"\n{'=' * 60}")
        print(f"GAME OVER! PLAYER {winner + 1} WINS IN {self.R} ROUNDS!")
        print(f"{'=' * 60}")
        
        # Ask for replay
        while True:
            response = input("\nPLAY AGAIN (Y/N)? ").strip().upper()
            if response in ('Y', 'N', 'YES', 'NO'):
                if response.startswith('Y'):
                    self.__init__()  # Reset game
                    self.play_game()
                    return
                break
            print("PLEASE ANSWER YES OR NO")
        
        print("\nTHANK YOU FOR PLAYING ARTILLERY 3!")
        print("ORIGINAL BASIC VERSION: MORE BASIC COMPUTER GAMES")


def main():
    """Main entry point"""
    print("Initializing Artillery 3...")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode - automated gameplay
        print("Running in test mode...")
        game = Artillery3()
        
        # Simulate game setup
        game.N = 2
        game.P = [500, 1500]
        game.W = [5.0, 5.0]
        game.Q = [45, 45]
        game.S = [500, 500]
        
        # Test calculations
        print("\nTesting shot calculation...")
        hit, impact = game.calculate_shot(0, 1)
        print(f"Test shot hit: {hit}, impact at: {impact}")
        
        return
    
    # Normal gameplay
    game = Artillery3()
    game.play_game()


if __name__ == "__main__":
    main()
