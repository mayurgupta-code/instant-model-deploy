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


def model_predict(request, id):
    print("model_id", id)
    # get the model
    ml_model = MLModel.objects.get(id=id)
    # get the model inputs
    ml_model_inputs = MLModelInput.objects.filter(model=ml_model)
    context = {
        "ml_model": ml_model,
        "ml_model_inputs": ml_model_inputs
    }
    return render(request, "home/predict.html", {"data": context})    