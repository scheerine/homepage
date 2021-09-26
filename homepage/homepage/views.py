from django.views.generic import TemplateView

from entries.models import Entry

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['entries'] = Entry.objects.all()
        return context
