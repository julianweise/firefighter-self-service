from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import TemplateView

from attendance.models import Attendance, Operation
from personal_data.models import Firefighter
from qualification.models import Training


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('statistics.view_statistics'), name='dispatch')
class StatisticsAllListView(TemplateView):
    template_name = "statistics_list.html"
    context_object_name = "firefighters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['firefighter_stats'] = []
        for firefighter in Firefighter.objects.filter(is_active=True).order_by("last_name", "first_name"):
            stats = {
                'staff_id': firefighter.staff_id,
                'first_name': firefighter.first_name,
                'last_name': firefighter.last_name,
                'last_operation': Operation.objects.filter(attendees__in=[firefighter]).order_by('end').last(),
                'last_training': Training.objects.filter(attendees__in=[firefighter]).order_by('end').last(),
                'training_total_time': round(sum(
                    d.duration() for d in
                    Training.objects.filter(attendees__in=[firefighter], end__year=now().year)) / (60 * 60), 2),
                'operation_total_time': round(sum(
                    d.duration() for d in
                    Operation.objects.filter(attendees__in=[firefighter], end__year=now().year)) / (60 * 60), 2),
                'prev_year_total_time': round(sum(
                    d.duration() for d in
                    Attendance.objects.filter(attendees__in=[firefighter], end__year=now().year - 1)) / (60 * 60), 2),
                'curr_year_total_time': round(sum(
                    d.duration() for d in
                    Attendance.objects.filter(attendees__in=[firefighter], end__year=now().year)) / (60 * 60), 2)
            }
            context['firefighter_stats'].append(stats)
        return context
