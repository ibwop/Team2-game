import unittest
from unittest.mock import patch
from code import *

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
        p = Player()
        stats = p.initialise_stats()

        for stat_name, stat_description in self.mock_data:
            # Verify stat exists
            self.assertIn(stat_name, stats)
            # Get object
            stat_obj = stats[stat_name]
            # Test object attributes are correct
            self.assertEqual(stat_obj.name, stat_name)
            self.assertEqual(stat_obj.description, stat_description)
            self.assertEqual(stat_obj.points, 0.5) # Initial stat points

    def test_stat_increment(self, mock_read_file):
        """Tests that stats can be incremented correctly."""
        p = Player()
        mock_read_file.return_value = self.mock_data
        stats = p.initialise_stats()
        
        health_stat = stats["Health"]
        health_stat.points = 0.5
           # Test incrementing within allowed bounds
        health_stat.inc_points(0.3)
        self.assertEqual(health_stat.points, 0.8)  # Points should now be 0.8

        # Test increment that would exceed 1
        health_stat.inc_points(0.5)
        self.assertEqual(health_stat.points, 1)  # Points should cap at 1

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
        p = Player()
        h = p.health
        
        # Check that attacks decrement health
        self.assertEqual(h.health, 100)  # Default starting health
        h.recieve_attack("punched")
        self.assertEqual(h.health, 95)  # Health should now be 95
        h.recieve_attack("elbowed")
        self.assertEqual(h.health, 89)  # Health should now be 89

    @patch('builtins.input', side_effect=['Health', '0.2', 'Strength', '0.3', 'Luck', '0.5'])  # mock user inputs
    @patch('builtins.print')  
    def test_allocate_points(self, mock_print, mock_input, mock_read_file):
        """Test that points are allocated to stats correctly."""
        mock_read_file.return_value = self.mock_data
        
        p = Player()
        p.available_points = 1  # set initial available points

        p.stats = {
            "Health": stat("Health", "Your health", 0.5),
            "Strength": stat("Strength", "Your strength", 0.5),
            "Luck": stat("Luck", "Your luck", 0.5)
        }
        
        # call allocate_points which will use the mocked inputs
        p.allocate_points()
        
        # verify that the points were correctly incremented
        self.assertEqual(p.stats["Health"].points, 0.7)  # health was incremented by 0.2
        self.assertEqual(p.stats["Strength"].points, 0.8)  # strength was incremented by 0.3
        self.assertEqual(p.stats["Luck"].points, 1) # luck was incremented by 0.5
        self.assertEqual(p.available_points, 0)  # all points should be allocated

if __name__ == '__main__':
    unittest.main()
