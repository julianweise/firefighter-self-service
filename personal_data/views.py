from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from fitness.models import Fitness
from personal_data.forms import UpdatePersonalDataPersonalForm, CreatePersonalDataForm, UpdatePersonalDataForm, \
    CreateDriverLicenseForm, CreateRankAssignmentForm, CreateHonorAssignmentForm, CreateRoleAssignmentForm
from personal_data.models import RankAssignment, Firefighter, DriverLicense, Honor, HonorAssignment, RoleAssignment, \
    Rank, Authority
from qualification.models import Course, Qualification


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class PersonalDataPersonalUpdateView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "form": UpdatePersonalDataPersonalForm(instance=self.request.user),
            "ranks": RankAssignment.objects.filter(firefighter=self.request.user).order_by('-issue_date'),
            "honors": HonorAssignment.objects.filter(firefighter=self.request.user).order_by('-issue_date'),
            "firefighter": self.request.user
        }
        return render(request, 'form_personal_data.html', context=context)

    def post(self, request, *args, **kwargs):
        form = UpdatePersonalDataPersonalForm(instance=self.request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _("Successfully updated personal data"))
            return HttpResponseRedirect(reverse_lazy('personal-data-update'))
        else:
            context = {
                "form": form,
                "ranks": RankAssignment.objects.filter(firefighter=self.request.user).order_by('-issue_date'),
                "honors": HonorAssignment.objects.filter(firefighter=self.request.user).order_by('-issue_date'),
                "firefighter": self.request.user
            }
            messages.error(request, _("The form has not be filled correctly"))
            return render(request, 'form_personal_data.html', context=context)


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('personal_data.view_firefighter'), name='dispatch')
@method_decorator(permission_required('personal_data.view_all_firefighter'), name='dispatch')
class PersonalDataListView(ListView):
    model = Firefighter
    context_object_name = "firefighters"
    template_name = "firefighter_list.html"

    def get_context_data(self, **kwargs):
        context = super(PersonalDataListView, self).get_context_data(**kwargs)
        grouped = dict()
        for firefighter in Firefighter.objects.filter(is_active=True).order_by("last_name", "first_name"):
            grouped.setdefault(firefighter.id, {})
        for qualification in Qualification.objects.all():
            grouped[qualification.firefighter.id][qualification.course] = qualification
        context.update({
            'firefighters': Firefighter.objects.filter(is_active=True).order_by("last_name", "first_name"),
            'qualifications': grouped,
            'courses': Course.objects.filter(show_in_overview=True),
        })
        return context


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('personal_data.view_firefighter'), name='dispatch')
@method_decorator(permission_required('personal_data.view_detail'), name='dispatch')
class PersonalDataDetailView(DetailView):
    model = Firefighter
    context_object_name = "firefighter"
    template_name = "firefighter_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PersonalDataDetailView, self).get_context_data(**kwargs)
        context.update({
            'firefighter': kwargs['object'],
            'ranks': Rank.objects.all().order_by("sorting_order"),
            'promotions': RankAssignment.group_by_rank(RankAssignment.objects.filter(firefighter=kwargs['object'])),
            'qualifications': Qualification.group_by_course(Qualification.objects.filter(firefighter=kwargs['object'])),
            'courses': Course.objects.all(),
            'fitness': Fitness.objects.filter(firefighter=kwargs['object']).order_by('-expiration_date')[:1],
            'driver_license': DriverLicense.objects.filter(owner=kwargs['object']).order_by('-issue_date')[:1],
            'honors': Honor.objects.all(),
            'honors_received': HonorAssignment.group_by_honor(
                HonorAssignment.objects.filter(firefighter=kwargs['object'])),
            'roles': RoleAssignment.objects.filter(firefighter=kwargs['object']).order_by('end')
        })
        return context


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
@method_decorator(permission_required('personal_data.delete_firefighter'), name='dispatch')
class PersonalDataDeleteView(SuccessMessageMixin, DeleteView):
    model = Firefighter
    success_url = reverse_lazy('firefighter-list')
    success_message = _("Successfully deleted Firefighter")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
