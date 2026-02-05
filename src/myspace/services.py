"""Service layer for MySpace application."""

from datetime import datetime
from typing import Optional

from .models import Comment, Post, User, UserRole


class UserService:
    """Service for managing users."""

    def __init__(self):
        self._users: dict[str, User] = {}

    def register(self, username: str, email: str) -> User:
        """Register a new user."""
        if not username or not email:
            raise ValueError("Username and email are required")
        if not self._is_valid_email(email):
            raise ValueError(f"Invalid email: {email}")
        if username in self._users:
            raise ValueError(f"Username '{username}' already taken")
        if any(u.email == email for u in self._users.values()):
            raise ValueError(f"Email '{email}' already registered")

        user = User(username=username, email=email)
        self._users[username] = user
        return user

    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self._users.get(username)

    def delete_user(self, username: str, requesting_user: User) -> bool:
        """Delete a user (admin only)."""
        if requesting_user.role != UserRole.ADMIN:
            raise PermissionError("Only admins can delete users")
        if username not in self._users:
            return False
        del self._users[username]
        return True

    def list_users(self, role: Optional[UserRole] = None, active_only: bool = False) -> list[User]:
        """List users with optional filtering."""
        users = list(self._users.values())
        if role:
            users = [u for u in users if u.role == role]
        if active_only:
            users = [u for u in users if u.is_active]
        return users

    def search_users(self, query: str) -> list[User]:
        """Search users by username or email."""
        query = query.lower()
        return [
            u for u in self._users.values()
            if query in u.username.lower() or query in u.email.lower()
        ]

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Basic email validation."""
        if "@" not in email:
            return False
        local, domain = email.rsplit("@", 1)
        if not local or not domain:
            return False
        if "." not in domain:
            return False
        return True


class PostService:
    """Service for managing posts."""

    def __init__(self):
        self._posts: list[Post] = []

    def create_post(self, title: str, content: str, author: User) -> Post:
        """Create a new post."""
        if not author.is_active:
            raise PermissionError("Inactive users cannot create posts")
        post = Post(title=title, content=content, author=author)
        self._posts.append(post)
        return post

    def get_published_posts(self) -> list[Post]:
        """Get all published posts."""
        return [p for p in self._posts if p.is_published]

    def get_posts_by_author(self, username: str) -> list[Post]:
        """Get all posts by a specific author."""
        return [p for p in self._posts if p.author.username == username]

    def get_posts_by_tag(self, tag: str) -> list[Post]:
        """Get all published posts with a specific tag."""
        normalized = tag.lower().strip()
        return [p for p in self._posts if p.is_published and normalized in p.tags]

    def get_popular_posts(self, min_likes: int = 10) -> list[Post]:
        """Get popular published posts sorted by likes."""
        popular = [p for p in self._posts if p.is_published and p.likes >= min_likes]
        return sorted(popular, key=lambda p: p.likes, reverse=True)

    def delete_post(self, post: Post, requesting_user: User) -> bool:
        """Delete a post (author, moderator, or admin)."""
        if requesting_user.role in (UserRole.ADMIN, UserRole.MODERATOR):
            self._posts.remove(post)
            return True
        if requesting_user.username == post.author.username:
            self._posts.remove(post)
            return True
        raise PermissionError("You don't have permission to delete this post")

    def get_feed(self, user: User, page: int = 1, page_size: int = 20) -> list[Post]:
        """Get paginated feed of published posts for a user."""
        published = sorted(
            [p for p in self._posts if p.is_published],
            key=lambda p: p.created_at,
            reverse=True,
        )
        start = (page - 1) * page_size
        end = start + page_size
        return published[start:end]


class CommentService:
    """Service for managing comments."""

    def __init__(self):
        self._comments: list[Comment] = []

    def add_comment(self, content: str, author: User, post: Post) -> Comment:
        """Add a comment to a post."""
        if not author.is_active:
            raise PermissionError("Inactive users cannot comment")
        if not post.is_published:
            raise ValueError("Cannot comment on unpublished posts")
        if not content.strip():
            raise ValueError("Comment content cannot be empty")

        comment = Comment(content=content, author=author, post=post)
        self._comments.append(comment)
        return comment

    def get_comments_for_post(self, post: Post) -> list[Comment]:
        """Get all non-deleted comments for a post."""
        return [
            c for c in self._comments
            if c.post is post and not c.is_deleted
        ]

    def delete_comment(self, comment: Comment, requesting_user: User) -> bool:
        """Delete a comment if the user has permission."""
        if not comment.can_be_deleted_by(requesting_user):
            raise PermissionError("You don't have permission to delete this comment")
        comment.delete()
        return True

    def get_comments_by_user(self, username: str) -> list[Comment]:
        """Get all non-deleted comments by a user."""
        return [
            c for c in self._comments
            if c.author.username == username and not c.is_deleted
        ]

    def count_comments_for_post(self, post: Post) -> int:
        """Count non-deleted comments for a post."""
        return len(self.get_comments_for_post(post))
