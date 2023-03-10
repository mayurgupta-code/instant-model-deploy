from django.urls import path
from .views import home


urlpatterns = [
    path("", home, name="home"),
    # path('register/', register_user, name="register"),
    # path("logout/", LogoutView.as_view(), name="logout")
]
