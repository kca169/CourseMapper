"""coursemapper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Refs: [1]

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from django.views.generic.base import TemplateView 


urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('accounts.urls')), #from django signup tutorial.
        path('accounts/', include('django.contrib.auth.urls')),
        path('sfu_academic_api_parser/', include('sfu_academic_api_parser.urls')),
        path('treemode/', include('treemode.urls')),

        path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
