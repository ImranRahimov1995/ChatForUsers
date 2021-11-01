from django.shortcuts import render,redirect
from .forms import UserLogin,SendMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Message, Room
# Create your views here.
from django.core.exceptions import ValidationError
from django.contrib import messages



def login_page(request):
    if request.method == "POST":
        form = UserLogin(request.POST)
       
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], 
                                password=cd['password'])

            if user is not None:
                login(request,user)
            else:
                name = User.objects.filter(username=cd['username'])
                if name:
                    messages.add_message(request, messages.WARNING,
                                             'Username is exists')
                    return redirect('login')
                    
                user=User.objects.create_user(username=cd['username'],
                                                password=cd['password'])
                login(request,user)
            return redirect('my-chats')
    else:
        form = UserLogin()
    return render(request,'auth.html',{'form':form,})






def my_chats(request):
    try:
        current_user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return redirect('login')
    my_rooms = Room.objects.filter(members__in=[request.user])
    last_messages_from_rooms = [room.all_messages.first()
                                     for room in my_rooms]
    context = {
        'owner': current_user,
        'my_messages': last_messages_from_rooms,
    }
    return render(request,'main.html',context)


def chat_detail(request,pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.all_messages.all().order_by('created_at')
    author = User.objects.get(username=request.user)
    recipient = room.members.exclude(pk=author.pk)[0]


    if request.method == "POST":
        form = SendMessage(request.POST,)
        if form.is_valid():
            message = Message.objects.create(author=author,
                                            recipient=recipient,
                                            room=room,
                                            body=form.cleaned_data['body'])
    else:
        form =SendMessage()

    context = {
        'room':room,
        'my_messages': room_messages,
        'form':form,
        'recipient':recipient,
    }
    return render(request,'room.html',context)

