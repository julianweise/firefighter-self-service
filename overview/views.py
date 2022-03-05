from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import TemplateView

from attendance.models import Attendance
from fitness.models import Fitness
from personal_data.models import DriverLicense


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class OverviewView(TemplateView):
    template_name = "overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_attendances = Attendance.objects.filter(attendees__in=[self.request.user],
                                                     end__lte=now()).order_by('-end')[:5]
        attendances_current_year = Attendance.objects.filter(attendees__in=[self.request.user],
                                                             end__year=datetime.now().year)
        driver_licenses = DriverLicense.objects.filter(owner=self.request.user).order_by('-expiration_date')[:1]
        fitness_certificates = Fitness.objects.filter(firefighter=self.request.user) \
            .order_by('level', '-expiration_date') \
            .distinct('level')
        context['firefighter'] = self.request.user
        context['attendances'] = last_attendances
        context['hours_served'] = round(sum(a.duration() for a in attendances_current_year) / 3600)
        context['expiring_fitness'] = [f for f in fitness_certificates if f.about_to_expire()]
        context['expiring_driver_license'] = [d for d in driver_licenses if d.about_to_expire()]
        return context
