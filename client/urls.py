from django.urls import path
from .views import signup, SignInOutView, activate

app_name = "client"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("log/", SignInOutView.as_view(), name="sign-in-out"),
    path('activate/<int:uid>/<str:token>-)/',activate, name='activate'),  
]