"""Input validation utilities for MySpace application."""

import re
from typing import Optional


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """Validate a username.

    Rules:
    - 3 to 30 characters
    - Only alphanumeric characters and underscores
    - Must start with a letter
    - Cannot be a reserved name
    """
    reserved_names = {"admin", "root", "system", "moderator", "support", "help"}

    if not username:
        return False, "Username is required"
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 30:
        return False, "Username must be 30 characters or fewer"
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"
    if username.lower() in reserved_names:
        return False, f"Username '{username}' is reserved"

    return True, None


def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """Validate an email address."""
    if not email:
        return False, "Email is required"
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """Validate a password.

    Rules:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, None


def validate_post_title(title: str) -> tuple[bool, Optional[str]]:
    """Validate a post title."""
    if not title:
        return False, "Title is required"
    if len(title) < 5:
        return False, "Title must be at least 5 characters"
    if len(title) > 200:
        return False, "Title must be 200 characters or fewer"
    return True, None


def validate_post_content(content: str) -> tuple[bool, Optional[str]]:
    """Validate post content."""
    if not content:
        return False, "Content is required"
    if len(content) < 10:
        return False, "Content must be at least 10 characters"
    if len(content) > 50000:
        return False, "Content must be 50,000 characters or fewer"
    return True, None


def sanitize_html(text: str) -> str:
    """Remove HTML tags from text (basic sanitization)."""
    return re.sub(r"<[^>]+>", "", text)


def validate_tag(tag: str) -> tuple[bool, Optional[str]]:
    """Validate a tag."""
    if not tag or not tag.strip():
        return False, "Tag is required"
    tag = tag.strip()
    if len(tag) > 50:
        return False, "Tag must be 50 characters or fewer"
    if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9\s-]*$", tag):
        return False, "Tag must start with alphanumeric and contain only letters, numbers, spaces, and hyphens"
    return True, None
