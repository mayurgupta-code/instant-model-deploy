from django.shortcuts import render, redirect
# import login required decorator
from django.contrib.auth.decorators import login_required
from .models import MLModel, MLModelInput

# Create your views here.
@login_required(login_url="/auth/login/")
def home(request):
    # get all the models
    ml_models = MLModel.objects.filter(user=request.user)
    context = {
        "ml_models": ml_models
    }
    return render(request, "home/index.html", {"data": context})