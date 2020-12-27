import logging
import re

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

ATTENDANCE_DEFAULT_MODELS = ["Attendance", "Operation", "OtherService"]
PERSONAL_DATA_DEFAULT_MODELS = ["Authority", "CategoryOfDriverLicense", "Rank", "UserStatus", "RankAssignment",
                                "DriverLicense", "Honor", "HonorAssignment", "Role", "RoleAssignment"]
EQUIPMENT_DEFAULT_MODELS = ["Pager", "Locker", "Key", "Room"]
FITNESS_DEFAULT_MODELS = ["Fitness", "FitnessLevel"]
QUALIFICATION_DEFAULT_MODELS = ["CourseRequirement", "Course", "Qualification", "LegallyRequiredRecurringTraining",
                                "Training", "QualificationRequirement"]

ALL_DEFAULT_MODELS = [("attendance", ATTENDANCE_DEFAULT_MODELS), ("personal_data", PERSONAL_DATA_DEFAULT_MODELS),
                      ("equipment", EQUIPMENT_DEFAULT_MODELS), ("fitness", FITNESS_DEFAULT_MODELS),
                      ("qualification", QUALIFICATION_DEFAULT_MODELS)]

CAMEL_CASE_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')


class Command(BaseCommand):
    help = 'Creates basic permission groups for users'

    def handle(self, *args, **options):
        members, _ = Group.objects.get_or_create(name="Members")
        lieutenants, _ = Group.objects.get_or_create(name="Lieutenant")
        captains, _ = Group.objects.get_or_create(name="Captains")

        for namespace, models in ALL_DEFAULT_MODELS:
            for model in models:
                _model = CAMEL_CASE_PATTERN.sub('', model).lower()
                Command.assign_permission(members, namespace, "view", _model)
                Command.assign_permission(lieutenants, namespace, "view", _model)
                Command.assign_permission(captains, namespace, "view", _model)
                Command.assign_permission(captains, namespace, "add", _model)
                Command.assign_permission(captains, namespace, "change", _model)
                Command.assign_permission(captains, namespace, "delete", _model)

        Command._assign_permission(lieutenants, "add_attendance")
        Command._assign_permission(lieutenants, "change_attendance")
        Command._assign_permission(lieutenants, "delete_attendance")
        Command._assign_permission(lieutenants, "add_operation")
        Command._assign_permission(lieutenants, "change_operation")
        Command._assign_permission(lieutenants, "delete_operation")
        Command._assign_permission(lieutenants, "add_otherservice")
        Command._assign_permission(lieutenants, "change_otherservice")
        Command._assign_permission(lieutenants, "delete_otherservice")

        # Custom permissions
        Command._assign_permission(captains, "view_all_attendance")
        Command._assign_permission(lieutenants, "view_all_attendance")
        Command._assign_permission(captains, "view_all_firefighter")
        Command._assign_permission(lieutenants, "view_all_firefighter")
        Command._assign_permission(captains, "view_detail_firefighter")

    @staticmethod
    def assign_permission(group: Group, namespace: str, action: str, model: str):
        Command._assign_permission(group, f'{action}_{model}')

    @staticmethod
    def _assign_permission(group: Group, permission_name: str):
        try:
            model_add_perm = Permission.objects.get(codename=permission_name)
        except Permission.DoesNotExist:
            logging.warning("Permission not found with name '{}'.".format(permission_name))
            return
        group.permissions.add(model_add_perm)
