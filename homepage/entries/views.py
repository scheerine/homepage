import re

from urllib.parse import unquote
from os.path import join

from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.static import serve

from entries.models import Entry


def index(request, slug):
    """Return a view for a specific blog entry."""
    entry = get_object_or_404(Entry, slug=slug)
    entries = Entry.objects \
        .order_by('-created') \
        .exclude(pk=entry.pk)[:2]
    return TemplateResponse(request, 'entries/index.html', {
        'entry': entry,
        'entries': entries,
    })


def serve_attachment(request, slug, path):
    """Serve an attachment for a blog entry."""
    if re.search('^(images|attachments)/', path) is None:
        raise PermissionDenied

    if '..' in unquote(path):
        raise PermissionDenied

    filesystem_path = join(slug, path)
    return serve(request, filesystem_path, settings.REPOSITORY_ROOT)
