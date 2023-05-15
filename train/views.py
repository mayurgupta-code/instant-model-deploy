from django.shortcuts import render, HttpResponse

# Create your views here.

def upload_data(request):
    return render(request, "train/upload_data.html")

def train_model(request): 
    return render(request, "train/train_model.html")