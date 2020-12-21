from django.contrib.contenttypes.models import ContentType
from django.db import models

from personal_data.models import Firefighter
from qualification.models import Course


class Event(models.Model):
    name = models.CharField(max_length=200)
    start = models.DateTimeField(
        help_text="Insert begin of the event. In case of a multi-day event insert very first day and start time.")
    end = models.DateTimeField(
        help_text="Insert end of the event. In case of a multi-day event insert very last day and end time."
    )
    person_in_charge = models.ForeignKey(Firefighter, on_delete=models.PROTECT, related_name='event_person_in_charge')
    content_type = models.ForeignKey(ContentType, editable=False, null=True, on_delete=models.PROTECT)


class CourseEvent(Event):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="course_event")

    def admission_restrictions_satisfied(self, firefighter: Firefighter):
        return self.course.requirements_satisfied_by(firefighter)


class EventResponse(models.Model):
    firefighter = models.ForeignKey(Firefighter, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    positive = models.BooleanField()
