from django.urls import path
from . import views

urlpatterns = [
    # Three links. Index (not created), manual input and database_search
    # path('', views.index, name='index'),
    path('manual_input/', views.prereqs, name='prereqs'),
    path('database_search/', views.search, name='database_search'),
]