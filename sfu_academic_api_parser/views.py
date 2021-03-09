from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import Http404
from .models import Course
from django.template import loader 

#from .forms import CourseForm
import requests
import json

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html

# Refs: [3], [4]

def prereqs(request):
    
    # getting form data, convert all to lower-case as that is how the API serves the data.
    year = request.POST.get('year', '').lower()
    semester = request.POST.get('semester', '').lower()
    dep = request.POST.get('department', '').lower()
    num = request.POST.get('course_number', '').lower()
    
    # DEBUG
    # '''print(dep)
    #print(num)
    # print(year)
    # print(semester)'''

    url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year}/{semester}/courses/{dep}/{num}' # changed to formatted string
    url_raw = url
    url = requests.get(url)
    courses = url.json()
    
    
    courses_str = json.dumps(courses)   # Convert 'courses' to a JSON string 
    data = json.loads(courses_str)      # Convert to a Python dictionary
    # print(type(data))     #debug


    #This function takes in a dict key and returns the value related to that key    
    def get_value(a_key):
        value = data[a_key]
        return value 
    
    # print(data) #debug

    #create a Course object from the parsed Json file (aka the dict 'data')
    
    # this solution is cursed, but it seems to work
    # if the page has been initialized, and a field is blank, Django spits out an exception.
    # to solve this, we set the fields to a string with a single space ' ' if the field is blank, and if it isn't blank, the value itself.
    
    course_data = Course(
        title=' ' if get_value("title") == '' else get_value("title"),
        number_str=' ' if get_value("number") == '' else get_value("number"),
        description=' ' if get_value("description") == '' else get_value("description"),
        # prerequisites=get_value("prerequisites"), # this can't be done this way. Pre-reqs must be linked
        units=' ' if get_value("units") == '' else get_value('units'),
    )

    course_data.save()                        # Need to figure out how to chekc if a course already exists 
    new_context = {'course_data':course_data} #This is the context for rendering to directions.html
    
    print(course_data.title)   #debug 

    template = loader.get_template('sfu_academic_api_parser/directions.html')
    # context = {'courses':courses,}            # old context when directly scraping from API

    if url.status_code != 200: 
        raise Http404("Cannot find course")
    
    ## print(url.status_code) #debug
    ## print(url_raw)
    # return render(request, 'sfu_academic_api_parser/directions.html', context)    # previous return from when we directly scraped from API 
    return render(request, 'sfu_academic_api_parser/directions.html', new_context)
   