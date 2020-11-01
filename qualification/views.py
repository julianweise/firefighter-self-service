from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, CreateView

from personal_data.models import Firefighter, Authority
from qualification.forms import CreateQualificationForm
from qualification.models import Qualification


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QualificationPersonalListView(TemplateView):
    template_name = "qualification_personal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qualifications'] = Qualification.objects.filter(firefighter=self.request.user)
        return context


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('personal_data.add_qualification'), name='dispatch')
class QualificationCreateForFirefighterView(CreateView):
    model = Qualification
    form_class = CreateQualificationForm
    template_name = "form_qualification.html"

    def get_success_url(self):
        return reverse_lazy("firefighter-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(QualificationCreateForFirefighterView, self).get_context_data(**kwargs)
        context['firefighter'] = Firefighter.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        issuer = Authority.objects.filter().order_by('id')[:1][0]
        return {'firefighter': firefighter, 'issuer': issuer, 'issue_date': now().date()}

    def get_success_message(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        return _("Successfully created new Qualification for ") + f'{firefighter.first_name} {firefighter.last_name}'
