"""Tests for validators."""

from src.myspace.validators import validate_username, validate_email


class TestValidateUsername:
    def test_valid_username(self):
        valid, error = validate_username("alice")
        assert valid is True
        assert error is None

    def test_empty_username(self):
        valid, error = validate_username("")
        assert valid is False
        assert "required" in error

    def test_too_short(self):
        valid, error = validate_username("ab")
        assert valid is False
        assert "at least 3" in error

    def test_reserved_name(self):
        valid, error = validate_username("admin")
        assert valid is False
        assert "reserved" in error


class TestValidateEmail:
    def test_valid_email(self):
        valid, error = validate_email("alice@example.com")
        assert valid is True

    def test_empty_email(self):
        valid, error = validate_email("")
        assert valid is False
