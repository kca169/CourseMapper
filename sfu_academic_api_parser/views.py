from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import Http404
from .models import Course
from django.template import loader 

#from .forms import CourseForm
import requests 

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html

# Refs: [3], [4]

def prereqs(request):
    
    # getting form data, convert all to lower-case as that is how the API serves the data.
    year = request.POST.get('year', '').lower()
    semester = request.POST.get('semester', '').lower()
    dep = request.POST.get('department', '').lower()
    num = request.POST.get('course_number', '').lower()
    
    # DEBUG
    '''print(dep)
    print(num)
    print(year)
    print(semester)'''

    url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year}/{semester}/courses/{dep}/{num}' # changed to formatted string
    url_raw = url
    url = requests.get(url)
    courses = url.json()
    template = loader.get_template('sfu_academic_api_parser/directions.html')
    context = {'courses':courses,}

    if url.status_code != 200:
        raise Http404("Cannot find course")
    
    # print(url.status_code) #debug
    # print(url_raw)
    return render(request, 'sfu_academic_api_parser/directions.html', context)

'''def prereqs(request):
    dep = request.POST.get('department', '')
    num = request.POST.get('course_number', '')
    url = 'http://www.sfu.ca/bin/wcm/academic-calendar?2020/spring/courses/' + dep + '/' + num
    url = requests.get(url)
    courses = url.json()
    template = loader.get_template('sfu_academic_api_parser/directions.html')
    context = {'courses':courses,}
    return HttpResponse(template.render(context,request))'''