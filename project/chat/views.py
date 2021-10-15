from django.shortcuts import render,redirect
from .forms import UserLogin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Message
# Create your views here.
from django.core.exceptions import ValidationError
from django.contrib import messages

def login_page(request):
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request,user)
            else:
                name = User.objects.filter(username=cd['username'])
                if name:
                    messages.add_message(request, messages.WARNING, 'Username is exists')
                    return redirect('login')
                user=User.objects.create(username=cd['username'], password=cd['password'])
                login(request,user)
            return redirect('my-chats')
    else:
        form = UserLogin()
    return render(request,'auth.html',{'form':form,})






def my_chats(request):
    pass















# def my_chats(request):
#     owner = User.objects.get(username=request.user)
#     my_messages = owner.message_delivered.all()
#    # my_messages.extend(owner.message_sended.all())
#     my_sended_messages = owner.message_sended.all()
#     print(my_sended_messages)
#     unique_author = []
#     unique_author_messages = []
#
#     for my_message in my_messages:
#         if my_message.author not in unique_author:
#             unique_author.append(my_message.author)
#             unique_author_messages.append(my_messages.filter(author=my_message.author).first())
#
#
#     for my_message in my_sended_messages:
#         if my_message.author not in unique_author:
#             unique_author.append(my_message.author)
#             unique_author_messages.append(my_messages.filter(author=my_message.author).first())
#
#     context = {
#         'owner': owner,
#         'my_messages': unique_author_messages,
#     }
#     print(unique_author,unique_author_messages)
#     return render(request,'main.html',context)