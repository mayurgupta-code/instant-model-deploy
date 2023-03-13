from django.urls import path
from .views import home, model_predict


urlpatterns = [
    path("", home, name="home"),
    path("model/predict/<int:id>", model_predict, name="model_predict"),
    # path('register/', register_user, name="register"),
    # path("logout/", LogoutView.as_view(), name="logout")
]
app_name = "home"
