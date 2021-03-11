from django.urls import path
from . import views

urlpatterns = [
    path('', views.prereqs, name='manual_input'),
    path('directions/', views.directions, name='directions'),
    path('database_search/', views.search, name='database_search'),
    path('error/', views.search, name='error',),
]