from django.urls import path
from . import views

urlpatterns = [
    path('', views.treemode, name='treemode'),
]