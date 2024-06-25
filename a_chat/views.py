from django.shortcuts import render, get_object_or_404
from a_chat.models import ChatGroup, GroupMessage
from django.contrib.auth.decorators import login_required


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    messages = chat_group.chat_messages.all()[:30]

    return render(request, 'a_chat/chat.html', {'chat_messages': messages})