import subprocess
import sys
import os

def run_game(inputs):
    """Run the game with given inputs and return output."""
    # This is a simple approach using subprocess
    # For more complex testing, you might want to mock input() directly
    process = subprocess.Popen(
        [sys.executable, 'artillery3.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Join inputs with newlines
    input_data = '\n'.join(inputs)
    stdout, stderr = process.communicate(input=input_data)
    
    return stdout, stderr

def test_basic_game():
    """Test a simple 2-player game scenario."""
    # Simulate: NO assistance, 2 players, distance=1000, velocities=200, 45 degree angle
    inputs = [
        "NO",        # Assistance? 
        "2",         # Number of players
        "1000",      # Distance 1 to 2
        "200",       # Muzzle velocity of 1
        "200",       # Muzzle velocity of 2
        "45",        # Firing angle for player 1
        "45",        # Firing angle for player 2
    ]
    
    print("Running test game...")
    stdout, stderr = run_game(inputs)
    
    # Check for expected strings in output
    assert "ARTILLERY 3" in stdout
    assert "WELCOME TO 'WAR3'" in stdout
    assert "ROUND 1" in stdout
    assert "PLAYER 1 SHOOTING AT 2" in stdout
    
    print("Test passed! Basic game flow works.")
    print("First 500 chars of output:")
    print(stdout[:500])

if __name__ == "__main__":
    test_basic_game()
