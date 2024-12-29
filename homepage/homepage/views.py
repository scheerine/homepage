from django.views.generic import TemplateView

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Whether we should display the new project
        context['show_reveal'] = True
        return context
