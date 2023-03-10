from django.shortcuts import render, redirect
# import login required decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/auth/login/")
def home(request):
    return render(request, "home/index.html")