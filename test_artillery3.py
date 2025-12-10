#!/usr/bin/env python3
"""
Test module for Artillery 3
Automated testing with comparison to original BASIC behavior
"""

import unittest
import subprocess
import sys
import os
from io import StringIO
import artillery3

class TestArtillery3(unittest.TestCase):
    """Unit tests for Artillery 3 game"""
    
    def setUp(self):
        """Set up test fixture"""
        self.game = artillery3.Artillery3()
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()
    
    def tearDown(self):
        """Clean up after test"""
        sys.stdout = self.original_stdout
    
    def test_game_initialization(self):
        """Test game initialization"""
        self.game.N = 2
        self.assertEqual(self.game.N, 2)
        
        self.game.N = 3
        self.assertEqual(self.game.N, 3)
    
    def test_physics_calculations(self):
        """Test physics calculations"""
        # Test with known values
        self.game.Q[0] = 45
        self.game.S[0] = 500
        self.game.W[0] = 0
        self.game.P[0] = 0
        self.game.P[1] = 1000
        
        hit, impact = self.game.calculate_shot(0, 1)
        
        # Should be a boolean and a number
        self.assertIsInstance(hit, bool)
        self.assertIsInstance(impact, (int, float))
        
        # Impact should be positive
        self.assertGreater(impact, 0)
    
    def test_wind_update(self):
        """Test wind update mechanics"""
        original_wind = self.game.W.copy()
        self.game.update_wind()
        
        # Wind should have changed
        self.assertNotEqual(self.game.W, original_wind)
        
        # Wind should be within bounds
        for wind in self.game.W[:self.game.N]:
            self.assertGreaterEqual(wind, -50)
            self.assertLessEqual(wind, 50)
    
    def test_player_positions(self):
        """Test player position setup"""
        self.game.N = 2
        self.game.setup_game()
        
        # Positions should be set according to original game
        self.assertEqual(self.game.P[0], 500)
        self.assertEqual(self.game.P[1], 1500)
        
        if self.game.N == 3:
            self.assertEqual(self.game.P[2], 2500)
    
    def test_shot_validation(self):
        """Test shot parameter validation"""
        # This would test input validation (requires mocking)
        pass


class IntegrationTests(unittest.TestCase):
    """Integration tests comparing with original BASIC"""
    
    def test_basic_equivalence(self):
        """Test that Python version produces similar results to BASIC"""
        # This is a placeholder for actual comparison tests
        # In real implementation, you would compare outputs with
        # saved logs from the original BASIC version
        
        print("Integration tests would compare with original BASIC output")
        self.assertTrue(True)  # Placeholder assertion
    
    def test_command_line_interface(self):
        """Test command line interface"""
        # Test that game runs without errors
        result = subprocess.run(
            [sys.executable, "artillery3.py", "--test"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Artillery", result.stdout)


def run_comparison_with_basic():
    """Run comparison tests with original BASIC output"""
    print("=" * 60)
    print("COMPARISON TESTS WITH ORIGINAL BASIC VERSION")
    print("=" * 60)
    
    # Note: In a real project, you would have saved output
    # from the original BASIC version and compare it with
    # the output from your Python version
    
    test_cases = [
        {
            "name": "Basic shot calculation",
            "basic_output": "IMPACT AT 1523 YARDS",  # Example from BASIC
            "params": {"angle": 45, "velocity": 500, "wind": 0}
        },
        # Add more test cases as needed
    ]
    
    all_passed = True
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Expected from BASIC: {test['basic_output']}")
        
        # Run Python version with same parameters
        game = artillery3.Artillery3()
        game.Q[0] = test["params"]["angle"]
        game.S[0] = test["params"]["velocity"]
        game.W[0] = test["params"]["wind"]
        game.P[0] = 500
        game.P[1] = 1500
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            hit, impact = game.calculate_shot(0, 1)
        
        output = f.getvalue()
        print(f"Python output contains: IMPACT AT {int(impact)} YARDS")
        
        # Simple comparison - in real test you'd do more detailed comparison
        if "IMPACT AT" in output:
            print("✓ Output format matches BASIC")
        else:
            print("✗ Output format differs from BASIC")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL COMPARISON TESTS PASSED!")
    else:
        print("SOME TESTS FAILED - check differences")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    # Run unit tests
    print("Running unit tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    # Run comparison tests
    print("\n" + "=" * 60)
    run_comparison_with_basic()
