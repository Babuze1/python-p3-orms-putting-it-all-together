
import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None 

    def create_table():
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    def drop_table():
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("UPDATE dogs SET name=?, breed=? WHERE id=?", (self.name, self.breed, self.id))
            CONN.commit()    

    
    @classmethod
    def create(cls, name, breed):
        # Create a new row in the database and return a Dog instance
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, db_row):
        # Create a Dog instance from a database row
        id, name, breed = db_row
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog:
            return dog
        else:
            return cls.create(name, breed)

    def update(self):
        if self.id:
            sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()
    