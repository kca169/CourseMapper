from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import Http404, HttpResponseNotFound
from .models import Course
from django.template import loader 

#from .forms import CourseForm
import requests
import json

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html

# Refs: [3], [4]

def search(request):

    # getting form data
    year = request.POST.get('year', '')
    semester = request.POST.get('semester', '').capitalize()
    course_code = request.POST.get('department', '').upper()
    num = request.POST.get('course_number', '')
    
    # DEBUG
    # '''print(dep)
    #print(num)
    # print(year)
    # print(semester)'''


    # To search for W courses, if the cast to int fails, we cut off the last letter and try again
    if year != '':
        try:
            num_to_search = int(num)
        except:
            num_to_search = int(num[:-1])

        year_to_search = int(year)

        try:
            course_to_search = Course.objects.get(code=course_code, number=num_to_search, year=year_to_search, semester=semester)
        except:
            return HttpResponseNotFound('<h1>Course not found</h1>')

        # Load error page if not found!
        # if not course_to_search:
        #     template = loader.get_template('sfu_academic_api_parser/error.html')
        #     return render(request, 'sfu_academic_api_parser/error.html')

        search_context = {'search_context':course_to_search}
        
        # Debug course search
        # print(course_to_search)

        template = loader.get_template('sfu_academic_api_parser/database_search.html')
        # context = {'courses':courses,}            # old context when directly scraping from API

        # return render(request, 'sfu_academic_api_parser/directions.html', context)    # previous return from when we directly scraped from API 
    else:
        # Default context for new initialization
        search_context = {'search_context':Course()}
    
    return render(request, 'sfu_academic_api_parser/database_search.html', search_context)

def manual_input(request):

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

    #this function identify_prereqs() gets rid of the filler in prerequisites and returns only the prereq codes as a string
    def identify_prereqs(preq):
        coursecodes_list = ['CMPT', 'MATH', 'MACM', 'ENSC']
        bad_chars = ['(', ')',',','.',':',';']
        result_list = list()
        prereq_list = list()
        index = 0

        HScourselist = ['Pre-Calculus', 'BC Math 12']

        preq = ''.join(i for i in preq if not i in bad_chars)
        prereq_list = preq.split()

        for bad in HScourselist:
            if bad in preq:
                return result_list

        for words in prereq_list:
            if words in coursecodes_list:
                #print("The position of " + words + " word: ", index)
                result_list.append(words + " " + prereq_list[index+1])
            index +=1

        index = 0        
        for i in range(len(prereq_list)-1):
            if 'and' in prereq_list[i]:
                #print("Index of 'and' is " + str(i) )
                if prereq_list[i+1].isdigit():
                    result_list.append(prereq_list[i-2] + " " + prereq_list[i+1])
        #print (result_list)
        return result_list

    def recursive_list(prereq_list):
        #for i in range(len(prereq_list)):

        return


    #create a Course object from the parsed Json file (aka the dict 'data')

    # if the page has been initialized, and a field is blank, Django spits out an exception.
    # to solve this, we set the fields to a string with a single space ' ' if the field is blank, and if it isn't blank, the value itself.
    # Also, will not save if duplicate
    if 'title' in data != '':

        # To search for W courses, if the cast to int fails, we cut off the last letter and try again
        try:
            num_to_enter= int(num)
        except:
            num_to_enter = int(num[:-1])

        course_data = Course(
            title=get_value("title"),
            code=dep.upper(),
            year=int(year),
            semester=semester.capitalize(),
            number_str=get_value("number"), # string number
            number=num_to_enter, # real number
            description=get_value("description"),
            prereqArray=identify_prereqs(get_value("prerequisites")),
            # prerequisites=get_value("prerequisites"), # this can't be done this way. Pre-reqs must be linked
            units=int(get_value('units')),
            signature=year + semester + get_value("title") + get_value("description") + get_value("number") + get_value("units")
        )
        
        course_data.save()                        # Need to figure out how to chekc if a course already exists 
        new_context = {'course_data':course_data} #This is the context for rendering to directions.html

    else:
        new_context = {'data':data}
    
    
    # print(course_data.title)   #debug 

    template = loader.get_template('sfu_academic_api_parser/manual_input.html')
    # context = {'courses':courses,}            # old context when directly scraping from API

    if url.status_code != 200: 
        # raise Http404("Cannot find course")
        return HttpResponseNotFound('<h1>Course not found</h1>')
    
    ## print(url.status_code) #debug
    ## print(url_raw)
    # return render(request, 'sfu_academic_api_parser/directions.html', context)    # previous return from when we directly scraped from API 
    return render(request, 'sfu_academic_api_parser/manual_input.html', new_context)
   


def directions(request):
    return render(request, 'sfu_academic_api_parser/directions.html')