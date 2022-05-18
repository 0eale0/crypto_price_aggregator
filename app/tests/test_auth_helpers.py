from app.api.services.auth_helpers import verify_password, get_password_hash


def test_verify_password():
    assert verify_password('string', '$2b$12$Bp0qpiUX/Mk0tl9YGteRzeTDCiaVQhobQpYYTvS28ybhQLgXUmuyi') is True
    assert verify_password('894579', '$2b$12$zSn4mklK3aQ8sTwk.r2Ws.hxpBrTCCH5yWI1xkJDRgf8WtZDT5tUq') is True
    assert verify_password('184509', '$2b$12$9kOVp/MvokQuGG0YvXty.OQ5LIRnua7slGm6SlVBm7uYGAHSbw6eS') is False
    assert type(verify_password('184509', '$2b$12$9kOVp/MvokQuGG0YvXty.OQ5LIRnua7slGm6SlVBm7uYGAHSbw6eS')) == bool


def test_get_password_hash():
    assert type(get_password_hash('456789')) == str

