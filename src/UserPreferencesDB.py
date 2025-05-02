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
        self.database_name:pathlib.Path = database_name
        self.max_username_length:int = 20
        self.max_directory_length:int = 200
        try:
            self.database:sqlite3.dbapi2 = sqlite3.connect(database_name)
            self.create_table()
            logger.info("Database connection successful")
        except sqlite3.OperationalError as error:
            logger.error("Did not create Database object")
            raise sqlite3.OperationalError from error


    def create_table(self) -> bool:
        """ Creating table in database"""
        logger.info("Creating table in database")
        try:
            with self.database as base:
                cursor:sqlite3.Cursor = base.cursor()
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
            with self.database as base:
                cursor:sqlite3.Cursor = base.cursor()
                value:str = cursor.execute(
                    "SELECT default_dir FROM user_preferences WHERE username = ?",
                [user]
                ).fetchone()
            # return None is no value is present otherwise return the values found
                if value is None:
                    return None
                logger.info("User is found")
                return pathlib.Path(value[0])
        except sqlite3.OperationalError as error:
            logger.error("User not fetched from database")
            raise sqlite3.OperationalError from error

    def input_check(self, user: str, directory:pathlib.Path) -> bool:
        """ To check is the lengths of the inputs are appropriate and exist """
        if (
            not user
            or directory is None
            or user.__len__() > self.max_username_length
            or directory == pathlib.Path("")
            or len(str(directory)) > self.max_directory_length
        ):
            logger.error("Invalid User or Directory Name")
            raise RuntimeError("Error: Invalid Directory Name")
        return True

    def add_default_directory(self, user: str, directory:pathlib.Path) -> bool:
        """ adding an entry into the user_preferences table """
        logger.info("Adding user to database")
        self.input_check(user, directory)
        try:
            with self.database as base:
                cursor:sqlite3.Cursor = base.cursor()
                directory:str = str(directory)
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
        self.input_check(user, directory)
        try:
            with self.database as base:
                cursor:sqlite3.Cursor = base.cursor()
                directory:str = str(directory)
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
            with self.database as base:
                cursor:sqlite3.Cursor = base.cursor()
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