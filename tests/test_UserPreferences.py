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
        access:UserPreferences = UserPreferences(test_db_dir)
        yield access

    @pytest.fixture
    def fix_create_dir(self, access:UserPreferences) -> 'Generator[UserPreferences, Any, None]':
        """ Fixture to create a directory in which the tests are running in """
        access.create_directory()
        yield access

    def test_create_directory(self, access:UserPreferences) -> None:
        """ Test method for the create directory method """
        # logic is required here due to the tests needing to know which OS is being run
        test_dir:bool = access.create_directory()
        if os.name == "nt":
            assert test_dir
        else:
            assert not test_dir

    def test_create_database_connection(self, access:UserPreferences) -> None:
        """ Testing for if the Class Creates an instance of UserPreferencesDB """
        assert access.create_database_connection()

    @pytest.fixture
    def fix_setup_db(self, tmp_path, access:UserPreferences) -> Generator[UserPreferences, Any, None]:
        """ Fixture to update user preferences """
        access.create_database_connection()
        temp_dir:pathlib.Path = tmp_path / "test_db"
        access.set_default_directory(temp_dir)
        yield access

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

    def test_close(self, access:UserPreferences) -> None:
        """ Test method for the close method """
        access.create_database_connection()
        assert access.close()

if __name__ == '__main__':
    pytest.main()
