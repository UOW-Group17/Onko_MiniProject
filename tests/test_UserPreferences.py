from typing import Any, Generator
import pytest
import logging
from src.UserPreferences import UserPreferences
from src.UserPreferencesDB import UserPreferencesDB
import sqlite3
import pathlib

logging.debug("UnitTests: UserPreferences")

class TestUserPreferences:
    """ Test Class for UserPreferences """
    @pytest.fixture
    def access(self, tmp_path:pathlib.Path) -> Generator[UserPreferences, Any, None]:
        """ Fixture to set up the Database environment for the tests to run in """
        test_db_dir:pathlib.Path = tmp_path / "test_db"
        test_db_dir.mkdir()
        access:UserPreferences = UserPreferences(test_db_dir)
        yield access

    @pytest.fixture
    def fix_create_dir(self, access:UserPreferences) -> 'Generator[UserPreferences, Any, None]':
        """ Fixture to create a directory in which the tests are running in """
        access.create_directory()
        yield access

    @pytest.fixture
    def fix_setup_db(self, tmp_path, access:UserPreferences) -> Generator[UserPreferences, Any, None]:
        """ Fixture to update user preferences """
        access.create_database_connection()
        temp_dir:pathlib.Path = tmp_path / "test_db"
        access.set_default_directory(temp_dir)
        yield access

    def test_create_directory(self, access:UserPreferences) -> None:
        """ Test method for the create directory method """
        # Need to figure out how to test between the different branches of this will return true if success but doesn't
        # interrogate between which OS branch it goes down
        assert access.create_directory()

    def test_create_database_connection(self, access:UserPreferences) -> None:
        """ Testing for if the Class Creates an instance of UserPreferencesDB """
        assert access.create_database_connection()
        result = access.create_database_connection()
        assert result
        assert isinstance(access.database, UserPreferencesDB)

    def test_set_default_directory(self, tmp_path, access:UserPreferences) -> None:
        """ Testing to see if Adding Directory branch works """
        access.create_database_connection()
        temp_dir:pathlib.Path = tmp_path / "test_db"
        assert access.set_default_directory(temp_dir)

    def test_update_default_directory(self, tmp_path, fix_setup_db:UserPreferences) -> None:
        """ Testing to see if updating Directory branch works """
        temp_dir:pathlib.Path = tmp_path / "test_db"
        assert fix_setup_db.set_default_directory(temp_dir)

    def test_get_default_directory(self, tmp_path, fix_setup_db:UserPreferences) -> None:
        """ Test method for the get_default_directory method """
        temp_dir: pathlib.Path = tmp_path / "test_db"
        assert fix_setup_db.get_default_directory() == temp_dir
        temp_dir2: pathlib.Path = tmp_path / "test_db2"
        with pytest.raises(sqlite3.OperationalError) as invalid_dir:
            new_db_dir:UserPreferences = UserPreferences(temp_dir2)
            new_db_dir.create_database_connection()
            new_db_dir.get_default_directory()
        assert isinstance(invalid_dir.value, sqlite3.OperationalError)

if __name__ == '__main__':
    pytest.main()
