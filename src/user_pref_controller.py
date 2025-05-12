"""
Class to access the API for the Database to Create directories
for the storage of default user preferences
"""
import pathlib # finding and creating directories
import os # getting environment attributes
import sqlite3
import subprocess # Running terminal code
import logging # Logging what is happening in the code base

from src.user_pref_interface import UserPrefInterface
from src.user_pref_model import UserPrefModel # accessing the database

logger = logging.getLogger(__name__) # Starting logger

class UserPrefController(UserPrefInterface):
    """
    To set and modify the default directory for the user to
    begin on when opening the application
    """
    # For testing purposes:
    #   True or Value means success
    #   False or exception means did not succeed
    # Unless otherwise Specified
    def __init__(self, database_name:str="user_pref.db", database_location:pathlib.Path=pathlib.Path.home()) -> None:
        """ Creating dependent classes and setting up the file system for the user """
        logger.info("START: UserPreferences Database")
        logger.debug("database_location: %s, database_name: %s", database_location, database_name)
        self.db_location:pathlib.Path = database_location / ".onko" # database directory ( "." makes file hidden in linux and macOS)
        self.create_directory()
        self.database_name:str=database_name
        logger.debug("DB Location: %s, DB Name: %s", self.db_location, self.database_name)
        self.user:str = "default" # Username for key
        self.database:UserPrefModel = None  # Database access
        logger.info("Finish UserPreferences Database")

    # Overwritten From Abstract Class
    def save_default_path(self, path:pathlib.Path) -> bool:
        """
        Saving a default path to the database
        returns true if path has been saved
        else False
        """
        self.create_directory()
        logger.debug("path %s", path)
        try:
            self.create_database_connection()
            self.set_default_directory(path)
        except sqlite3.OperationalError as error:
            error_message = f"Failed to save default directory in save_default_path: {error}"
            logger.error(error_message)
            raise sqlite3.OperationalError(error_message) from error
        return True

    # Overwritten from Abstract Class
    def default_path(self) -> pathlib.Path | None:
        """
        Getting a default path from the database
        A check is likely Required before using this method
        to ensure that a default path exists
        """
        self.create_database_connection()
        try:
            directory:pathlib.Path = self.get_default_directory()
            return directory
        except sqlite3.OperationalError as error:
            logger.error(error)
            raise sqlite3.OperationalError from error

    def create_directory(self) -> bool:
        """
        Creating a directory for the database to be stored
        directory in home directory and set to hidden
        Returns True for success;
        """
        logger.info("START UserPreferences Directory")

        # Creating To store User-Preferences
        if not pathlib.Path(self.db_location).exists():
            pathlib.Path(self.db_location).mkdir(parents=True, exist_ok=False)
            logger.info("UserPreferences Directory: Directory Created")

        # Skipping the rest of the function if the OS is not Windows
        if os.name != "nt":
            logger.info("FINISHED: UserPreferences Directory: OS is not windows")
            return True
        # Making Folder Hidden for Windows
        try:
            subprocess.run(["attrib", "+h", str(self.db_location)], check=True, stderr=subprocess.PIPE, text=True)
            logger.info("FINISHED: UserPreferences Directory: Windows Directory hidden")
        except subprocess.CalledProcessError as error:
            logger.warning(f"WARNING: UserPreferences Directory: Setting folder to hidden failed (non-critical), error: {error.stderr.strip()}. Continuing without hidden attribute.")
        return True

    def create_database_connection(self) -> None:
        """
        Creating Database Connection for the class to access
        """
        logger.info("START: Creating Database Connection")
        try:
            logger.debug("database: %s", str(self.database))
            if self.database is None:
                self.database:UserPrefModel = UserPrefModel(database_path=self.db_location, database_name=self.database_name)
                logger.debug("database: %s", self.database.posix_database_location)
            logger.info("FINISH: Creating Database Connection")
        except sqlite3.OperationalError as error:
            raise sqlite3.OperationalError from error

    def set_default_directory(self, path: pathlib.Path) -> bool:
        """
        Sets or changes the default directory in the database.

        Note:
        Ensure that UserPrefModel.update_default_directory and UserPrefModel.add_default_directory
        return Boolean values consistently representing the result of the operation.
        """
        logger.info("START: UserPrefController Setting directory")
        try:
            if self.database.get_default_directory(user=self.user) is not None:
                value:bool = self.database.update_default_directory(user=self.user, directory=path)
                logger.info("FINISH: UserPreferences Setting Directory: Updated User")
            else:
                value:bool = self.database.add_default_directory(user=self.user, directory=path)
                logger.info("FINISH: UserPreferences Setting Directory: Added User")
            return value
        except sqlite3.OperationalError as error:
            raise sqlite3.OperationalError from error

    def get_default_directory(self) -> pathlib.Path | None:
        """ Getting the user working directory"""
        logger.info("START: Getting Default Directory")
        try:
            output:pathlib.Path = self.database.get_default_directory(user=self.user)
            logger.info("FINISHED: Getting Default Directory")
        except sqlite3.OperationalError as error:
            raise sqlite3.OperationalError from error
        return output
