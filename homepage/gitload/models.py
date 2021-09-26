from django.db import models
from django.utils.crypto import get_random_string


def generate_token_value():
    """
    Generate a random token value for the token creation.
    """
    return get_random_string(length=64)


class GitloadToken(models.Model):
    """
    A token used for the continuous integration authentication.

    The token can be easily created via the admin interface.
    """

    value = models.TextField(
        default=generate_token_value,
        editable=False,
        primary_key=True
    )

    def __str__(self):
        return self.value
