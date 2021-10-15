from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_sended')
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_delivered')
    created_at = models.DateTimeField(auto_now_add=True)

    body = models.TextField()


    def __str__(self):
        return f"{self.author.username} send message to {self.recipient.username}"

    class Meta:
        ordering = ('-created_at',)