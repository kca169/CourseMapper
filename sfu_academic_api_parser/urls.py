from django.urls import path
from . import views

urlpatterns = [
    path('manual_input/', views.manual_input, name='manual_input'),
    # path('manual_input/', views.manual_input, name='prereqs'),
    path('directions/', views.directions, name='directions'),
    path("automatic_input/", views.automatic_parser, name='automatic_parser'),
    path('database_search/', views.search, name='database_search'),
    path('error/', views.search, name='error',),
]