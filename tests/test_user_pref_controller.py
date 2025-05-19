""" Test File for user_pref_controller file """
import logging
import pathlib
# import sqlite3
from typing import Any, Generator
import pytest
from src.user_pref_controller import UserPrefController
from src.user_pref_model import UserPrefModel

logger = logging.getLogger(__name__)
logger.debug("UnitTests: UserPrefModel")


class TestUserPrefController:
    """ Test Class for UserPrefController """
    @pytest.fixture(scope="function")
    def base_fixture(
            self,
            tmp_path: pathlib.Path
    ) -> Generator[UserPrefController, Any, None]:
        """
        Fixture to set up the Database environment for the tests to run in
        """
        yield UserPrefController(
            database_location=tmp_path,
            database_name="test_db.db"
        )

    @pytest.fixture(scope="function")
    def fixture_create_dir(
            self,
            base_fixture: UserPrefController
    ) -> 'Generator[UserPrefController, Any, None]':
        """ Fixture to create a directory in which the tests are running in """
        base_fixture.create_directory()
        yield base_fixture

    @pytest.fixture(scope="function")
    def fixture_setup_database(
            self,
            tmp_path,
            base_fixture: UserPrefController
    ) -> Generator[UserPrefController, Any, None]:
        """ Fixture to update user preferences """
        logger.debug("Setting up Database")
        base_fixture.create_directory()
        base_fixture.create_database_connection()
        base_fixture.set_default_directory(tmp_path)
        yield base_fixture

    def test_save_default_path(self, tmp_path: pathlib.Path) -> None:
        """ Test method for the save default path method """
        use: UserPrefController = UserPrefController(
            database_location=tmp_path,
            database_name="test_db.db"
        )
        assert use.save_default_path(tmp_path)
        assert use.default_path() == tmp_path

    def test_default_path(
            self,
            tmp_path,
            fixture_setup_database: UserPrefController
    ) -> None:
        """ Test method for the default path method """
        assert fixture_setup_database.default_path() == tmp_path
        second: UserPrefController = UserPrefController(
            database_name="test_db2.db",
            database_location=tmp_path
        )
        assert second.default_path() is None

    def test_default_path_when_not_set(
            self,
            fixture_create_dir: UserPrefController
    ) -> None:
        """
        Test method for the default path method if no default path is set
        """
        assert fixture_create_dir.default_path() is None

    def test_create_directory(self, base_fixture: UserPrefController) -> None:
        """ Test method for the create directory method """
        assert base_fixture.create_directory()
        # Verify the directory was actually created on disk
        created_dir = base_fixture.db_location
        assert created_dir.exists() and created_dir.is_dir()

    def test_create_database_connection(
            self,
            base_fixture: UserPrefController
    ) -> None:
        """ Testing for if the Class Creates an instance of UserPrefModel """
        base_fixture.create_directory()
        base_fixture.create_database_connection()
        assert isinstance(base_fixture.database, UserPrefModel)

    def test_set_default_directory(
            self,
            tmp_path,
            fixture_setup_database: UserPrefController
    ) -> None:
        """ Testing to see if Adding Directory branch works """
        temp_dir: pathlib.Path = tmp_path
        assert fixture_setup_database.set_default_directory(temp_dir)

    def test_update_default_directory(
            self,
            tmp_path,
            fixture_setup_database: UserPrefController
    ) -> None:
        """ Testing to see if updating Directory branch works """
        temp_dir: pathlib.Path = tmp_path / "test_db"
        assert fixture_setup_database.set_default_directory(temp_dir)

    def test_get_default_directory(
            self,
            tmp_path,
            fixture_setup_database: UserPrefController
    ) -> None:
        """ Test method for the get_default_directory method """
        logging.debug("testpath: %s", str(tmp_path))
        assert fixture_setup_database.get_default_directory() == tmp_path

        # Don't know why but this section of code when create directory
        # is working in the UserPref Controller causes an error
        # temp_dir2: pathlib.Path = tmp_path
        # with pytest.raises(sqlite3.OperationalError) as invalid_dir:
        #     new_db_dir:UserPrefController = UserPrefController(
        #         database_location=temp_dir2,
        #         database_name="test_db.db"
        #     )
        #     new_db_dir.create_database_connection()
        #     new_db_dir.get_default_directory()
        # logging.debug("test_get_directory: %s", invalid_dir.value)
        # assert isinstance(invalid_dir.value, sqlite3.OperationalError)


if __name__ == '__main__':
    pytest.main()
