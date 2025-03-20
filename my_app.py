import json
import os

class App:
    def __init__(self, database):
        # Konstruktor klasy. Inicjalizuje obiekt z podaną ścieżką do pliku bazy danych
        # i ładuje dane z pliku JSON.
        self.database = database
        self.load_data()

    def load_data(self):
        # Ładuje dane z pliku JSON. Jeśli plik nie istnieje, inicjalizuje pustą strukturę danych.
        try:
            with open(self.database, "r", encoding="utf-8") as f:
                self.dane = json.load(f)
        except FileNotFoundError:
            print("Plik JSON nie istnieje!")
            self.dane = {"members": []}

    def get_marines(self):
        # Zwraca listę wszystkich członków (marines) z danych.
        return self.dane.get("members", [])

    def get_marine(self, id):
        # Wyszukuje i zwraca dane konkretnego członka (marine) na podstawie jego ID.
        # Jeśli nie znajdzie członka, zwraca None.
        for marine in self.get_marines():
            if int(marine["id"]) == int(id):
                return marine
        return None

    def set_marine(self, id, new_data):
        # Aktualizuje dane konkretnego członka (marine) na podstawie jego ID.
        # Jeśli członek zostanie znaleziony i zaktualizowany, zapisuje zmiany do pliku i zwraca True.
        # Jeśli nie znajdzie członka, zwraca False.
        for marine in self.dane["members"]:
            if int(marine["id"]) == int(id):  
                marine.update(new_data)
                self.set_marines()
                return True
        return False

    def add_marine(self, new_marine):
        # Dodaje nowego członka (marine) do listy, jeśli jego ID nie istnieje już w danych.
        # Po dodaniu zapisuje zmiany do pliku.
        if not any(int(m["id"]) == int(new_marine["id"]) for m in self.dane["members"]):
            self.dane["members"].append(new_marine)
            self.set_marines()

    def delete_marine(self, id):
        # Usuwa członka (marine) z listy na podstawie jego ID.
        # Jeśli członek zostanie usunięty, zapisuje zmiany do pliku.
        original_count = len(self.dane["members"])
        self.dane["members"] = [m for m in self.dane["members"] if int(m["id"]) != int(id)]
        
        if len(self.dane["members"]) < original_count:  
            self.set_marines()

    def set_marines(self):
        # Zapisuje aktualne dane do pliku JSON i ponownie ładuje dane z pliku.
        with open(self.database, "w", encoding="utf-8") as f:
            json.dump(self.dane, f, indent=4)
        self.load_data()
