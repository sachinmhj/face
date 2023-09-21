from django.shortcuts import render
from django.http import HttpResponse
from .form import customcreatefrom

# Create your views here.
def signup(request):
    if request.method == "POST":
        usercreateform = customcreatefrom(request.POST, request.FILES)   # request.FILES is required for image
        print(usercreateform.errors)
        if usercreateform.is_valid():
            usercreateform.save()
            return render(request,"sineup/sinupSuccess.html")
    else:
        usercreateform = customcreatefrom()
    return render(request,"sineup/sinup.html",{"ctform":usercreateform})