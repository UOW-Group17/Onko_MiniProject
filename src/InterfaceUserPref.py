"""
To provide a set group of methods for other classes
to access the UserPreferences Class
"""
from abc import ABC, abstractmethod

class InterfaceUserPref(ABC):
    """
    Abstract class to provide methods the to define
    the accessible methods of the UserPreferences Class
    """
    @abstractmethod
    def check_if_path_exists(self) -> bool:
        """ Check if there exists a saved path """
        pass

    @abstractmethod
    def save_default_path(self, path:str) -> None:
        """ Saving a default path to the database """
        pass

    @abstractmethod
    def load_default_path(self) -> str:
        """ Getting a default path from the database"""
        pass