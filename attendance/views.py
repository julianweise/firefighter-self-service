from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, TemplateView

from attendance.forms import OperationForm, OtherServiceForm, TrainingForm
from attendance.models import Operation, Attendance, OtherService
from qualification.models import LegallyRequiredRecurringTraining, Training


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_operation'), name='dispatch')
class OperationListView(ListView):
    model = Operation
    context_object_name = "operations"
    template_name = "operation_list.html"


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.add_operation'), name='dispatch')
class OperationCreateView(SuccessMessageMixin, CreateView):
    model = Operation
    template_name = "form_operation.html"
    success_message = _("Successfully added Operation")
    form_class = OperationForm
    success_url = reverse_lazy("operation-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.change_operation'), name='dispatch')
class OperationUpdateView(SuccessMessageMixin, UpdateView):
    model = Operation
    template_name = 'form_operation.html'
    form_class = OperationForm
    success_url = reverse_lazy("operation-list")
    success_message = _("Operation has been updated successfully")


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.delete_operation'), name='dispatch')
class OperationDelete(SuccessMessageMixin, DeleteView):
    model = Operation
    success_message = _("Successfully deleted Operation")
    success_url = reverse_lazy('operation-list')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_other_service'), name='dispatch')
class OtherServiceListView(ListView):
    model = OtherService
    context_object_name = "other_services"
    template_name = "other_service_list.html"


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.add_other_service'), name='dispatch')
class OtherServiceCreateView(SuccessMessageMixin, CreateView):
    model = OtherService
    template_name = "form_other_service.html"
    success_message = _("Successfully added Other Service")
    form_class = OtherServiceForm
    success_url = reverse_lazy("other_service-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.change_other_service'), name='dispatch')
class OtherServiceUpdateView(SuccessMessageMixin, UpdateView):
    model = OtherService
    template_name = "form_other_service.html"
    success_message = _("Successfully added Other Service")
    form_class = OtherServiceForm
    success_url = reverse_lazy("other_service-list")


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.delete_other_service'), name='dispatch')
class OtherServiceDelete(SuccessMessageMixin, DeleteView):
    model = OtherService
    success_message = _("Successfully deleted Other Service")
    success_url = reverse_lazy('other_service-list')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_training'), name='dispatch')
class TrainingListView(ListView):
    model = Training
    context_object_name = "trainings"
    template_name = "training_list.html"


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.add_training'), name='dispatch')
class TrainingCreateView(SuccessMessageMixin, CreateView):
    model = Training
    template_name = "form_training.html"
    success_message = _("Successfully added Training")
    form_class = TrainingForm
    success_url = reverse_lazy("training-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.change_training'), name='dispatch')
class TrainingUpdateView(SuccessMessageMixin, UpdateView):
    model = Training
    template_name = "form_training.html"
    success_message = _("Successfully updated Training")
    form_class = TrainingForm
    success_url = reverse_lazy("training-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.delete_training'), name='dispatch')
class TrainingDelete(SuccessMessageMixin, DeleteView):
    model = Training
    success_message = _("Successfully deleted Training")
    success_url = reverse_lazy('training-list')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_attendance'), name='dispatch')
class AttendanceListView(ListView):
    model = Attendance
    context_object_name = "attendances"
    template_name = "attendance_list.html"


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class TrainingParticipatedListView(TemplateView):
    template_name = "training_participated_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainings'] = Training.objects.filter(end__year=now().year,
                                                       attendees__in=[self.request.user])
        context['required_trainings'] = LegallyRequiredRecurringTraining.objects \
            .filter(training_course__required_for_qualification__firefighter=self.request.user)
        context['fulfilled_required_trainings'] = LegallyRequiredRecurringTraining.objects \
            .filter(satisfied_by__attendees__in=[self.request.user], satisfied_by__end__year=now().year)
        return context
