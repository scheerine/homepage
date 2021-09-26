import json

from huey.contrib.djhuey import db_task

from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt

from gitload.models import GitloadToken


@db_task()
def call_gitload_async():
    """
    Call the gitload command asynchronously.

    Use the huey task queue for this.
    """
    call_command('gitload')


@csrf_exempt
def trigger_gitload(request):
    """
    A json endpoint view to trigger a gitload.

    This endpoint is used by the continuous publishing
    workflow in the entries repository. The access to
    this endpoint requires the caller to pass a valid
    token value, which has to be created via the
    admin interface. The gitload is called asynchronously.
    """
    if request.method != 'POST':
        raise Http404
    token_value = request.POST.get('token_value')
    if not token_value:
        payload = json.loads(request.body)
        token_value = payload.get('token_value')
        if not token_value:
            raise Http404
    get_object_or_404(GitloadToken, pk=token_value)
    call_gitload_async()
    response = JsonResponse({'success': True})
    response["Access-Control-Allow-Origin"] = "*"
    return response
