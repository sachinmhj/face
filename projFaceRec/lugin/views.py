from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def loggin(request):
    if request.method == "POST":
        authen = AuthenticationForm(request=request,data=request.POST)
        if authen.is_valid():
            nem = authen.cleaned_data["username"]
            pwd = authen.cleaned_data["password"]
            uzer = authenticate(username=nem,password=pwd)
            # print(uzer)
            if uzer != None:
                login(request,uzer)
                if request.user.is_superuser:
                    return HttpResponseRedirect("/admin/")
                else:
                    return HttpResponseRedirect("/userProfile/")  
        else:
            return render(request,"lugin/logFailed.html")
    else:
        authen = AuthenticationForm()
    return render(request,"lugin/login.html",{"form":authen})

def lugout(request):
    logout(request)
    return HttpResponseRedirect("/")

        
