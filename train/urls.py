from django.urls import path
from .views import *


urlpatterns = [
    path("", train_model, name="train_model"),
    path("upload-data/", upload_data, name="upload_data"),
]
app_name = "train"
