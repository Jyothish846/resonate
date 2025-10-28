from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class ChatThread(models.Model):
    user1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='chat_threads_as_user1'
    )
    user2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='chat_threads_as_user2'
    )
    
    updated = models.DateTimeField(auto_now=True) 
    timestamp = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-updated'] 

    def __str__(self):
        return f"Thread between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    thread = models.ForeignKey(
        ChatThread, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message by {self.sender.username} in Thread {self.thread.id}"