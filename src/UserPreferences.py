"""
Class to access the API for the Database to Create directories
for the storage of default user preferences
"""
import pathlib # finding and creating directories
import os # getting environment attributes
import subprocess # Running terminal code
import logging # Logging what is happening in the code base
from src.UserPreferencesDB import UserPreferencesDB # accessing the database


logger = logging.getLogger(__name__) # Starting logger

class UserPreferences:
    """
    To set and modify the default directory for the user to
    begin on when opening the application
    """
    # Return str used for testing so we can see what branches are used

    def __init__(self, db_location=pathlib.Path.home(), db_model=None) -> None:
        """ Creating dependent classes and setting up the file system for the user """
        logger.info("START: UserPreferences Database")
        self.db_location = f"{db_location}/.onko" # database directory ( "." makes file hidden in linux and macOS)
        self.user = "default" # Username for key
        # self.create_directory() #running method to create database folder
        self.database = None  # Database access
        logger.info("Finish UserPreferences Database")

    def create_directory(self) -> str:
        """
        Creating a directory for the database to be stored
        directory in home directory and set to hidden
        """
        logger.info("START UserPreferences Directory")
        if not pathlib.Path(self.db_location).exists():
            pathlib.Path(self.db_location).mkdir(parents=True, exist_ok=False)
            logger.info("UserPreferences Directory:Directory Created")
        if os.name == "nt":
            try:
                subprocess.run(["attrib", "+h", str(self.db_location)], check=True, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as error:
                logger.error(f"ERROR: UserPreferences Directory: Setting folder to hidden failed, error: {error.stderr.decode().strip()}")
                raise RuntimeError("Failed to set hidden attribute for UserPreferences directory") from error
            logger.info("FINISHED: UserPreferences Directory: Created Onko directory")
            return "windows"
        else:
            logger.info("FINISHED: UserPreferences Directory: Onko directory already exists")
            return "notWindows"

    def create_database_connection(self) -> str:
        """ Creating Database Connection for the class to access """
        logger.info("START: Creating Database Connection")
        self.database = UserPreferencesDB(self.db_location)
        logger.info("FINISH: Creating Database Connection")
        return "connectionMade"

    def set_default_directory(self) -> str:
        """ Setting/Changing the default directory in the Database"""
        self.create_database_connection()
        logger.info("START: UserPreferences Setting directory")
        working_dir = os.getcwd() # getting the current working directory
        if self.database.get_user(user=self.user) is not None:
            self.database.update_user(user=self.user, directory=working_dir)
            logger.info("FINISH: UserPreferences Setting Directory: Updated User")
            return "updated"
        else:
            self.database.add_user(user=self.user, directory=working_dir)
            logger.info("FINISH: UserPreferences Setting Directory: Added User")
            return "added"

    def get_default_directory(self) -> str:
        """ Getting the user working directory"""
        logger.info("START: Getting Default Directory")
        output = self.database.get_user(user=self.user)
        logger.info("FINISHED: Getting Default Directory")
        return output

    def close(self) -> int:
        self.database.close()
        return 1