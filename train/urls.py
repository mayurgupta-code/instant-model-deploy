from django.urls import path
from .views import *


urlpatterns = [
    path("", train_model, name="train_model"),
    path("data-feature/", data_feature, name="data_feature"),
    path("upload-data/", upload_data, name="upload_data"),
]
app_name = "train"
