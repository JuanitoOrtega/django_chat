from django.shortcuts import render, get_object_or_404, redirect
from a_chat.models import ChatGroup, GroupMessage
from django.contrib.auth.decorators import login_required
from a_chat.forms import ChatmessageCreateForm, NewGroupForm, ChatRoomEditForm


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            context = {
                'message': message,
                'user': request.user,
            }

            return render(request, 'a_chat/partials/chat_message_p.html', context)

    return render(request, 'a_chat/chat.html', {'chat_messages': messages, 'form': form})