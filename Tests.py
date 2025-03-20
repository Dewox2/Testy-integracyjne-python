import unittest
import json
import shutil
import os
from my_app import App

class TestMarinesApp(unittest.TestCase):
    def setUp(self):
        self.test_file = "Dane/marines_data.json"
        self.backup_file = "Dane/marines_data_backup.json"

        shutil.copy(self.test_file, self.backup_file)
        
        self.app = App(self.test_file)

    def tearDown(self):
  
        shutil.copy(self.backup_file, self.test_file)
        os.remove(self.backup_file)

    def test_marines_count(self):
        self.assertGreaterEqual(len(self.app.get_marines()), 2)

    def test_existence_of_marine(self):
        marine = self.app.get_marine(2)
        self.assertIsNotNone(marine)
        self.assertEqual(marine["name"], "Ortan Cassius")
        self.assertEqual(marine["function"], "Chaplain")

    def test_add_marine(self):
        start_count = len(self.app.get_marines())
        new_marine = {"id": 4, "name": "Tigurius", "age": 120, "function": "Librarian", "battles": ["War of the Beast"]}
        self.app.add_marine(new_marine)
        self.assertEqual(len(self.app.get_marines()), start_count + 1)

    def test_update_marine(self):
        self.app.set_marine(2, {"age": 130})
        updated_marine = self.app.get_marine(2)
        self.assertIsNotNone(updated_marine)
        self.assertEqual(updated_marine["age"], 130)

    def test_delete_marine(self):

        start_count = len(self.app.get_marines())
        self.app.delete_marine(2)
        self.assertEqual(len(self.app.get_marines()), start_count - 1)
        self.assertIsNone(self.app.get_marine(2))

if __name__ == '__main__':
    unittest.main()
