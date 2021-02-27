from django.shortcuts import render
from django.http import HttpResponse
from .models import Course
from django.template import loader 
#from .forms import CourseForm
import requests 

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html

def prereqs(request):
    
    year = request.POST.get('year', '')
    semester = request.POST.get('semester', '')
    dep = request.POST.get('department', '')
    num = request.POST.get('course_number', '')
    
    print(dep)
    print(num)
    print(year)
    print(semester)

    url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year}/{semester}/courses/{dep}/{num}' # changed to formatted string
    url_raw = url
    url = requests.get(url)
    courses = url.json()
    template = loader.get_template('sfu_academic_api_parser/directions.html')
    context = {'courses':courses,}
    print(url.status_code) #debug
    print(url_raw)
    return HttpResponse(template.render(context,request))

'''def prereqs(request):
    dep = request.POST.get('department', '')
    num = request.POST.get('course_number', '')
    url = 'http://www.sfu.ca/bin/wcm/academic-calendar?2020/spring/courses/' + dep + '/' + num
    url = requests.get(url)
    courses = url.json()
    template = loader.get_template('sfu_academic_api_parser/directions.html')
    context = {'courses':courses,}
    return HttpResponse(template.render(context,request))'''