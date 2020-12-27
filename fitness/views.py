from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, CreateView

from fitness.forms import CreateFitnessForm
from fitness.models import Fitness
from personal_data.models import Firefighter


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('fitness.view_fitness'), name='dispatch')
class FitnessPersonalListView(TemplateView):
    template_name = "fitness_personal_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fitness_statements'] = Fitness.objects.filter(firefighter=self.request.user) \
            .order_by('level', '-expiration_date') \
            .distinct('level')
        return context


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('fitness.add_fitness'), name='dispatch')
class FitnessCreateForFirefighterView(CreateView):
    model = Fitness
    form_class = CreateFitnessForm
    template_name = "form_fitness.html"

    def get_success_url(self):
        return reverse_lazy("firefighter-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(FitnessCreateForFirefighterView, self).get_context_data(**kwargs)
        context['firefighter'] = Firefighter.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        return {'firefighter': Firefighter.objects.get(pk=self.kwargs['pk'])}

    def get_success_message(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        return _("Successfully created new Fitness Level for ") + f'{firefighter.first_name} {firefighter.last_name}'
