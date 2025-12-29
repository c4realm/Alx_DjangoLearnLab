from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with following system
    """

    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="UserFollowing",
        related_name="followers"
    )

    def __str__(self):
        return self.username


class UserFollowing(models.Model):
    user = models.ForeignKey(
        User,
        related_name="following_relationships",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name="follower_relationships",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "following")

    def __str__(self):
        return f"{self.user} follows {self.following}"

