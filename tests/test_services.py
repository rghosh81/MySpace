"""Tests for service layer."""

import pytest

from src.myspace.models import User, UserRole
from src.myspace.services import UserService, PostService


class TestUserService:
    def test_register_user(self):
        service = UserService()
        user = service.register("alice", "alice@example.com")
        assert user.username == "alice"
        assert user.email == "alice@example.com"

    def test_register_duplicate_username(self):
        service = UserService()
        service.register("alice", "alice@example.com")
        with pytest.raises(ValueError, match="already taken"):
            service.register("alice", "alice2@example.com")

    def test_register_invalid_email(self):
        service = UserService()
        with pytest.raises(ValueError, match="Invalid email"):
            service.register("alice", "not-an-email")

    def test_get_user(self):
        service = UserService()
        service.register("alice", "alice@example.com")
        user = service.get_user("alice")
        assert user is not None
        assert user.username == "alice"

    def test_get_nonexistent_user(self):
        service = UserService()
        assert service.get_user("ghost") is None


class TestPostService:
    def _make_service_and_user(self):
        user = User(username="alice", email="alice@example.com")
        service = PostService()
        return service, user

    def test_create_post(self):
        service, user = self._make_service_and_user()
        post = service.create_post("Title", "Content here", user)
        assert post.title == "Title"
        assert post.author.username == "alice"

    def test_create_post_inactive_user(self):
        service, user = self._make_service_and_user()
        user.deactivate()
        with pytest.raises(PermissionError):
            service.create_post("Title", "Content here", user)

    def test_get_published_posts(self):
        service, user = self._make_service_and_user()
        post1 = service.create_post("Post 1", "Content 1", user)
        post2 = service.create_post("Post 2", "Content 2", user)
        post1.publish()
        published = service.get_published_posts()
        assert len(published) == 1
        assert published[0].title == "Post 1"
