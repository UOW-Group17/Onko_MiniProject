"""
To provide a set group of methods for other classes
to access the UserPreferences Class
"""
import pathlib
from abc import ABC, abstractmethod

class InterfaceUserPref(ABC):
    """
    Abstract class to define methods to
    access the UserPreferences Class
    """
    @abstractmethod
    def save_default_path(self, path:pathlib.Path) -> bool:
        """
        Saving a default path to the database
        returns true if path has been saved
        else False
        """
        pass

    @abstractmethod
    def default_path(self) -> pathlib.Path | None:
        """
        Getting a default path from the database
        A check is likely Required before using this method
        to ensure that a default path exists
        """
        pass