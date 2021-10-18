from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Room(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User,related_name='members')

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('chat_detail',kwargs={'pk':self.pk,})

class Message(models.Model):

    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_sended')
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_delivered')
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='all_messages',null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    body = models.TextField()


    def __str__(self):
        return f"{self.author.username} send message to {self.recipient.username} text {self.body}"

    class Meta:
        ordering = ('-created_at',)