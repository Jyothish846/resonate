from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import ChatThread, Message
from .forms import MessageForm 

User = get_user_model()

@login_required
def inbox_view(request):
    threads = ChatThread.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).distinct()

    context = {
        'threads': threads,
        'page_title': 'Message Inbox'
    }
    return render(request, 'chat/inbox.html', context)

@login_required
def start_thread_view(request, username):

    other_user = get_object_or_404(User, username=username)
    current_user = request.user
    

    if other_user == current_user:
        return redirect('inbox') 

    thread = ChatThread.objects.filter(
        Q(user1=current_user, user2=other_user) | 
        Q(user1=other_user, user2=current_user)
    ).first()

    if not thread:
        thread = ChatThread.objects.create(user1=current_user, user2=other_user)
    
    return redirect('thread', thread_id=thread.id)



@login_required
def thread_view(request, thread_id):
    
    thread = get_object_or_404(ChatThread, id=thread_id)
    

    if request.user not in [thread.user1, thread.user2]:
        return redirect('inbox') 

    messages = thread.messages.all()
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            
            
            thread.save()
            return redirect('thread', thread_id=thread.id) 


    other_user = thread.user1 if thread.user2 == request.user else thread.user2

    context = {
        'thread': thread,
        'messages': messages,
        'form': form,
        'other_user': other_user, 
        'page_title': f'Chat with {other_user.username}'
    }
    return render(request, 'chat/thread.html', context)