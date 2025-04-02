from sqlite3 import connect, Error, IntegrityError
from os import path


class DatabaseHandler:
    def __init__(self, db_name="prime_data.db"):
        self.db_name = self.get_file_path(db_name)
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()
        self.create_tables()

    def get_file_path(self, filename):
        return path.join(path.dirname(__file__), "resources/data", filename)

    def create_connection(self):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = connect(self.db_name)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS primes (
                    number INTEGER PRIMARY KEY
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS current_number (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    value INTEGER NOT NULL
                )
            """)
            self.cursor.execute("SELECT COUNT(*) FROM current_number")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute(
                    "INSERT INTO current_number (id, value) VALUES (1, 2)"
                )
            self.conn.commit()
        except Error as e:
            print(e)

    def load_prime_numbers(self):
        """Load prime numbers from the database."""
        self.cursor.execute("SELECT number FROM primes ORDER BY number ASC")
        primes = [row[0] for row in self.cursor.fetchall()]
        return primes

    def save_found_prime(self, prime):
        """Save a newly found prime number to the database."""
        try:
            self.cursor.execute("INSERT INTO primes (number) VALUES (?)", (prime,))
            self.conn.commit()
        except IntegrityError:
            pass
        except Error as e:
            print(e)

    def load_current_number(self):
        """Load the current number from the database."""
        self.cursor.execute("SELECT value FROM current_number WHERE id = 1")
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 2

    def save_current_number(self, number):
        """Save the current number to the database."""
        try:
            self.cursor.execute(
                "UPDATE current_number SET value = ? WHERE id = 1", (number,)
            )
            self.conn.commit()
        except Error as e:
            print(e)

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
