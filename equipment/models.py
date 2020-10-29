from django.db import models


class Pager(models.Model):
    pager_id = models.CharField(max_length=100)

    def __str__(self):
        return f'Pager#{self.pager_id}'


class Locker(models.Model):
    locker_id = models.CharField(max_length=10)

    def __str__(self):
        return f'Locker#{self.locker_id}'


class Room(models.Model):
    room_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Room#{self.room_id}:  {self.name}'


class Key(models.Model):
    access_rights = models.ManyToManyField(Room, blank=True, help_text='Select rooms the key provides access to')

    def __str__(self):
        return f'Key#{self.id}'
