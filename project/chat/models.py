from django.db import models
from django.contrib.auth.models import User



class Room(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    client1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='client1')
    client2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='client2')

    class Meta:
        unique_together = [['client1', 'client2']]

    def __str__(self):
        return str(self.pk)

class Message(models.Model):

    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_sended')
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_delivered')
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='all_messages',null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    body = models.TextField()


    def __str__(self):
        return f"{self.author.username} send message to {self.recipient.username}"

    class Meta:
        ordering = ('-created_at',)