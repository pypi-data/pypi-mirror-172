import sqlite3
import os

from luxhouse.model import House, Location, PriceDate

class SQLite(object):
    def __init__(self, location:str) -> None:
        self.location = location

        if not os.path.exists(self.location):
            with sqlite3.connect(self.location) as conn:
                cursor = conn.cursor()
                cursor.execute(PriceDate.create_table())
                cursor.execute(Location.create_table())
                cursor.execute(House.create_table())
                print('database initialized')

    def add_house(self, house:House):
        with sqlite3.connect(self.location) as conn:
            cursor = conn.cursor()
            house.insert(cursor)