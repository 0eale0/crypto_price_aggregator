import pytest

from app.api.services.auth_helpers import (
    verify_password,
    get_password_hash,
    create_access_token,
)


@pytest.mark.parametrize(
    "input_data, output_data, expected",
    [
        (
            "string",
            "$2b$12$Bp0qpiUX/Mk0tl9YGteRzeTDCiaVQhobQpYYTvS28ybhQLgXUmuyi",
            True,
        ),
        (
            "894579",
            "$2b$12$zSn4mklK3aQ8sTwk.r2Ws.hxpBrTCCH5yWI1xkJDRgf8WtZDT5tUq",
            True,
        ),
        (
            "184509",
            "$2b$12$9kOVp/MvokQuGG0YvXty.OQ5LIRnua7slGm6SlVBm7uYGAHSbw6eS",
            False,
        ),
    ],
)
def test_true_false_verify_password(input_data, output_data, expected):
    assert verify_password(input_data, output_data) == expected


@pytest.mark.parametrize(
    "input_data",
    ["456768798", "768909", "string"],
)
def test_get_password_hash(input_data):
    assert isinstance(get_password_hash(input_data), str) is True


@pytest.mark.parametrize(
    "input_username, input_password",
    [("username_1", "122847"), ("username_2", "768909"), ("username_3", "string")],
)
def test_create_access_token(input_username, input_password):
    x = create_access_token(
        data={"username": input_username, "password": input_password}
    )
    assert isinstance(x, str) is True
