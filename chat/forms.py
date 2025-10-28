from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 1, 
                'placeholder': 'Type a message...',
                'class': 'chat-input-textarea'
            })
        }