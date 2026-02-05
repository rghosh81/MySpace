"""Domain models for MySpace application."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"


@dataclass
class User:
    username: str
    email: str
    role: UserRole = UserRole.USER
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    bio: Optional[str] = None

    def promote(self) -> None:
        """Promote user to the next role level."""
        promotion_path = {
            UserRole.GUEST: UserRole.USER,
            UserRole.USER: UserRole.MODERATOR,
            UserRole.MODERATOR: UserRole.ADMIN,
        }
        if self.role in promotion_path:
            self.role = promotion_path[self.role]
        else:
            raise ValueError(f"Cannot promote user with role {self.role.value}")

    def demote(self) -> None:
        """Demote user to the previous role level."""
        demotion_path = {
            UserRole.ADMIN: UserRole.MODERATOR,
            UserRole.MODERATOR: UserRole.USER,
            UserRole.USER: UserRole.GUEST,
        }
        if self.role in demotion_path:
            self.role = demotion_path[self.role]
        else:
            raise ValueError(f"Cannot demote user with role {self.role.value}")

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True

    def update_bio(self, bio: str) -> None:
        """Update user bio with validation."""
        if len(bio) > 500:
            raise ValueError("Bio must be 500 characters or fewer")
        self.bio = bio


@dataclass
class Post:
    title: str
    content: str
    author: User
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    is_published: bool = False
    likes: int = 0
    tags: list[str] = field(default_factory=list)

    def publish(self) -> None:
        """Publish the post."""
        if not self.author.is_active:
            raise PermissionError("Inactive users cannot publish posts")
        if not self.title or not self.content:
            raise ValueError("Post must have both title and content to publish")
        self.is_published = True

    def unpublish(self) -> None:
        """Unpublish the post."""
        self.is_published = False

    def edit(self, title: Optional[str] = None, content: Optional[str] = None) -> None:
        """Edit the post."""
        if title:
            self.title = title
        if content:
            self.content = content
        self.updated_at = datetime.utcnow()

    def like(self) -> None:
        """Add a like to the post."""
        self.likes += 1

    def add_tag(self, tag: str) -> None:
        """Add a tag to the post."""
        normalized = tag.lower().strip()
        if not normalized:
            raise ValueError("Tag cannot be empty")
        if normalized in self.tags:
            raise ValueError(f"Tag '{normalized}' already exists")
        if len(self.tags) >= 10:
            raise ValueError("Maximum of 10 tags allowed")
        self.tags.append(normalized)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the post."""
        normalized = tag.lower().strip()
        if normalized not in self.tags:
            raise ValueError(f"Tag '{normalized}' not found")
        self.tags.remove(normalized)


@dataclass
class Comment:
    content: str
    author: User
    post: Post
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_deleted: bool = False

    def delete(self) -> None:
        """Soft-delete the comment."""
        self.is_deleted = True

    def can_be_deleted_by(self, user: User) -> bool:
        """Check if a given user has permission to delete this comment."""
        if user.role == UserRole.ADMIN:
            return True
        if user.role == UserRole.MODERATOR:
            return True
        if user.username == self.author.username:
            return True
        if user.username == self.post.author.username:
            return True
        return False
