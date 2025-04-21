""" Class to Create a User Preferences Databases """
import sqlite3
import logging

logger = logging.getLogger(__name__) # Starting Logger

class UserPreferencesDB:
    """ class to create a user preferences database """
    # As this will likely make it easier to test during testing
    # Return Codes:
    #   1 indicates ran correctly
    #   2 indicates operational Error

    def __init__(self, database_name: str):
        """ Initializing the database connection/creating database """
        logger.info("Initializing the database connection/creating database")
        try:
            self.database = sqlite3.connect(database_name)
            self.create_table()
            logger.info("Database connection successful")
        except sqlite3.OperationalError:
            logger.error("Did not create Database object")

    def create_table(self) -> int:
        """ Creating table in database"""
        logger.info("Creating table in database")
        try:
            cursor = self.database.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS user_preferences ("
                    "username TEXT UNIQUE PRIMARY KEY, "
                    "default_dir TEXT"
                ")"
            )
            self.database.commit()
            logger.info("Table created successfully")
            return 1
        except sqlite3.OperationalError:
            logger.error("Table did not get created")
            return 2

    def get_user(self, user: str) -> str:
        logger.info("Getting User from database")
        try:
            cursor = self.database.cursor()
            value = cursor.execute(
                "SELECT * FROM user_preferences WHERE username = ?",
                [user]
            ).fetchone()
            # return None is no value is present otherwise return the values found
            if value is None:
                logger.error("User not found")
                return None
            else:
                logger.info("User is found")
                return value[1]

        except sqlite3.OperationalError:
            logger.error("User not fetched from database")
            return None

    def add_user(self, user: str, directory: str) -> int:
        """ adding an entry into the user_preferences table """
        logger.info("Adding user to database")
        if (
            not user
            or not directory
            or user.__len__() > 50
            or directory.__len__() > 50
        ):
            logger.error("invalid user name")
            return 2
        try:
            cursor = self.database.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO user_preferences VALUES (?, ?)",
                [user, directory]
            )
            self.database.commit()
            logger.info("User added successfully")
            return 1
        except sqlite3.OperationalError:
            logger.error("OperationalError")
            return 2

    def update_user(self, user:str, directory:str) -> int:
        """ updating an existing entry to the user_preferences table """
        logger.info("Updating user to database")
        if (
            not user
            or not directory
            or user.__len__() > 50
            or directory.__len__() > 50
        ):
            logger.error("invalid directory")
            return 2
        try:
            cursor = self.database.cursor()
            cursor.execute(
                "UPDATE user_preferences SET default_dir= ? WHERE username= ? ",
                [directory, user]
            )
            self.database.commit()
            logger.info("user Updated successfully")
            return 1
        except sqlite3.OperationalError:
            logger.error("User not updated")
            return 2

    def delete_user(self, user:str) -> int:
        """ deleting an existing entry from the user_preferences table """
        logger.info("Deleting user to database")
        try:
            cursor = self.database.cursor()
            cursor.execute(
                "DELETE FROM user_preferences WHERE username= ? ",
                [user]
            )
            self.database.commit()
            logger.info("User Deleted successfully")
            return 1
        except sqlite3.OperationalError:
            logger.error("User not deleted")
            return 2

    def close(self) -> int:
        """ Closing the database connection """
        self.database.close()
        return 1