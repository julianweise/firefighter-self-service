from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from equipment.models import Pager, Key, Locker
from personal_data.models import Firefighter


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class PersonalEquipmentView(View):

    @staticmethod
    def get(request):
        firefighter = get_object_or_404(Firefighter, id__exact=request.user.id)

        context = {
            'pager': firefighter.pager,
            'key': firefighter.key,
            'locker': firefighter.locker
        }

        return render(request, 'equipment_personal.html', context)


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('equipment.view_pager'), name='dispatch')
class PagerDetailView(DetailView):
    model = Pager
    template_name = "pager_detail.html"
    context_object_name = "pager"


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('equipment.view_key'), name='dispatch')
class KeyDetailView(DetailView):
    model = Key
    template_name = "key_detail.html"
    context_object_name = "key"


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
@method_decorator(permission_required('equipment.view_locker'), name='dispatch')
class LockerDetailView(DetailView):
    model = Locker
    template_name = "locker_detail.html"
    context_object_name = "locker"
