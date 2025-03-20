import json
import os

class App:
    def __init__(self, database):
        self.database = database
        self.load_data()

    def load_data(self):
        try:
            with open(self.database, "r", encoding="utf-8") as f:
                self.dane = json.load(f)
        except FileNotFoundError:
            print("Plik JSON nie istnieje!")
            self.dane = {"members": []}

    def get_marines(self):
        return self.dane.get("members", [])

    def get_marine(self, id):
        for marine in self.get_marines():
            if int(marine["id"]) == int(id):
                return marine
        return None

    def set_marine(self, id, new_data):
        for marine in self.dane["members"]:
            if int(marine["id"]) == int(id):  
                marine.update(new_data)
                self.set_marines()
                return True
        return False

    def add_marine(self, new_marine):
        if not any(int(m["id"]) == int(new_marine["id"]) for m in self.dane["members"]):
            self.dane["members"].append(new_marine)
            self.set_marines()

    def delete_marine(self, id):
        original_count = len(self.dane["members"])
        self.dane["members"] = [m for m in self.dane["members"] if int(m["id"]) != int(id)]
        
        if len(self.dane["members"]) < original_count:  
            self.set_marines()

    def set_marines(self):
        with open(self.database, "w", encoding="utf-8") as f:
            json.dump(self.dane, f, indent=4)
        self.load_data()
