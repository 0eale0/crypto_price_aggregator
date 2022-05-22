import pytest
from app.models.forms.users import UserValidation, RegistrationForm, ChangeDataForm


@pytest.mark.parametrize(
    "input_data, expected", [("Ivan", "Ivan"), ("Sasha", "Sasha"), ("Peter", "Peter")]
)
def test_check_username_in_user_validation(input_data, expected):
    assert UserValidation.check_username(input_data) == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [("Adelya", "Adelya"), ("Ruslan", "Ruslan"), ("Danis", "Danis")],
)
def test_check_username_in_register_form(input_data, expected):
    assert RegistrationForm.check_username(input_data) == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [("Masha", "Masha"), ("Artem", "Artem"), ("Kamila", "Kamila")],
)
def test_check_username_in_change_data_form(input_data, expected):
    assert ChangeDataForm.check_username(input_data) == expected
