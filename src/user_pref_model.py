""" Class to Create a User Preferences Databases """
import sqlite3
import logging
import pathlib

logger = logging.getLogger(__name__) # Starting Logger

class UserPrefModel:
    """ class to create a user preferences database """
    # As this will likely make it easier to test during testing
    # Return Codes:
    #   True or Value indicates ran correctly
    #   False indicates operational Error

    def __init__(self, database_path:pathlib.Path, database_name: str):
        """ Initializing the database connection/creating database """
        logger.info("Initializing the database connection/creating database")
        # appending database name to database path
        self.database_location:pathlib.Path = database_path / database_name
        self.max_username_length:int = 20
        self.max_directory_length:int = 200
        # converting to posix cause sqlite3 seems to not like taking a pathlib.Path object as an input
        self.posix_database_location:str = self.database_location.as_posix()
        logger.debug("database location: %s", self.posix_database_location)

        self.create_table()
        logger.info("Database connection successful")


    def create_table(self) -> bool:
        """ Creating table in database"""
        logger.info("Creating table in database")
        try:
            with sqlite3.connect(self.posix_database_location) as base:
                base.execute(
                "CREATE TABLE IF NOT EXISTS user_preferences ("
                    "username TEXT UNIQUE PRIMARY KEY, "
                    "default_dir TEXT"
                    ")"
                )
            logger.info("Table created successfully")
            return True
        except sqlite3.OperationalError as error:
            logger.error("Table did not get created: %s", error)
            raise sqlite3.OperationalError from error

    def get_default_directory(self, user: str) -> pathlib.Path | None:
        logger.info("Getting default_directory from database")
        try:
            with sqlite3.connect(self.posix_database_location) as base:
                value:str = base.execute(
                    "SELECT default_dir FROM user_preferences WHERE username = ?",
                [user]
                ).fetchone()
                logger.debug("output value %s:", value)
                # return None is no value is present otherwise return the values found
                if value is None:
                    logger.info("No default directory found")
                    return None
                logger.info("Default directory found")
                return pathlib.Path(value[0])
        except sqlite3.OperationalError as error:
            logger.error("Directory not fetched from database")
            raise sqlite3.OperationalError from error

    def _input_check(self, user: str, directory:pathlib.Path) -> None:
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

    def add_default_directory(self, user: str, directory:pathlib.Path) -> bool:
        """ adding an entry into the user_preferences table """
        logger.info("Adding user to database")
        self._input_check(user, directory)
        try:
            with sqlite3.connect(self.posix_database_location) as base:
                directory:str = str(directory)
                base.execute(
                    "INSERT OR IGNORE INTO user_preferences(username, default_dir) VALUES (?, ?)",
                    [user, directory]
                )
                logger.info("User added successfully")
                return True
        except sqlite3.OperationalError as error:
            logger.error("OperationalError")
            raise sqlite3.OperationalError from error

    def update_default_directory(self, user:str, directory:pathlib.Path) -> bool:
        """ updating an existing entry to the user_preferences table """
        logger.info("Updating user to database")
        self._input_check(user, directory)
        try:
            with sqlite3.connect(self.posix_database_location) as base:
                directory:str = str(directory)
                base.execute(
                    "UPDATE user_preferences SET default_dir= ? WHERE username= ? ",
                    [directory, user]
                )
                logger.info("Directory Updated successfully")
                return True
        except sqlite3.OperationalError as error:
            logger.error("OperationalError")
            raise sqlite3.OperationalError from error

    def delete_default_directory(self, user:str) -> bool:
        """ deleting an existing entry from the user_preferences table """
        logger.info("Deleting directory to database")
        try:
            with sqlite3.connect(self.posix_database_location) as base:
                base.execute(
                    "DELETE FROM user_preferences WHERE username= ? ",
                    [user]
                )
                logger.info("Directory Deleted successfully")
                return True
        except sqlite3.OperationalError as error:
            logger.error("Directory not deleted")
            raise sqlite3.OperationalError from error