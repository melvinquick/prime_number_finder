import os
import sqlite3


class DatabaseHandler:
    def __init__(self, db_name="prime_data.db"):
        self.db_dir = os.path.expanduser("~/.config/prime_number_finder")
        os.makedirs(self.db_dir, exist_ok=True)

        self.db_name = os.path.join(self.db_dir, db_name)
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(e)
        return conn

    def create_tables(self):
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
        except sqlite3.Error as e:
            print(e)

    def load_prime_numbers(self):
        self.cursor.execute("SELECT number FROM primes ORDER BY number ASC")
        return [row[0] for row in self.cursor.fetchall()]

    def save_found_prime(self, prime):
        try:
            self.cursor.execute("INSERT INTO primes (number) VALUES (?)", (prime,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
        except sqlite3.Error as e:
            print(e)

    def load_current_number(self):
        self.cursor.execute("SELECT value FROM current_number WHERE id = 1")
        result = self.cursor.fetchone()
        return result[0] if result else 2

    def save_current_number(self, number):
        try:
            self.cursor.execute(
                "UPDATE current_number SET value = ? WHERE id = 1", (number,)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
