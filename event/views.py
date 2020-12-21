from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.utils.translation import gettext as _

from event.forms import CreateEventForm, CreateCourseEventForm
from event.models import Event, CourseEvent


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('event.view_event'), name='dispatch')
class EventListView(ListView):
    model = Event
    context_object_name = "events"
    template_name = "event_list.html"


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('event.add_event'), name='dispatch')
class EventCreateView(SuccessMessageMixin, CreateView):
    model = Event
    form_class = CreateEventForm
    template_name = "form_event.html"
    success_message = _("Successfully created Event")
    success_url = reverse_lazy('event-list')

    def get_initial(self):
        return {'person_in_charge': self.request.user}


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('event.add_course_event'), name='dispatch')
class CourseEventCreateView(SuccessMessageMixin, CreateView):
    model = CourseEvent
    form_class = CreateCourseEventForm
    template_name = "form_course_event.html"
    success_message = _("Successfully created Course Event")
    success_url = reverse_lazy('event-list')

    def get_initial(self):
        return {'person_in_charge': self.request.user}
