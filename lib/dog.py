import sqlite3

CONN = sqlite3.connect('dogs.db')
CURSOR = CONN.cursor()

class Dog:
  
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            sql = """
                UPDATE dogs
                SET name = ?
                WHERE id = ?
            """

            CURSOR.execute(sql, (self.name, self.id))

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    sql = """"
        SELECT *
        FROM dogs
    """

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM dogs')
        rows = CURSOR.fetchall()
        dogs = []
        for row in rows:
            dog = Dog.new_from_db(row)
            dogs.append(dog)
        return dogs
    
    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name=?", (name,))
        row = CURSOR.fetchone()
        if row is not None:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, dog_id):
        CURSOR.execute("SELECT * FROM dogs WHERE id=?", (dog_id,))
        row = CURSOR.fetchone()
        if row is not None:
            return cls.new_from_db(row)
        return None
    
    #Bonus Deliverables
    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog is not None:
            return dog
        return cls.create(name, breed)
    
    def update(self):
        if self.id is not None:
            sql = """
                UPDATE dogs
                SET name = ?
                WHERE id = ?
            """

            CURSOR.execute(sql, (self.name, self.id))
            CONN.commit()
            return True
        return False
    
    pass
