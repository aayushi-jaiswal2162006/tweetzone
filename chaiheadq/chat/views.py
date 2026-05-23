from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User

@login_required
def chat_view(request, username):
    other_user = User.objects.get(username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    )

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('chat:chat_view', username=username)
    else:
        form = MessageForm()

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'form': form,
        'other_user': other_user
    })
