from django.contrib import admin
from django.contrib.admin import ModelAdmin

from qualification.models import Course, Qualification, LegallyRequiredRecurringTraining, QualificationRequirement


class CustomCourseAdmin(ModelAdmin):
    list_display = ("name", "abbreviation", "administration_level")
    list_filter = ("name", "abbreviation", "administration_level", "requirements")
    search_fields = ("name", "administration_level")
    ordering = ("sorting_order", "name",)


admin.site.register(Course, CustomCourseAdmin)


class CustomQualificationAdmin(ModelAdmin):
    list_display = ("course", "firefighter", "issue_date", "issuer")
    list_filter = ("course", "firefighter", "issue_date", "issuer")
    search_fields = ("course", "firefighter")
    ordering = ("firefighter", "course", "issue_date")


admin.site.register(Qualification, CustomQualificationAdmin)


class CustomLegallyRequiredRecurringTrainingAdmin(ModelAdmin):
    list_display = ("name", "training_course", "recurring_interval")
    list_filter = ("name", "training_course", "recurring_interval")
    search_fields = ("name", "training_course", "recurring_interval")
    ordering = ("name", "training_course", "recurring_interval")


admin.site.register(LegallyRequiredRecurringTraining, CustomLegallyRequiredRecurringTrainingAdmin)


class CustomQualificationRequirementAdmin(ModelAdmin):
    list_display = ("course", "fitness_level", "required_training")
    list_filter = ("course", "fitness_level", "required_training")
    search_fields = ("course", "fitness_level", "required_training")
    ordering = ("course", "fitness_level", "required_training")


admin.site.register(QualificationRequirement, CustomQualificationRequirementAdmin)
