from django.urls import path
from .views import home, model_predict, get_predict_result


urlpatterns = [
    path("", home, name="home"),
    path("model/predict/<int:id>", model_predict, name="model_predict"),
    path("model/predict/result/<int:id>", get_predict_result, name="get_predict_result"),
    # path('register/', register_user, name="register"),
    # path("logout/", LogoutView.as_view(), name="logout")
]
app_name = "home"
