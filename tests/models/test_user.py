from app.models import User


def test_password_is_hashed_when_set(mocker):
    mocker.patch(
        'app.models.user.hash_password', return_value='hashed-password'
    )
    user = User(
        id=1,
        email='user@mail.com',
        password='plain-password',
    )
    assert user.password == 'hashed-password'


def test_verify_password_when_password_is_correct_should_return_true():
    user = User(
        id=1,
        email='user@mail.com',
        password='correct-password',
    )
    assert user.verify_password('correct-password') is True


def test_verify_password_when_password_is_incorrect_should_return_false():
    user = User(
        id=1,
        email='user@mail.com',
        password='correct-password',
    )
    assert user.verify_password('wrong-password') is False
