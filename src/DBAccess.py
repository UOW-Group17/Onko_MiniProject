""" Class to Create a User Preferences Database """
import sqlite3

class DBAccess:
    """ class to create a user preferences database """
    # As this will likely make it easier to test during testing
    # Return Codes:
    #   1 indicates ran correctly
    #   2 indicates operational Error
    #   3 indicates Integrity Error

    def __init__(self, database_name: str):
        """ Initializing the database connection/creating database """
        try:
            self.database = sqlite3.connect(database_name)
            self.create_table()
        except sqlite3.OperationalError:
            print("Did not create Database object")

    def create_table(self) -> int:
        """ Creating table in database"""
        try:
            cursor = self.database.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS user_preferences (username TEXT UNIQUE PRIMARY KEY, default_dir TEXT)")
            self.database.commit()
            return 1
        except sqlite3.OperationalError:
            print("Table did not get created: 'def create_table(self)' ")
            return 2

    def get_user(self, username: str) -> (str, str):
        try:
            cursor = self.database.cursor()
            value = cursor.execute(f"SELECT * FROM user_preferences WHERE username = '{username}'")
            if value is None:
                return "None", "None" # Indicates that value was not in database
            else:
                return value.fetchone() # Tuple (username, directory)

        except sqlite3.OperationalError:
            print("User not fetched from database: 'get_user('{username}')'")
            return 2

    def add_user(self, user: str, directory: str) -> int:
        """ adding an entry into the user_preferences table """
        try:
            cursor = self.database.cursor()
            cursor.execute(f"INSERT OR IGNORE INTO user_preferences VALUES ('{user}', '{directory}')")
            self.database.commit()
            return 1
        except sqlite3.OperationalError:
            return 2

    def update_user(self, username:str, directory:str) -> int:
        """ updating an existing entry to the user_preferences table """
        try:
            cursor = self.database.cursor()
            cursor.execute(f"UPDATE user_preferences SET default_dir='{directory}' WHERE username='{username}'")
            self.database.commit()
            return 1
        except sqlite3.OperationalError:
            print("User not updated: 'update_user(self, username: str, directory:str)'")
            return 2

    def delete_user(self, username:str) -> int:
        """ deleting an existing entry from the user_preferences table """
        try:
            cursor = self.database.cursor()
            cursor.execute(f"DELETE FROM user_preferences WHERE username='{username}'")
            self.database.commit()
            return 1
        except sqlite3.OperationalError:
            print("User not deleted: 'delete_user(self, username: str):'")
            return 2
