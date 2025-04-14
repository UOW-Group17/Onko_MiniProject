import pytest
from DBAccess import DBAccess

class TestDBAccess:
    def test_create_table(self):
        access = DBAccess("test_Database.db")
        assert access.create_table() == 1

    def test_get_user(self):
        access = DBAccess("test_Database.db")
        access.create_table()
        access.add_user("Adam", "~")
        assert access.get_user("Adam") == ("Adam", "~")


    def test_add_user(self):
        access = DBAccess("test_Database.db")
        access.create_table()
        assert access.add_user("Bert", "~") == 1
        # assert access.add_user(123, 23213) == 2

    def test_update_user(self):
        access = DBAccess("test_Database.db")
        access.create_table()
        access.add_user("Chuck", "~")
        assert access.update_user("Chuck", "~/.user") == 1

    def test_delete_user(self):
        access = DBAccess("test_Database.db")
        access.create_table()
        access.add_user("Dan", "~/")
        assert access.delete_user("Dan") == 1

if __name__ == "__main__":
    pytest.main()

