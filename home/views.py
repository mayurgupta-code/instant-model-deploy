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

@csrf_exempt
def get_predict_result(request, id):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        input_data_str = data.get('inputValues')
        print("input_data_str", input_data_str)
        input_data = [float(x) for x in input_data_str] 
        print("input_data", input_data)
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
        # data_dict = request.POST.dict()
        # print("data_dict", data_dict)
        # data_dict.pop('csrfmiddlewaretoken')
        
        # data_arr = []
        # for key, value in data_dict.items():
        #     data_arr.append(float(value))
        # print("data_arr", data_arr)   
        # print(type(data_arr[0])) 

        ml_result = pickled_model.predict([input_data])
        print("ml_result", ml_result)
        print("type(ml_result[0])", type(ml_result[0]))
        
        data = {
            "result": ml_result[0],
            "message": "Predict result successfuly!"
            }
        if type(ml_result[0]) != int:
            # print("here")
            ml_result = str(ml_result[0])
            # print("ml_result", ml_result)
            data = {
                "result": ml_result,
            }
        # data = {'message': 'Hello, world!'}
        json_content = json.dumps(data)
        return HttpResponse(json_content, content_type='application/json; charset=utf-8')  
    
def upload_model(request):
    if request.method == "POST":
        print("request.POST", request.POST.dict())
        data_dict = request.POST.dict()
        data_dict.pop('csrfmiddlewaretoken')
        ml_model = MLModel(
            name=data_dict.get('model_name'),
            description=data_dict.get('model_desc'),
            model_file=data_dict.get('model_file'),
            accuracy=data_dict.get('accuracy'),
            output=data_dict.get('model_output_name'),
            user=request.user,
        )
        ml_model.save()
        # get the model inputs
        for i in range(1, int(data_dict.get('input_count'))+1):
            ml_model_input = MLModelInput(
                name=data_dict.get('input-name-'+str(i)),
                input_type=data_dict.get('input-type-'+str(i)),
                model=ml_model
            )
            ml_model_input.save()

        
    return render(request, "home/upload_model.html")