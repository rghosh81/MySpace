"""Tests for domain models."""

import pytest

from src.myspace.models import Comment, Post, User, UserRole


class TestUser:
    def test_create_user_defaults(self):
        user = User(username="alice", email="alice@example.com")
        assert user.username == "alice"
        assert user.email == "alice@example.com"
        assert user.role == UserRole.USER
        assert user.is_active is True
        assert user.bio is None

    def test_promote_user(self):
        user = User(username="alice", email="alice@example.com", role=UserRole.USER)
        user.promote()
        assert user.role == UserRole.MODERATOR

    def test_promote_guest_to_user(self):
        user = User(username="bob", email="bob@example.com", role=UserRole.GUEST)
        user.promote()
        assert user.role == UserRole.USER

    def test_deactivate_user(self):
        user = User(username="alice", email="alice@example.com")
        user.deactivate()
        assert user.is_active is False


class TestPost:
    def _make_user(self):
        return User(username="alice", email="alice@example.com")

    def test_create_post(self):
        user = self._make_user()
        post = Post(title="Hello", content="World", author=user)
        assert post.title == "Hello"
        assert post.content == "World"
        assert post.is_published is False
        assert post.likes == 0

    def test_publish_post(self):
        user = self._make_user()
        post = Post(title="Hello", content="World", author=user)
        post.publish()
        assert post.is_published is True

    def test_like_post(self):
        user = self._make_user()
        post = Post(title="Hello", content="World", author=user)
        post.like()
        post.like()
        assert post.likes == 2

    def test_add_tag(self):
        user = self._make_user()
        post = Post(title="Hello", content="World", author=user)
        post.add_tag("python")
        assert "python" in post.tags
