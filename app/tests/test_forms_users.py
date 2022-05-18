from app.models.forms.users import UserValidation


def test_check_username():
    assert UserValidation.check_username('Ivan') == 'Ivan'
    assert UserValidation.check_username('Sasha') == 'Sasha'
    assert type(UserValidation.check_username('Peter')) == str
