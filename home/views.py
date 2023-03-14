from django.shortcuts import render, redirect
from django.http import HttpResponse
# import login required decorator
from django.contrib.auth.decorators import login_required
from .models import MLModel, MLModelInput
from django.views.decorators.csrf import csrf_exempt
import pickle
import sklearn
import json

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
    # print("model_id", id)
    # get the model
    ml_model = MLModel.objects.get(id=id)
    # get the model inputs
    ml_model_inputs = ml_model.inputs.all()
    context = {
        "ml_model": ml_model,
        "ml_model_inputs": ml_model_inputs
    }
    # print("context", context)
    return render(request, "home/predict.html", {"data": context})


def get_predict_result(request, id):
    if request.method == "POST":
        print("request.POST", request.POST)
        # print("model_id", id)
        # get the model
        ml_model = MLModel.objects.get(id=id)

        # pickle the model
        model_file = ml_model.model_file
        pickled_model = pickle.load(open(model_file.path, 'rb'))
        # print("pickled_model", pickled_model)

        # get data from the request and predict
        # data = request.POST.get_list()
        # print("data", data)
        data_dict = request.POST.dict()
        print("data_dict", data_dict)
        data_dict.pop('csrfmiddlewaretoken')
        
        data_arr = []
        for key, value in data_dict.items():
            data_arr.append(float(value))
        # print("data_arr", data_arr)   
        # print(type(data_arr[0])) 

        ml_result = pickled_model.predict([data_arr])
        print("ml_result", ml_result)
        data = {
            "result": ml_result[0],
            "message": "Predict result successfuly!"
            }

        # data = {'message': 'Hello, world!'}
        json_content = json.dumps(data)
        return HttpResponse(json_content, content_type='application/json; charset=utf-8')  
    
def upload_model(request):
    return render(request, "home/upload_model.html")