"""Markdown Package.

To provide dynamic Markdown rendering, we use the Markdown package.

.. _Markdown package:
   https://pypi.python.org/pypi/Markdown

.. _Markdown package extensions
   https://python-markdown.github.io/extensions/
"""
import subprocess

from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from markdown import Markdown, Extension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.treeprocessors import Treeprocessor

from django import template

import bleach

"""
Default whitelist of allowed HTML tags. Any other HTML tags will be escaped or
stripped from the text. This applies to the html output that Markdown produces.
"""
ALLOWED_TAGS = [
    'ul',
    'ol',
    'li',
    'p',
    'pre',
    'code',
    'blockquote',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr',
    'br',
    'strong',
    'em',
    'a',
    'img',
    'div'
]

"""
Default whitelist of attributes. It allows the href and title attributes for <a>
tags and the src, title and alt attributes for <img> tags. Any other attribute
will be stripped from its tag.
"""
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'title'],
    'img': ['src', 'title', 'alt'],
    'code': ['*'],
}

"""
Default whitelist of styles is an empty list. If you allow the style attribute,
you will also need to whitelist styles users are allowed to set, for example
color and background-color.
"""
ALLOWED_STYLES = []

"""
If you allow tags that have attributes containing a URI value
(like the href attribute of an anchor tag,) you may want to adapt
the accepted protocols. The default list only allows http, https and mailto.
"""
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


class ImageVersionTreeprocessor(Treeprocessor):
    """Markdown tree processor that appends version strings to image resources."""

    def __init__(self, version_provider, *args, **kwargs):
        self.version_provider = version_provider
        super().__init__(*args, **kwargs)

    def run(self, root):
        """
        Traverse the tree and add the version id to the src attribute
        of all <img> tags to control browser image caching based on the
        given version id.
        """
        version_id = self.version_provider.get_version()
        if version_id is None:
            return
        img_nodes = root.iter('img')
        for node in img_nodes:
            url = node.get('src')
            if not url:
                continue
            if url.startswith('https://') or url.startswith('http://'):
                # note that the comparison is intentionally case-sensitive
                continue
            node.set('src', f'{url}?v={version_id}')


class ImageVersionExtension(Extension):
    """Markdown extension that appends version strings to image resources."""

    def __init__(self, version_provider, *args, **kwargs):
        """Create an image version extension."""
        self.version_provider = version_provider
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Wrap the custom image version treeprocessor."""
        md.treeprocessors.add(
            'image_version_extension',
            ImageVersionTreeprocessor(self.version_provider, md),
            '_end'
        )


class GitVersionProvider:
    """Provides a version string based on the id of a repo's latest commit."""

    args = 'git rev-parse --short HEAD'.split()

    def __init__(self, repo):
        """Initialize with the given path to a Git repository."""
        self.repo = repo

    def get_version(self):
        """Return the short id of the latest commit or None if it can't be determined."""
        try:
            result = subprocess.run(
                self.args,
                cwd=self.repo,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                universal_newlines=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except OSError:
            pass


register = template.Library()
convert = Markdown(output_format="html5", extensions=[
    "markdown.extensions.toc",
    "markdown.extensions.smarty",
    "markdown.extensions.fenced_code",
    "markdown.extensions.tables",
    CodeHiliteExtension(),
    ImageVersionExtension(GitVersionProvider(settings.REPOSITORY_ROOT)),
]).convert


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(convert(value))
