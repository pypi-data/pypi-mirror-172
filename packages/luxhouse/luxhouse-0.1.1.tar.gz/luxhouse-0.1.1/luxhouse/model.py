from datetime import datetime
from sqlite3 import Cursor

class PriceDate(object):
    def __init__(self, price:int, date:datetime, house_id:int) -> None:
        self.price = price
        self.date = date
        self.house_id = house_id

    def create_table():
        return """
            create table if not exists price_date(
                id integer primary key,
                price integer not null,
                date date not null,
                house_id integer not null,
                unique(price,date, house_id)
                foreign key (house_id) references houses (id)
            );"""
    
    def insert(self, cursor:Cursor):
        try:
            sql = "insert into price_date(price,date,house_id) values (?,?,?);"
            values = (self.price, self.date, self.house_id)
            cursor.execute(sql, values)
        except:
            pass
        
        self.id = self.get_id(cursor)
        return self

    def get_id(self, cursor: Cursor):
        sql = "select id from price_date where price={} and date='{}' and house_id={};".format(self.price, self.date, self.house_id)
        cursor.execute(sql)
        records = cursor.fetchone()
        return records[0]

class Location(object):
    def __init__(self, city:str, province:str) -> None:
        self.city = city
        self.province = province

    def create_table():
        return """
            create table if not exists locations(
                id integer primary key,
                city text not null,
                province text not null,
                unique(city,province)
            );"""

    def insert(self, cursor: Cursor):
        try:
            sql = "insert into locations(city,province) values (?,?);"
            values = (self.city, self.province)
            cursor.execute(sql, values)
        except:
            pass
        
        self.id = self.get_id(cursor)
        return self
    
    def get_id(self, cursor: Cursor):
        sql = "select id from locations where city='{}' and province='{}';".format(self.city, self.province)
        cursor.execute(sql)
        records = cursor.fetchone()
        return records[0]


class House(object):
    def __init__(self, reference:str, title:str, current_price:int, rooms:int, size:int, location: Location, description:str) -> None:
        self.reference = reference
        self.title = title
        self.rooms = rooms 
        self.size = size
        self.location = location
        self.description = description
        self.current_date = datetime.today()
        self.current_price = current_price

    def create_table():
        return """
                create table if not exists houses(
                    id integer primary key,
                    reference text key,
                    title text not null,
                    rooms integer not null,
                    size integer not null,
                    location_id integer not null,
                    description text not null,
                    foreign key (location_id) references location (id)
                );"""

    def insert(self, cursor: Cursor):
        location = self.location.insert(cursor)

        try:
            sql = "insert into houses(reference, title, rooms, size, location_id, description) values (?,?,?,?,?,?);"
            values = (self.reference, self.title, self.rooms, self.size, location.id, self.description)
            cursor.execute(sql, values)
        except:
            pass

        self.id = self.get_id(cursor)

        price_date = PriceDate(self.current_price, self.current_date, self.id)
        price_date.insert(cursor)

        return self


    def get_id(self, cursor: Cursor):
        sql = "select id from houses where reference='{}';".format(self.reference)
        cursor.execute(sql)
        records = cursor.fetchone()
        return records[0]