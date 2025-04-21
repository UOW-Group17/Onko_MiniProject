from typing import Any, Generator

import pytest
import logging
import os
from src.UserPreferences import UserPreferences
import pathlib

logging.debug("UnitTests: UserPreferences")

class TestUserPreferences:
    """ Test Class for UserPreferences """
    @pytest.fixture
    def access(self, tmp_path:pathlib.Path) -> Generator[UserPreferences, Any, None]:
        """ Fixture to set up the Database environment for the tests to run in """
        test_db_dir:pathlib.Path = tmp_path / "test_db"
        test_db_dir.mkdir()
        access:UserPreferences = UserPreferences(str(test_db_dir))
        yield access

    @pytest.fixture
    def fix_create_dir(self, access:UserPreferences) -> 'Generator[UserPreferences, Any, None]':
        """ Fixture to create a directory in which the tests are running in """
        access.create_directory()
        yield access

    def test_create_directory(self, access:UserPreferences) -> None:
        """ Test method for the create directory method """
        # logic is required here due to the tests needing to know which OS is being run
        test_dir:str = access.create_directory()
        if os.name == "nt":
            assert test_dir == "windows"
            assert test_dir != "notWindows"
        else:
            assert test_dir == "notWindows"
            assert test_dir != "windows"

    def test_create_database_connection(self, access:UserPreferences) -> None:
        """ Testing for if the Class Creates an instance of UserPreferencesDB """
        assert access.create_database_connection() == "connectionMade"

    @pytest.fixture
    def fix_setup_db(self, access:UserPreferences) -> Generator[UserPreferences, Any, None]:
        """ Fixture to update user preferences """
        access.create_database_connection()
        access.set_default_directory()
        yield access

    def test_set_default_directory(self, access:UserPreferences) -> None:
        """ Testing to see if Adding Directory branch works """
        access.create_database_connection()
        test_dir_add:str = access.set_default_directory()
        assert test_dir_add == "added"
        assert test_dir_add != "updated"

    def test_update_default_directory(self, fix_setup_db:UserPreferences) -> None:
        """ Testing to see if updating Directory branch works """
        test_dir_up:str = fix_setup_db.set_default_directory()
        assert test_dir_up == "updated"
        assert test_dir_up != "added"

    def test_get_default_directory(self, fix_setup_db:UserPreferences) -> None:
        """ Test method for the get_default_directory method """
        assert fix_setup_db.get_default_directory() == os.getcwd()

    def test_close(self, access:UserPreferences) -> None:
        """ Test method for the close method """
        access.create_database_connection()
        assert access.close() == 1

if __name__ == '__main__':
    pytest.main()