@method_decorator(permission_required('personal_data.add_firefighter'), name='dispatch')
class PersonalDataCreateView(SuccessMessageMixin, CreateView):
    model = Firefighter
    success_url = reverse_lazy('firefighter-list')
    success_message = _("Successfully created new Firefighter")
    form_class = CreatePersonalDataForm
    template_name = "form_firefighter.html"


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
@method_decorator(permission_required('personal_data.change_firefighter'), name='dispatch')
class PersonalDataUpdateView(SuccessMessageMixin, UpdateView):
    model = Firefighter
    success_message = _("Successfully updated Firefighter")
    form_class = UpdatePersonalDataForm
    template_name = "form_firefighter.html"

    def get_success_url(self):
        return reverse_lazy('firefighter-detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('personal_data.add_driver_license'), name='dispatch')
class DriverLicenseCreateForFirefighterView(CreateView):
    model = DriverLicense
    form_class = CreateDriverLicenseForm
    template_name = "form_driver_license.html"

    def get_success_url(self):
        return reverse_lazy("firefighter-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(DriverLicenseCreateForFirefighterView, self).get_context_data(**kwargs)
        context['firefighter'] = Firefighter.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        return {'owner': Firefighter.objects.get(pk=self.kwargs['pk'])}

    def get_success_message(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        return _("Successfully created new Driver License for ") + f'{firefighter.first_name} {firefighter.last_name}'


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('personal_data.add_rank_assignment'), name='dispatch')
class RankAssignmentCreateForFirefighterView(CreateView):
    model = RankAssignment
    form_class = CreateRankAssignmentForm
    template_name = "form_rank_assignment.html"

    def get_success_url(self):
        return reverse_lazy("firefighter-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(RankAssignmentCreateForFirefighterView, self).get_context_data(**kwargs)
        context['firefighter'] = Firefighter.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        rank = RankAssignment.objects.filter(firefighter=firefighter).order_by("-issue_date")[:1]
        next_rank = Rank.objects.filter(sorting_order__gt=rank[0].rank.sorting_order).order_by("sorting_order")[:1][0] \
            if len(rank) > 0 else None
        issuer = Authority.objects.filter().order_by('id')[:1][0]
        return {'firefighter': firefighter, 'rank': next_rank, 'issuer': issuer,
                'issue_date': now().date}

    def get_success_message(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        return _("Successfully created new Driver License for ") + f'{firefighter.first_name} {firefighter.last_name}'


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('personal_data.add_honor_assignment'), name='dispatch')
class HonorAssignmentCreateForFirefighterView(CreateView):
    model = HonorAssignment
    form_class = CreateHonorAssignmentForm
    template_name = "form_honor_assignment.html"

    def get_success_url(self):
        return reverse_lazy("firefighter-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(HonorAssignmentCreateForFirefighterView, self).get_context_data(**kwargs)
        context['firefighter'] = Firefighter.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        issuer = Authority.objects.filter().order_by('id')[:1][0]
        return {'firefighter': firefighter, 'issuer': issuer, 'issue_date': now().date}

    def get_success_message(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        return _("Successfully assigned new Honor to ") + f'{firefighter.first_name} {firefighter.last_name}'


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('personal_data.add_role_assignment'), name='dispatch')
class RoleAssignmentCreateForFirefighterView(CreateView):
    model = RoleAssignment
    form_class = CreateRoleAssignmentForm
    template_name = "form_role_assignment.html"

    def get_success_url(self):
        return reverse_lazy("firefighter-detail", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(RoleAssignmentCreateForFirefighterView, self).get_context_data(**kwargs)
        context['firefighter'] = Firefighter.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        issuer = Authority.objects.filter().order_by('id')[:1][0]
        return {'firefighter': firefighter, 'issuer': issuer, 'start': now().date}

    def get_success_message(self):
        firefighter = Firefighter.objects.get(pk=self.kwargs['pk'])
        return _("Successfully assigned new Role to ") + f'{firefighter.first_name} {firefighter.last_name}'
