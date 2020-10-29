from django.contrib import admin
from django.contrib.admin import ModelAdmin

from fitness.models import Fitness, FitnessLevel

admin.site.register(FitnessLevel)


class CustomFitnessAdmin(ModelAdmin):
    list_display = ("firefighter", "level", "issue_date", "expiration_date")
    list_filter = ("firefighter", "level", "issue_date", "expiration_date")
    search_fields = ('firefighter', 'issue_date', 'expiration_date')
    ordering = ('firefighter', 'level', 'issue_date')


admin.site.register(Fitness, CustomFitnessAdmin)
