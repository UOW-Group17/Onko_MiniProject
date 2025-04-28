"""
Class to access the API for the Database to Create directories
for the storage of default user preferences
"""
import pathlib # finding and creating directories
import os # getting environment attributes
import sqlite3
import subprocess # Running terminal code
import logging # Logging what is happening in the code base

from src.InterfaceUserPref import InterfaceUserPref
from src.UserPreferencesDB import UserPreferencesDB # accessing the database

logger = logging.getLogger(__name__) # Starting logger

class UserPreferences(InterfaceUserPref):
    """
    To set and modify the default directory for the user to
    begin on when opening the application
    """
    # For testing purposes:
    #   True or Value means success
    #   False or exception means did not succeed
    # Unless otherwise Specified
    def __init__(self, db_location=pathlib.Path.home()) -> None:
        """ Creating dependent classes and setting up the file system for the user """
        logger.info("START: UserPreferences Database")
        db_location = pathlib.Path(db_location)
        self.db_location = db_location/ ".onko" # database directory ( "." makes file hidden in linux and macOS)
        self.user = "default" # Username for key
        # self.create_directory() #running method to create database folder
        self.database = None  # Database access
        logger.info("Finish UserPreferences Database")

    # Overwritten From Abstract Class
    def save_default_path(self, path:pathlib.Path) -> bool:
        self.create_directory()
        try:
            self.create_database_connection()
            self.set_default_directory(path)
            self.close()
        except sqlite3.OperationalError as error:
            logger.error(error)
            raise sqlite3.OperationalError from error
        return True

    # Overwritten from Abstract Class
    def default_path(self) -> pathlib.Path | None:
        self.create_database_connection()
        try:
            directory = self.get_default_directory()
            self.close()
            return directory
        except sqlite3.OperationalError as error:
            logger.error(error)
            raise sqlite3.OperationalError from error

    def create_directory(self) -> bool:
        """
        Creating a directory for the database to be stored
        directory in home directory and set to hidden
        Returns True if Windows;
        Returns False if not Windows
        """
        logger.info("START UserPreferences Directory")

        if not pathlib.Path(self.db_location).exists():
            pathlib.Path(self.db_location).mkdir(parents=True, exist_ok=False)
            logger.info("UserPreferences Directory:Directory Created")

        if os.name == "nt":
            try:
                subprocess.run(["attrib", "+h", str(self.db_location)], check=True, stderr=subprocess.PIPE, text=True)
            except subprocess.CalledProcessError as error:
                logger.error(f"ERROR: UserPreferences Directory: Setting folder to hidden failed, error: {error.stderr.strip()}")
                raise RuntimeError("Failed to set hidden attribute for UserPreferences directory") from error
            logger.info("FINISHED: UserPreferences Directory: Created Onko directory")
            return True
        else:
            logger.info("FINISHED: UserPreferences Directory: OS is not windows")
            return False

    def create_database_connection(self) -> bool:
        """
        Creating Database Connection for the class to access
        Returns True if connection made
        """
        logger.info("START: Creating Database Connection")
        try:
            self.database = UserPreferencesDB(self.db_location)
            logger.info("FINISH: Creating Database Connection")
            return True
        except sqlite3.OperationalError as error:
            raise sqlite3.OperationalError from error

    def set_default_directory(self, path:pathlib.Path) -> bool:
        """
        Setting/Changing the default directory in the Database
            Returns True if default directory updated in Database
            Returns False if default directory added to Database
        """
        logger.info("START: UserPreferences Setting directory")
        try:
            if self.database.get_default_directory(user=self.user) is not None:
                value = self.database.update_default_directory(user=self.user, directory=path)
                logger.info("FINISH: UserPreferences Setting Directory: Updated User")
            else:
                value = self.database.add_default_directory(user=self.user, directory=path)
                logger.info("FINISH: UserPreferences Setting Directory: Added User")
            return value
        except sqlite3.OperationalError as error:
            raise sqlite3.OperationalError from error

    def get_default_directory(self) -> pathlib.Path | None:
        """ Getting the user working directory"""
        logger.info("START: Getting Default Directory")
        try:
            output = self.database.get_default_directory(user=self.user)
            logger.info("FINISHED: Getting Default Directory")
        except sqlite3.OperationalError as error:
            raise sqlite3.OperationalError from error
        return output

    def close(self) -> bool:
        """ closes the database connection"""
        logger.info("Closing Database")
        try:
            value = self.database.close()
            logger.info("FINISH: Database Closing")
            return value
        except sqlite3.OperationalError as error:
            logger.error("ERROR: Database Closing")
            raise sqlite3.OperationalError from error
