from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{str(self.room)} - {self.sender}"
# Create your models here.
