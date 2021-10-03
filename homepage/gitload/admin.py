from django.contrib import admin
from django.apps import apps


app = apps.get_app_config('gitload')

for _, model in app.models.items():
    admin.site.register(model)
