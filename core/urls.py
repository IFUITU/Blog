from django.urls import path
from .views import GenerateRndomuserView, index, random, user_list

urlpatterns = [
    path("", GenerateRndomuserView.as_view()),
    path("user_list/", index,  name="user_list"),
    path('random/', random, name="random"),
    path('ppp/', user_list, name='user_list'),

]