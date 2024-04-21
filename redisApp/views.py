from django.shortcuts import render



def index(request,slug=None):
     return render(request,'index.html',{"Group_Name":slug})

       
# Create your views here.
