from datetime import date
from sqlite3 import Cursor

def fetchOne(cursor: Cursor, sql:str, values:tuple) -> any:
    cursor.execute(sql, values)
    records = cursor.fetchone()
    
    if records is None:
        with_values = ''
        for item in values:
            with_values = with_values + str(item) + ','
        
        if with_values:
            with_values = ' with values (' + with_values + ')'

        raise Exception("query found nothin: " + sql + with_values)

    return records[0]

class PriceDate(object):
    def __init__(self, price:int, date:date, house_id:int) -> None:
        self.price = price
        self.date = date
        self.house_id = house_id

    def create_table() -> str:
        return """
            create table if not exists price_date(
                id integer primary key,
                price integer,
                date date not null,
                house_id integer not null,
                unique(price, date, house_id),
                constraint fk_house foreign key (house_id) references houses (id)
            );"""
    
    def insert(self, cursor:Cursor):
        if not self.is_saved(cursor):
            sql = "insert into price_date(price,date,house_id) values (?,?,?);"
            values = (self.price, self.date, self.house_id)
            cursor.execute(sql, values)
        
        self.id = self.get_id(cursor)
        return self

    def get_id(self, cursor: Cursor) -> int:
        sql = "select id from price_date where (price=? or price is null) and date=? and house_id=?;"
        values = (self.price, self.date, self.house_id)
        return fetchOne(cursor, sql, values)

    def is_saved(self, cursor: Cursor) -> bool:
        try:
            self.get_id(cursor)
            return True
        except:
            return False

class Location(object):
    def __init__(self, locality:str, commune:str, country:str) -> None:
        self.locality = locality
        self.commune = commune
        self.country = country

    def create_table() -> str:
        return """
            create table if not exists locations(
                id integer primary key,
                locality text not null,
                commune text not null,
                country text not null,
                unique(locality,commune, country)
            );"""

    def insert(self, cursor: Cursor):
        if not self.is_saved(cursor):
            sql = "insert into locations(locality,commune,country) values (?,?,?);"
            values = (self.locality, self.commune, self.country)
            cursor.execute(sql, values)
        
        self.id = self.get_id(cursor)
        return self
    
    def get_id(self, cursor: Cursor) -> int:
        sql = "select id from locations where locality=? and commune=? and country=?;"
        values = (self.locality, self.commune, self.country)
        return fetchOne(cursor, sql, values)

    def is_saved(self, cursor: Cursor) -> bool:
        try:
            self.get_id(cursor)
            return True
        except:
            return False


class House(object):
    def __init__(self, reference:str, title:str, current_price:int, rooms:int, bathrooms:int, size:int, location: Location, description:str) -> None:
        self.reference = reference
        self.title = title
        self.rooms = rooms 
        self.bathrooms = bathrooms
        self.size = size
        self.location = location
        self.description = description
        self.current_date = date.today()
        self.current_price = current_price

    def create_table() -> str:
        return """
                create table if not exists houses(
                    id integer primary key,
                    reference text unique,
                    title text not null,
                    rooms integer,
                    bathrooms integer,
                    size integer,
                    location_id integer not null,
                    description text,
                    constraint fk_location foreign key (location_id) references locations (id)
                );"""

    def insert(self, cursor: Cursor):
        try:
            cursor.execute("begin")
            if not self.is_saved(cursor):
                location = self.location.insert(cursor)
                sql = "insert into houses(reference, title, rooms, bathrooms, size, location_id, description) values (?,?,?,?,?,?,?);"
                values = (self.reference, self.title, self.rooms, self.bathrooms, self.size, location.id, self.description)
                cursor.execute(sql, values)
                cursor.execute("commit")
            self.id = self.get_id(cursor)
            price_date = PriceDate(self.current_price, self.current_date, self.id)
            price_date.insert(cursor)
        except Exception as e:
            print("Failed to save house " + self.reference + ": " + str(e))
            cursor.execute('rollback')

        return self

    def get_id(self, cursor: Cursor) -> int:
        sql = "select id from houses where reference=?;"
        values = (self.reference,)
        return fetchOne(cursor, sql, values)

    def is_saved(self, cursor: Cursor) -> bool:
        try:
            self.get_id(cursor)
            return True
        except:
            return False
