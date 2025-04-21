""" Test File for the DBAccess file """
import pytest
import logging
from src.UserPreferencesDB import UserPreferencesDB

logging.debug("UnitTests: UserPreferencesDB")

@pytest.fixture
def access(tmp_path):
    """ Fixture to set up and Teardown tests """
    logging.info('Setting up test DB fixture')
    db_path = tmp_path / "test_Database.db"
    db_access = UserPreferencesDB(str(db_path))
    db_access.create_table()
    yield db_access
    db_access.database.close()
    db_path.unlink()
    logging.info('Teardown test DB fixture')

class TestUserPreferencesDB:
    """ Test Class for DBAccess """
    def test_create_table(self, access):
        """ Test Method for create Table method """
        assert access.create_table() == 1

    def test_get_user(self, access):
        """ Test Method for get User method """
        access.add_user('Adam', "~")
        assert access.get_user("Adam") == "~"
        assert access.get_user("Aiden") is None

    def test_add_user(self, access):
        """ Test Method for add User method """
        assert access.add_user("Bert", "~") == 1
        assert access.get_user("Bert") == "~"
        assert access.add_user("Bert", "~/Documents") == 1
        assert access.get_user("Bert") != "~/Documents"
        assert access.add_user("", "~") != 1
        assert access.add_user("ValidUser", "") != 1
        long_username = "u" * 300
        assert access.add_user(long_username, "~") != 1
        long_username_2 = "u" * 50
        assert access.add_user(long_username_2, "~") == 1
        long_dir = "p" * 300
        assert access.add_user("ValidUser", long_dir) != 1
        long_dir_2 = "p" * 50
        assert access.add_user("ValidUser", long_dir_2) == 1

    def test_update_user(self, access):
        """ Test Method for update User method """
        access.add_user("Chuck", "~")
        assert access.update_user("Chuck", "~/.user") == 1
        assert access.update_user("Cho", "~/Documents") == 1
        assert access.update_user("", "~") != 1
        assert access.update_user("ValidUser", "") != 1
        long_username = "u" * 300
        assert access.update_user(long_username, "~") != 1
        long_dir = "p" * 300
        assert access.update_user("ValidUser", long_dir) != 1

    def test_delete_user(self, access):
        """ Test Method for delete User method """
        access.add_user("Dan", "~/")
        assert access.delete_user("Dan") == 1
        assert access.get_user("Dan") != ("Dan", "~/")
        assert access.delete_user("Dom") == 1

    def test_close(self, access):
        """ closes database connection """
        assert access.close() == 1

if __name__ == "__main__":
    pytest.main()
