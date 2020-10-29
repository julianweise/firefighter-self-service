from django.contrib import admin
from django.contrib.admin import ModelAdmin

from attendance.models import Operation, OtherService
from qualification.models import Training


class CustomOperationAdmin(ModelAdmin):
    list_display = ("start", "end", "operation_id", "code_word", "person_in_charge")
    list_filter = ("code_word", "person_in_charge")
    search_fields = ('code_word', 'start', 'operation_id')
    ordering = ('start', 'end', 'code_word')


admin.site.register(Operation, CustomOperationAdmin)


class CustomOtherServiceAdmin(ModelAdmin):
    list_display = ("start", "end", "name", "person_in_charge")
    list_filter = ("person_in_charge",)
    search_fields = ('name', 'start')
    ordering = ('start', 'end')


admin.site.register(OtherService, CustomOtherServiceAdmin)


class CustomTrainingAdmin(ModelAdmin):
    list_display = ("start", "end", "topic", "person_in_charge")
    list_filter = ("person_in_charge",)
    search_fields = ('topic', 'start')
    ordering = ('start', 'end')


admin.site.register(Training, CustomTrainingAdmin)
