from django.urls import path
from . import views


urlpatterns = [
    path('',views.login_page,name='login'),
    path('my-chats/',views.my_chats,name='my-chats'),
]
