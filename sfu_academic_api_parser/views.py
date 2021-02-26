from django.shortcuts import render
from django.http import HttpResponse
from .models import Course
from django.template import loader 

import requests
import json


# based upon the previous "prereqs" function, but is meant to call upon the class model
def getAndParseJSON(request):
    department = request.POST.get('department', '')
    course_num = request.POST.get('course_number', '')
    semester = request.POST.get('semester', '')
    url = 'http://www.sfu.ca/bin/wcm/academic-calendar?2020/spring/courses/' + department.lower() + '/' + course_num # Grabs JSON
    url = requests.get(url)
    json_raw = url.json()
    Course.extract_data(json_raw) # im not sure this is going to work. Need to figure out how to use this datastructure
    # template = loader.get_template('sfu_academic_api_parser/lookup.html')
    # context = {'json_':courses,}
    

    return HttpResponse(output)
    # return HttpResponse(template.render(context,request))

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html
def prereqs(request):
    dep = request.POST.get('department', '')
    num = request.POST.get('course_number', '')
    url = 'http://www.sfu.ca/bin/wcm/academic-calendar?2020/spring/courses/' + dep.lower() + '/' + num
    url = requests.get(url)
    courses = url.json()
    template = loader.get_template('sfu_academic_api_parser/directions.html')
    
    context = {'courses':courses,}
    return HttpResponse(template.render(context,request))