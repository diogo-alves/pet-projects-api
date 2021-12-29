from app.models import User


def test_add_should_save_a_new_user_in_db(user_repository):
    user = User(first_name='user', email='user@mail.com')
    saved_user = user_repository.add(user)
    assert isinstance(saved_user, User)
    assert saved_user.id is not None


def test_list_should_retrieve_a_list_of_users(user_repository, users):
    result = user_repository.list(skip=0, limit=10)
    assert isinstance(result, list)
    assert all(isinstance(user, User) for user in result)
    assert len(result) == 3


def test_list_should_skip_an_user(user_repository, users):
    result = user_repository.list(skip=1, limit=10)
    assert len(result) == 2


def test_list_should_limit_the_retrieved_users(user_repository, users):
    result = user_repository.list(skip=0, limit=1)
    assert len(result) == 1


def test_filter_should_retrieve_a_filtered_list_of_users(
    user_repository, users
):
    result = user_repository.filter(skip=0, limit=10, is_superuser=True)
    assert isinstance(result, list)
    assert all(isinstance(user, User) for user in result)
    assert len(result) == 2


def test_get_should_retrieve_user_if_exists(user_repository, user):
    assert user_repository.get(id=user.id) == user


def test_get_should_return_none_if_user_does_not_exist(user_repository, users):
    assert user_repository.get(id=None) is None


def test_update_should_update_user_in_db(user_repository, user):
    user.is_superuser = True
    updated_user = user_repository.update(user)
    assert updated_user.id == user.id
    assert updated_user.is_superuser


def test_remove_should_delete_user_in_db(user_repository, user):
    user_repository.remove(user)
    assert user_repository.get(id=user.id) is None
