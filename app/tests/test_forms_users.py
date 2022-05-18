import pytest

from app.models.forms.users import UserValidation


@pytest.mark.parametrize(
    'input_data, expected',
    [
        ('Ivan', 'Ivan'),
        ('Sasha', 'Sasha'),
        ('Peter', 'Peter')
    ]
)
def test_check_username(input_data, expected):
    assert UserValidation.check_username('Ivan') == 'Ivan'
    assert UserValidation.check_username('Sasha') == 'Sasha'
