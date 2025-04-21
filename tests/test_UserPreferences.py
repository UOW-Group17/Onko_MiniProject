import pytest
import logging
import os
from src.UserPreferences import UserPreferences
from src.UserPreferencesDB import UserPreferencesDB

logging.debug("UnitTests: UserPreferences")

@pytest.fixture
def access(tmp_path):
    """ Fixture to access class """
    test_db_dir = tmp_path / "test_db"
    test_db_dir.mkdir()
    access = UserPreferences(str(test_db_dir))
    yield access

class TestUserPreferences:
    """ Test Class for UserPreferences """
    def test_create_directory(self, access):
        """ Test method for the create directory method """
        # logic is required here due to the tests needing to know which OS is being run
        test_dir = access.create_directory()
        if os.name == "nt":
            assert test_dir == "windows"
            assert test_dir != "notWindows"
        else:
            assert test_dir == "notWindows"
            assert test_dir != "windows"

    def test_create_database_connection(self, access):
        """ Testing for if the Class Creates an instance of UserPreferencesDB """
        assert access.create_database_connection() == "connectionMade"


    def test_set_default_directory(self, access):
        """ Test method for the set_default_directory method """
        access.create_database_connection()

        """ Testing to see if adding directory branch works """
        test_dir_add = access.set_default_directory()
        assert test_dir_add == "added"
        assert test_dir_add != "updated"

    def test_update_default_directory(self, access):
        """ Testing to see if updating Directory branch works """
        test_dir_up = access.set_default_directory()
        test_dir_up = access.set_default_directory()
        assert test_dir_up == "updated"
        assert test_dir_up != "added"

    def test_get_default_directory(self, access):
        """ Test method for the get_default_directory method """
        access.create_database_connection()
        access.set_default_directory()
        assert access.get_default_directory() == os.getcwd()

    def test_close(self, access):
        """ Test method for the close method """
        access.create_database_connection()
        assert access.close() == 1

if __name__ == '__main__':
    pytest.main()
