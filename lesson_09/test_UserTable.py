import pytest
from UsersTable import UserTable

CONNECTION_STRING = "postgresql://postgres:123@localhost:5432/QA"


@pytest.fixture(scope="function")
def user_table():
    table = UserTable(CONNECTION_STRING)
    table.delete_all()
    yield table
    table.delete_all()


class TestUserCRUDOperations:
    TEST_USER_ID = 10001
    TEST_USER_EMAIL = "test@google.com"
    TEST_SUBJECT_ID = 5

    def test_create_user_success(self, user_table):
        assert user_table.count() == 0
        rows_affected = user_table.create(
            user_id=self.TEST_USER_ID,
            user_email=self.TEST_USER_EMAIL,
            subject_id=self.TEST_SUBJECT_ID
        )

        assert rows_affected == 1
        assert user_table.count() == 1

        user = user_table.get(self.TEST_USER_ID)
        assert user is not None
        assert user[0] == self.TEST_USER_ID
        assert user[1] == self.TEST_USER_EMAIL
        assert user[2] == self.TEST_SUBJECT_ID

    def test_update_user_success(self, user_table):
        user_table.create(
            user_id=self.TEST_USER_ID,
            user_email=self.TEST_USER_EMAIL,
            subject_id=self.TEST_SUBJECT_ID
        )

        updated_email = "updated@bk.ru"
        updated_subject_id = 10

        rows_updated = user_table.update(
            user_id=self.TEST_USER_ID,
            user_email=updated_email,
            subject_id=updated_subject_id
        )

        assert rows_updated == 1

        user = user_table.get(self.TEST_USER_ID)
        assert user[1] == updated_email
        assert user[2] == updated_subject_id

    def test_delete_user_success(self, user_table):
        user_table.create(
            user_id=self.TEST_USER_ID,
            user_email=self.TEST_USER_EMAIL,
            subject_id=self.TEST_SUBJECT_ID
        )

        assert user_table.count() == 1

        rows_deleted = user_table.delete(self.TEST_USER_ID)

        assert rows_deleted == 1
        assert user_table.count() == 0
        assert user_table.get(self.TEST_USER_ID) is None

    def test_create_duplicate_user_id_fails(self, user_table):
        user_table.create(
            user_id=self.TEST_USER_ID,
            user_email=self.TEST_USER_EMAIL,
            subject_id=self.TEST_SUBJECT_ID
        )

        with pytest.raises(ValueError, match="уже существует"):
            user_table.create(
                user_id=self.TEST_USER_ID,
                user_email="another@example.com",
                subject_id=7
            )

    def test_update_nonexistent_user_fails(self, user_table):
        with pytest.raises(ValueError, match="не найден"):
            user_table.update(
                user_id=99999,
                user_email="nonexistent@example.com",
                subject_id=1
            )

    def test_delete_nonexistent_user_fails(self, user_table):
        with pytest.raises(ValueError, match="не найден"):
            user_table.delete(99999)

    def test_get_user_as_dict(self, user_table):
        user_table.create(
            user_id=self.TEST_USER_ID,
            user_email=self.TEST_USER_EMAIL,
            subject_id=self.TEST_SUBJECT_ID
        )

        user_dict = user_table.get_user_as_dict(self.TEST_USER_ID)

        assert isinstance(user_dict, dict)
        assert user_dict['user_id'] == self.TEST_USER_ID
        assert user_dict['user_email'] == self.TEST_USER_EMAIL
        assert user_dict['subject_id'] == self.TEST_SUBJECT_ID

    def test_create_batch_users(self, user_table):
        users_data = [
            (10002, "user1@example.com", 1),
            (10003, "user2@example.com", 2),
            (10004, "user3@example.com", 3)
        ]

        rows_affected = user_table.create_batch(users_data)

        assert rows_affected == 3
        assert user_table.count() == 3

        for user_id, email, subject_id in users_data:
            user = user_table.get(user_id)
            assert user[1] == email
            assert user[2] == subject_id

    def test_update_email_only(self, user_table):
        user_table.create(
            user_id=self.TEST_USER_ID,
            user_email=self.TEST_USER_EMAIL,
            subject_id=self.TEST_SUBJECT_ID
        )

        new_email = "newemail@mail.ru"
        rows_updated = user_table.update_email(self.TEST_USER_ID, new_email)

        assert rows_updated == 1

        user = user_table.get(self.TEST_USER_ID)
        assert user[1] == new_email
        assert user[2] == self.TEST_SUBJECT_ID

    def test_update_subject_only(self, user_table):
        user_table.create(
            user_id=self.TEST_USER_ID,
            user_email=self.TEST_USER_EMAIL,
            subject_id=self.TEST_SUBJECT_ID
        )

        new_subject_id = 15
        rows_updated = user_table.update_subject(self.TEST_USER_ID,
                                                 new_subject_id)

        assert rows_updated == 1

        user = user_table.get(self.TEST_USER_ID)
        assert user[1] == self.TEST_USER_EMAIL
        assert user[2] == new_subject_id

    def test_search_users(self, user_table):
        test_users = [
            (10010, "john.doe@example.com", 5),
            (10011, "jane.smith@example.com", 10),
            (10012, "john.wick@example.org", 3),
            (10013, "alice@test.com", 15),
            (10014, "bob.johnson@example.net", 8)
        ]

        for user_id, email, subject_id in test_users:
            user_table.create(user_id, email, subject_id)

        results = user_table.search_users(email_pattern="john")
        assert len(results) == 3

        results = user_table.search_users(min_subject_id=5, max_subject_id=10)
        assert len(results) == 3

        results = user_table.search_users(email_pattern="example",
                                          min_subject_id=5)
        assert len(results) == 3

    def test_get_all_as_dicts(self, user_table):
        test_users = [
            (10020, "user1@example.com", 1),
            (10021, "user2@example.com", 2)
        ]

        for user_id, email, subject_id in test_users:
            user_table.create(user_id, email, subject_id)

        users_dicts = user_table.get_all_as_dicts()

        assert len(users_dicts) == 2
        assert isinstance(users_dicts[0], dict)
        assert users_dicts[0]['user_id'] == 10020
        assert users_dicts[1]['user_email'] == "user2@example.com"

    def test_get_by_email(self, user_table):
        user_table.create(10030, "test@example.com", 1)
        user_table.create(10031, "test@example.com", 2)
        user_table.create(10032, "other@example.com", 3)

        users = user_table.get_by_email("test@example.com")
        assert len(users) == 2

        for user in users:
            assert user[1] == "test@example.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
