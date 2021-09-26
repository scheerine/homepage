import math

from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    slug = models.SlugField(primary_key=True)
    title = models.TextField(max_length=60)
    description = models.TextField(max_length=200)
    markdown = models.TextField()

    authors = models.TextField(null=True, blank=True)
    tags = models.TextField(max_length=200, null=True, blank=True)
    thumbnail = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def tags_list(self):
        """The entry tags, split into a list."""
        return self.tags.split(',')

    @property
    def minutes_to_read(self):
        """Compute an approximate read time by the word count."""
        avg_words_per_minute = 240 # average english reader
        num_words = len(self.markdown.split())
        return math.ceil(num_words / avg_words_per_minute)
