from django.shortcuts import render,redirect
from .forms import UserLogin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def login_page(request):
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request,user)
            else:
                user=User.objects.create(username=cd['username'], password=cd['password'])
                login(request,user)
            return redirect('my-chats')
    else:
        form = UserLogin()
    return render(request,'auth.html',{'form':form,})


def my_chats(request):
    return render(request,'main.html',{})