from django.shortcuts import render
from .models import group_chat_message
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login,logout

def index(request,slug=None):
     if request.user.is_authenticated:
          if slug is not None:
               all_msgs=group_chat_message.objects.filter(group_name=slug).order_by('created_time')
     
          else:
               all_msgs=group_chat_message.objects.filter(group_name='public').order_by('created_time')

          return render(request,'index.html',{"Group_Name":slug,"all_msg":all_msgs})
     else:
          return render(request,'index.html',{"Group_Name":slug})


def signup(request):
     if request.method=="POST":
          data=request._post
          username=data.get('username')
          password=data.get('password')
          if User.objects.filter(username=username).exists():
               messages.warning(request,"Username Alreay Exist")
               return JsonResponse({"status":False})
          user = User.objects.create_user(username=username,password=password)
          if user is not None:
           messages.success(request,"Signup Success")
           return JsonResponse({"status":True})

     else:
          messages.warning(request,"Unauthorized Access")
          return JsonResponse({"status":False})   

def logout_user(request):
     if request.user.is_authenticated:
          logout(request)
          messages.success(request,"Logout Successfully")
          return JsonResponse({"status":True}) 
     else:
          messages.success(request,"Something Went Wrong")
          return JsonResponse({"status":False}) 
     
def login_user(request):
     if request.method=="POST":
          data=request._post
          username=data.get('username')
          password=data.get('password')
          user=authenticate(username=username,password=password)
          if user is not None:
               login(request,user)
               messages.success(request,"Login Success")
               return JsonResponse({"status":True}) 
          else:
               messages.warning(request,"Invalid Credentials")
               return JsonResponse({"status":False})
     else:
          messages.warning(request,"Unauthorized Access")
          return JsonResponse({"status":False})     

