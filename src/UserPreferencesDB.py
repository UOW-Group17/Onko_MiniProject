""" Class to Create a User Preferences Databases """
import sqlite3
import logging
import pathlib

logger = logging.getLogger(__name__) # Starting Logger

class UserPreferencesDB:
    """ class to create a user preferences database """
    # As this will likely make it easier to test during testing
    # Return Codes:
    #   True or Value indicates ran correctly
    #   False indicates operational Error

    def __init__(self, database_name: pathlib.Path):
        """ Initializing the database connection/creating database """
        logger.info("Initializing the database connection/creating database")
        try:
            self.database = sqlite3.connect(database_name)
            self.create_table()
            logger.info("Database connection successful")
        except sqlite3.OperationalError as error:
            logger.error("Did not create Database object")
            raise sqlite3.OperationalError from error

    def create_table(self) -> bool:
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
            return True
        except sqlite3.OperationalError as error:
            logger.error("Table did not get created")
            raise sqlite3.OperationalError from error

    def get_default_directory(self, user: str) -> pathlib.Path | None:
        logger.info("Getting default_directory from database")
        try:
            cursor = self.database.cursor()
            value = cursor.execute(
                "SELECT * FROM user_preferences WHERE username = ?",
                [user]
            ).fetchone()
            # return None is no value is present otherwise return the values found
            if value is None:
                return None
            logger.info("User is found")
            return pathlib.Path(value[1])
        except sqlite3.OperationalError as error:
            logger.error("User not fetched from database")
            raise sqlite3.OperationalError from error

    def add_default_directory(self, user: str, directory:pathlib.Path) -> bool:
        """ adding an entry into the user_preferences table """
        logger.info("Adding user to database")
        if (
            not user
            or directory is None
            or user.__len__() > 15
            or directory == pathlib.Path("")
            or len(str(directory)) > 200
        ):
            logger.error("Invalid User or Directory Name")
            raise RuntimeError("Error: Invalid Directory Name")
        try:
            cursor = self.database.cursor()
            directory = str(directory)
            cursor.execute(
                "INSERT OR IGNORE INTO user_preferences(username, default_dir) VALUES (?, ?)",
                [user, directory]
            )
            self.database.commit()
            logger.info("User added successfully")
            return True
        except sqlite3.OperationalError as error:
            logger.error("OperationalError")
            raise sqlite3.OperationalError from error

    def update_default_directory(self, user:str, directory:pathlib.Path) -> bool:
        """ updating an existing entry to the user_preferences table """
        logger.info("Updating user to database")
        if (
            not user
            or directory is None
            or user.__len__() > 50
            or directory == pathlib.Path("")
            or len(str(directory)) > 200
        ):
            logger.error("Invalid Directory Name")
            raise RuntimeError("Error: Invalid Directory Name")
        try:
            cursor = self.database.cursor()
            directory = str(directory)
            cursor.execute(
                "UPDATE user_preferences SET default_dir= ? WHERE username= ? ",
                [directory, user]
            )
            self.database.commit()
            logger.info("Directory Updated successfully")
            return True
        except sqlite3.OperationalError as error:
            logger.error("OperationalError")
            raise sqlite3.OperationalError from error

    def delete_default_directory(self, user:str) -> bool:
        """ deleting an existing entry from the user_preferences table """
        logger.info("Deleting directory to database")
        try:
            cursor = self.database.cursor()
            cursor.execute(
                "DELETE FROM user_preferences WHERE username= ? ",
                [user]
            )
            self.database.commit()
            logger.info("Directory Deleted successfully")
            return True
        except sqlite3.OperationalError as error:
            logger.error("Directory not deleted")
            raise sqlite3.OperationalError from error

    def close(self) -> bool:
        """ Closing the database connection """
        logger.info("Closing the database connection")
        try:
            self.database.close()
            logger.info("Database connection closed")
            return True
        except sqlite3.OperationalError as error:
            logger.error("SQL:OperationalError")
            raise sqlite3.OperationalError from error