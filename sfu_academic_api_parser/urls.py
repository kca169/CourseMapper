from django.urls import path
from . import views

urlpatterns = [
    path('', views.prereqs, name='prereqs'),
    path('directions/', views.directions, name='directions'),
]