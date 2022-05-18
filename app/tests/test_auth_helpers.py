from app.api.services.auth_helpers import verify_password, get_password_hash
import pytest


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


def test_get_password_hash():
    assert type(get_password_hash("456789")) == str
