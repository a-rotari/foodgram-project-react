from django.urls import path

from . import views

urlpatterns = [
    path('token/login/', views.CustomAuthToken.as_view()),
    path('token/logout/', views.DeleteAuthToken.as_view())
]
