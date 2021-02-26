from django.shortcuts import render
from django.http import HttpResponse
from .models import Course
from django.template import loader 
import requests 


# based upon the previous "prereqs" function, but is meant to 
def getAndParseJSON(reqeust):
    # stub

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html
def prereqs(request):
    dep = request.POST.get('department', '')
    num = request.POST.get('course_number', '')
    url = 'http://www.sfu.ca/bin/wcm/academic-calendar?2020/spring/courses/' + dep + '/' + num
    url = requests.get(url)
    courses = url.json()
    template = loader.get_template('sfu_academic_api_parser/directions.html')
    context = {'courses':courses,}
    return HttpResponse(template.render(context,request))