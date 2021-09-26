import json

from django.core.management.base import BaseCommand
from django.conf import settings

from gitload.repository import GitRepository
from entries.models import Entry


class Command(BaseCommand):
    help = 'Synchronizes with the Git repository and loads entries into the system.'

    def handle(self, *args, **options):
        if not settings.GITLOAD_URL:
            self.stderr.write('GITLOAD_URL not configured.')
            return
        if not settings.GITLOAD_BRANCH:
            self.stderr.write('GITLOAD_BRANCH not configured.')
            return
        if not settings.REPOSITORY_ROOT:
            self.stderr.write('REPOSITORY_ROOT not configured.')
            return

        repository = GitRepository(
            settings.REPOSITORY_ROOT,
            url=settings.GITLOAD_URL,
            branch=settings.GITLOAD_BRANCH
        )
        repository.synchronize()
        self.synchronize(repository)

    def synchronize_entry(self, readme_path):
        entry_path = readme_path.parent
        entry_slug = entry_path.name
        entry_meta_path = entry_path / 'meta.json'

        if not entry_meta_path.exists():
            print(
                f'Readme {readme_path} lacks meta.json file. '
                f'Add a meta.json file to the path to include '
                f'this entry into the application.'
            )
            return

        with open(readme_path, 'r') as f:
            entry_markdown = f.read()
        with open(entry_meta_path, 'r') as f:
            entry_meta = json.loads(f.read())

        defaults = {
            'markdown': entry_markdown,
            'title': entry_meta['title'],
            'description': entry_meta['description'],
            'authors': entry_meta.get('authors'),
            'tags': entry_meta.get('tags'),
            'thumbnail': entry_meta.get('thumbnail'),
        }

        _, was_created = Entry.objects.update_or_create(
            slug=entry_slug,
            defaults=defaults
        )

    def synchronize(self, repository):
        for readme_path in repository.find_files('**/readme.md'):
            self.synchronize_entry(readme_path)
