"""Utility functions for MySpace application."""

import hashlib
import re
from datetime import datetime, timedelta
from typing import Any


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def time_ago(dt: datetime) -> str:
    """Convert a datetime to a human-readable 'time ago' string."""
    now = datetime.utcnow()
    diff = now - dt

    if diff < timedelta(minutes=1):
        seconds = int(diff.total_seconds())
        return f"{seconds} second{'s' if seconds != 1 else ''} ago"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=30):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif diff < timedelta(days=365):
        months = diff.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = diff.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"


def generate_hash(content: str) -> str:
    """Generate a SHA-256 hash of the content."""
    return hashlib.sha256(content.encode()).hexdigest()


def paginate(items: list[Any], page: int = 1, page_size: int = 20) -> dict:
    """Paginate a list of items."""
    total = len(items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": items[start:end],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


def extract_mentions(text: str) -> list[str]:
    """Extract @mentions from text."""
    return re.findall(r"@(\w+)", text)


def extract_hashtags(text: str) -> list[str]:
    """Extract #hashtags from text."""
    return re.findall(r"#(\w+)", text)


def mask_email(email: str) -> str:
    """Mask an email address for privacy."""
    if "@" not in email:
        return email
    local, domain = email.rsplit("@", 1)
    if len(local) <= 2:
        masked_local = local[0] + "*"
    else:
        masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked_local}@{domain}"
