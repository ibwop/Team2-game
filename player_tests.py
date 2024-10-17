import unittest
from unittest.mock import patch
from items import *
from file_manager import * 
from player import *

@patch('file_manager.read_file') 
class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        """Set up for each test case."""
        self.mock_data = [
            ["Health", "How fast a player loses health"],
            ["Drunkenness", "How fast a player becomes drunk"],
            ["Strength", "Increases players base damage"],
            ["Luck", "Effects the likelihood of receiving certain perks, or facing certain enemies"],
            ["Charisma", "Reduces the cost of items in shops"]
        ]
        
    def test_stat_initialization(self, mock_read_file):
        """Tests that player stats are correctly initialized."""
        mock_read_file.return_value = self.mock_data

        stats = initialise_stats()

        for stat_name, stat_description in self.mock_data:
            # Verify stat exists
            self.assertIn(stat_name, stats)
            # Get object
            stat_obj = stats[stat_name]
            # Test object attributes are correct
            self.assertEqual(stat_obj.name, stat_name)
            self.assertEqual(stat_obj.description, stat_description)
            self.assertEqual(stat_obj.points, 1)  # Initial points should be 1

    def test_stat_increment(self, mock_read_file):
        """Tests that stats can be incremented correctly."""
        mock_read_file.return_value = self.mock_data
        stats = initialise_stats()
        
        health_stat = stats["Health"]
        self.assertEqual(health_stat.points, 1)
        health_stat.inc_points(3)
        self.assertEqual(health_stat.points, 4)
        health_stat.inc_points(2)
        self.assertEqual(health_stat.points, 6)

    def test_receive_attack(self, mock_read_file):
        """Tests that attacks on the player work properly."""
        mock_attacks = {
            "punched": 5,
            "kicked": 7,
            "headbutted": 10, 
            "elbowed": 6,
            "burnt": 9,
        }
        mock_read_file.return_value = mock_attacks
        
        # Instantiate class
        h = Health()
        
        # Check that attacks decrement health
        self.assertEqual(h.health, 100)  # Default starting health
        h.recieve_attack("punched")
        self.assertEqual(h.health, 95)  # Health should now be 95
        h.recieve_attack("elbowed")
        self.assertEqual(h.health, 89)  # Health should now be 89


if __name__ == '__main__':
    unittest.main()
