import unittest
from unittest.mock import patch


class TestLocation(unittest.TestCase):
    
    def setUp(self):
        # This will run before each test
        self.test_location_data = [
            [
                "Central Bar", 
                "PUB",  
                "south",  
                "Cardiff Queen St", 
                "west",  
                "North Junction",  
                "description for central bar"  
            ]
        ]

    @patch('file_manager.read_file')  # Mocking the read file function
    def test_initialise_locations(self, mock_read_file):
        """Tests that locations are correctly initialised"""
        # Make mock return the test location data (sp don't have to read the file in initialise locaiton)
        mock_read_file.return_value = self.test_location_data

        locations = initialise_locations()
        self.assertIn("Central Bar", locations) # Ensure location exists
        loc_obj = locations["Central Bar"] # Get object of the location

        # Check the attributes of the location object
        self.assertEqual(loc_obj.name, "Central Bar")
        self.assertEqual(loc_obj.type, "PUB")
        self.assertEqual(loc_obj.exits, {"south": "Cardiff Queen St", "west": "North Junction"})
        self.assertEqual(loc_obj.description, "description for central bar")
        self.assertFalse(loc_obj.visited)  # By default, visited should be False
        self.assertEqual(loc_obj.items, [])  # Items should be empty by default
        self.assertEqual(loc_obj.events, [])  # Events should be empty by default

    def test_is_empty_method(self):
        """Tests that the is empty method correctly recognises when events completed"""
        # Create a location instance for testing the is_empty method
        loc_obj = location("Test Location", "JUNCTION", {"north": "Next Location"}, "A test location.")
        self.assertTrue(loc_obj.is_empty())  # Should be True with no events
        
        # Add an event to the location and test again
        loc_obj.events.append("An event occurs!")
        self.assertFalse(loc_obj.is_empty())  # Should be False with an event

if __name__ == '__main__':
    unittest.main()