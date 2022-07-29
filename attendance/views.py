from datetime import datetime
from tempfile import NamedTemporaryFile

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, TemplateView
from mailmerge import MailMerge

from attendance.forms import OperationForm, OtherServiceForm, TrainingForm
from attendance.models import Operation, Attendance, OtherService
from attendance.settings import PROTECTED_MEDIA_ROOT
from personal_data.models import Firefighter
from qualification.models import LegallyRequiredRecurringTraining, Training


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_attendance'), name='dispatch')
class OperationListView(ListView):
    model = Operation
    context_object_name = "operations"
    template_name = "operation_list.html"

    ordering = ['-end']


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.add_attendance'), name='dispatch')
class OperationCreateView(SuccessMessageMixin, CreateView):
    model = Operation
    template_name = "form_operation.html"
    success_message = _("Successfully added Operation")
    form_class = OperationForm
    success_url = reverse_lazy("operation-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.change_attendance'), name='dispatch')
class OperationUpdateView(SuccessMessageMixin, UpdateView):
    model = Operation
    template_name = 'form_operation.html'
    form_class = OperationForm
    success_url = reverse_lazy("operation-list")
    success_message = _("Operation has been updated successfully")


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.delete_attendance'), name='dispatch')
class OperationDelete(SuccessMessageMixin, DeleteView):
    model = Operation
    success_message = _("Successfully deleted Operation")
    success_url = reverse_lazy('operation-list')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_attendance'), name='dispatch')
class OtherServiceListView(ListView):
    model = OtherService
    context_object_name = "other_services"
    template_name = "other_service_list.html"

    ordering = ['-end']


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.add_attendance'), name='dispatch')
class OtherServiceCreateView(SuccessMessageMixin, CreateView):
    model = OtherService
    template_name = "form_other_service.html"
    success_message = _("Successfully added Other Service")
    form_class = OtherServiceForm
    success_url = reverse_lazy("other_service-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.change_attendance'), name='dispatch')
class OtherServiceUpdateView(SuccessMessageMixin, UpdateView):
    model = OtherService
    template_name = "form_other_service.html"
    success_message = _("Successfully added Other Service")
    form_class = OtherServiceForm
    success_url = reverse_lazy("other_service-list")


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.delete_attendance'), name='dispatch')
class OtherServiceDelete(SuccessMessageMixin, DeleteView):
    model = OtherService
    success_message = _("Successfully deleted Other Service")
    success_url = reverse_lazy('other_service-list')


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_attendance'), name='dispatch')
class TrainingListView(ListView):
    model = Training
    context_object_name = "trainings"
    template_name = "training_list.html"

    ordering = ['-end']


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.add_attendance'), name='dispatch')
class TrainingCreateView(SuccessMessageMixin, CreateView):
    model = Training
    template_name = "form_training.html"
    success_message = _("Successfully added Training")
    form_class = TrainingForm
    success_url = reverse_lazy("training-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.change_attendance'), name='dispatch')
class TrainingUpdateView(SuccessMessageMixin, UpdateView):
    model = Training
    template_name = "form_training.html"
    success_message = _("Successfully updated Training")
    form_class = TrainingForm
    success_url = reverse_lazy("training-list")

    def get_initial(self):
        return {"person_in_charge": self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.delete_attendance'), name='dispatch')
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

    ordering = ['-end']


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('attendance.view_attendance'), name='dispatch')
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


@login_required(login_url='/accounts/login/')
@permission_required('attendance.create_confirmation')
def download_attendance_confirmation(request, operation, user):
    operation = get_object_or_404(Operation, id__exact=operation)
    firefighter = get_object_or_404(Firefighter, id__exact=user)

    if not firefighter in operation.attendees.all():
        return HttpResponseBadRequest("Firefighter specified did not participate in operation specified.")

    template = staticfiles_storage.path('confirmation/Einsatzbestaetigung_Vorlage.docx')
    document = MailMerge(template)
    document.merge(address_name=f'{firefighter.first_name} {firefighter.last_name}',
                   address_street=str(firefighter.street),
                   address_zip=str(firefighter.zip),
                   address_city=str(firefighter.city),
                   date=str(datetime.today().strftime('%d.%m.%Y')),
                   operation_id=str(operation.operation_id),
                   operation_date=str(operation.start.date().strftime('%d.%m.%Y')),
                   operation_start=str(operation.start.timetz().strftime('%H:%M')),
                   operation_end=str(operation.end.timetz().strftime('%H:%M')))
    filename = f'Einsatzbest_{firefighter.id}_{firefighter.last_name}_{operation.start.strftime("%d.%m.%Y")}.docx'
    with NamedTemporaryFile(suffix='.docx', mode='r+', encoding='utf8', dir=PROTECTED_MEDIA_ROOT) as f:
        document.write(f.name)
        return FileResponse(open(f.name, 'rb'), as_attachment=True, filename=filename)

