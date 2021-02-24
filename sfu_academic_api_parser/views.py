from django.shortcuts import render
from django.http import HttpResponse
from .models import Course
from django.template import loader 
import requests 

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html
def prereqs(request):
    response = requests.get('http://www.sfu.ca/bin/wcm/academic-calendar?2020/spring/courses/cmpt/307')
    courses = response.json()
    template = loader.get_template('sfu_academic_api_parser/directions.html')
    context = {'courses':courses,}
    return HttpResponse(template.render(context,request))