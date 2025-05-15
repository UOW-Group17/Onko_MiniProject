""" Test File for the user_pref_model file """
import pathlib
import logging
import pytest
from src.user_pref_model import UserPrefModel

logger = logging.getLogger(__name__)
logger.debug("UnitTests: UserPrefModel")


class TestUserPrefModel:
    """ Test Class for UserPrefModel """
    @pytest.fixture
    def access(self, tmp_path):
        """ Fixture to set up and Teardown tests """
        logging.info('Setting up test DB fixture')
        yield UserPrefModel(database_path=tmp_path, database_name="test_db.db")
        logging.info('Teardown test DB fixture')

    def test_create_table(self, access):
        """ Test Method for create Table method """
        assert access.create_table() == 1

    def test_get_default_directory(self, tmp_path, access):
        """ Test Method for get User method """
        temp_dir: pathlib.Path = tmp_path / "test_db"
        access.add_default_directory('Adam', temp_dir)
        assert access.get_default_directory("Adam") == temp_dir
        assert access.get_default_directory("Aiden") is None

    def test_add_default_directory(self, tmp_path, access):
        """ Test Method for add User method """
        temp_dir: pathlib.Path = tmp_path / "test_db"
        temp_dir2: pathlib.Path = temp_dir / "test_db2"
        assert access.add_default_directory("Bert", temp_dir)
        assert access.get_default_directory("Bert") == temp_dir
        assert access.add_default_directory("Bert", temp_dir2)
        assert access.get_default_directory("Bert") != temp_dir2
        with pytest.raises(RuntimeError) as invalid_user:
            access.add_default_directory("", temp_dir)
        assert str(invalid_user.value) == "Error: Invalid Directory Name"
        with pytest.raises(RuntimeError) as invalid_dir:
            access.add_default_directory("ValidUser", pathlib.Path(""))
        assert str(invalid_dir.value) == "Error: Invalid Directory Name"
        with pytest.raises(RuntimeError) as invalid_user:
            long_username = "u" * 300
            access.add_default_directory(long_username, temp_dir)
        assert str(invalid_user.value) == "Error: Invalid Directory Name"
        with pytest.raises(RuntimeError) as invalid_dir:
            long_dir = "p" * 300
            access.add_default_directory("ValidUser", pathlib.Path(long_dir))
        assert str(invalid_dir.value) == "Error: Invalid Directory Name"

    def test_update_directory(self, tmp_path, access):
        """ Test Method for update User method """
        temp_dir: pathlib.Path = tmp_path / "test_db"
        temp_dir2: pathlib.Path = temp_dir / "test_db2"
        access.add_default_directory("Chuck", temp_dir)
        assert access.update_default_directory("Chuck", temp_dir2)
        assert access.update_default_directory("Cho", temp_dir)
        assert access.get_default_directory("Cho") is None
        with pytest.raises(RuntimeError) as invalid_user:
            access.update_default_directory("", temp_dir)
        assert str(invalid_user.value) == "Error: Invalid Directory Name"
        with pytest.raises(RuntimeError) as invalid_dir:
            access.update_default_directory("ValidUser", pathlib.Path(""))
        assert str(invalid_dir.value) == "Error: Invalid Directory Name"
        long_username = "u" * 300
        with pytest.raises(RuntimeError) as invalid_user:
            access.update_default_directory(long_username, temp_dir)
        assert str(invalid_user.value) == "Error: Invalid Directory Name"
        long_dir = "p" * 300
        with pytest.raises(RuntimeError) as invalid_dir:
            access.update_default_directory(
                "ValidUser",
                pathlib.Path(long_dir)
            )
        assert str(invalid_dir.value) == "Error: Invalid Directory Name"

    def test_delete_default_directory(self, tmp_path, access):
        """ Test Method for delete User method """
        access.add_default_directory("Dan", pathlib.Path(tmp_path))
        assert access.delete_default_directory("Dan")
        assert access.get_default_directory("Dan") is None
        assert access.delete_default_directory("Dom")


if __name__ == "__main__":
    pytest.main()
