from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import Http404
from .models import CourseTree
from django.template import loader 
#from .forms import CourseForm
import requests
import json

#This function GET's from the provided url, turns the resuld into JSON then loads and renders directions.html

# Refs: [3], [4]

def treemode(request):
    result_list = list()
    # getting form data, convert all to lower-case as that is how the API serves the data.
    year = request.POST.get('year', '').lower()
    semester = request.POST.get('semester', '').lower()
    dep = request.POST.get('department', '').lower()
    num = request.POST.get('course_number', '').lower()
    

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
        if len(value)==0:
            value = 'empty'
            return value
        
        return value 
    
    # print(data) #debug

    #this function identify_prereqs() gets rid of the filler in prerequisites and returns only the prereq codes as a string
    def identify_prereqs(preq):
        coursecodes_list = ['CMPT', 'MATH', 'MACM', 'ENSC', 'CRIM', 'ECON',
        'ENGL', 'FREN', 'GSWS', 'LBST', 'LING', 'PHIL', 'POL', 'PSYC', 'SA', 
        'ACMA', 'BISC', 'BPK', 'CHEM', 'EASC', 'NUSC', 'PHYS', 'STAT', 'CA', 'CMNS', 'IAT', 
        'PUB', 'ARCH', 'ENV', 'GEOG', 'REM', 'EDUC', 'BEUC', 'BUS', 'COGS', 'HIST', 'HUM',
        'INDG', 'IS', 'WL', 'HSCI', 'DIAL']

        bad_chars = ['(', ')',',','.',':',';']
        result_list = list()
        prereq_list = list()
        index = 0
        HScourselist = ['Pre-Calculus', 'BC Math 12']
 
        if (preq == '') :      #if the prerequisites are an empty string
            result_list.append('empty')
            return result_list  #return empty result list

        if (preq == 'empty') :      #if the prerequisites are an empty string
            result_list.append('empty')
            return result_list  #return empty result list
             
        preq = ''.join(i for i in preq if not i in bad_chars)
        prereq_list = preq.split()

        for bad in HScourselist:
            if bad in preq:
                return result_list

        for words in prereq_list:
            if words in coursecodes_list:
                result_list.append(words + " " + prereq_list[index+1])
            index +=1

        index = 0        
        for i in range(len(prereq_list)-1):
            if 'and' in prereq_list[i]:
                #print("Index of 'and' is " + str(i) )
                if prereq_list[i+1].isdigit():
                    result_list.append(prereq_list[i-2] + " " + prereq_list[i+1])
        #print (result_list)
        if len(result_list)==0:
            result_list.append('empty')
        return result_list

    def recursive_list(prereq_list, result_list):

        if "empty" in prereq_list: #when the list of prereqs is empty
            return 

        for i in range(len(prereq_list)): # Moving through the array of courses
            print( i)
            temp_list = list() #creates empty list
            temp_list = prereq_list[i].split() #splits coursecode + number into 2 parts
            search_list = list() #creates a list of courses to search for recursively
            dep = temp_list[0].lower() #takes the lowercase course code
            num = temp_list[1].lower()  #takes the course num

            print('for course: ' + dep + num)    #THIS LINE is for debugging      
            #####
            url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year}/{semester}/courses/{dep}/{num}' # changed to formatted string
            url_raw = url
            url = requests.get(url)
            courses = url.json()
            courses_str = json.dumps(courses)   # Convert 'courses' to a JSON string 
            data = json.loads(courses_str)      # Convert to a Python dictionary

           
            if prereq_list[i] not in result_list: #checks if a course in the result list already exists, only appends if it does not exist
                result_list.append(prereq_list[i])

            temp_list=identify_prereqs(data["prerequisites"])

            for existingcourses in temp_list:
                if existingcourses not in result_list:
                    search_list.append(existingcourses)

            if (dep.upper()+' '+num.upper()) in search_list:
                search_list.remove(dep.upper()+' '+num.upper())

            print (search_list)       ##ANOTHER DEBUGGING LINE

            recursive_list((search_list), result_list)

        
        return result_list
        


    #create a Course object from the parsed Json file (aka the dict 'data')
    
    # if the page has been initialized, and a field is blank, Django spits out an exception.
    # to solve this, we set the fields to a string with a single space ' ' if the field is blank, and if it isn't blank, the value itself.

    if 'title' in data != '':

        course_data = CourseTree(
            name=get_value("title"),
            prerequisite=identify_prereqs(get_value("prerequisites")), # this can't be done this way. Pre-reqs must be linked
            prereqList=recursive_list(identify_prereqs(get_value("prerequisites")), result_list),
        )
        course_data.save()                        # Need to figure out how to chekc if a course already exists 
        new_context = {'course_data':course_data} #This is the context for rendering to directions.html

    else:
        new_context = {'data':data}

    
    # print(course_data.title)   #debug 

    template = loader.get_template('treemode/tree_diagram.html')
    # context = {'courses':courses,}            # old context when directly scraping from API

    if url.status_code != 200: 
        raise Http404("Cannot find course")
    
    ## print(url.status_code) #debug
    ## print(url_raw)
    # return render(request, 'sfu_academic_api_parser/directions.html', context)    # previous return from when we directly scraped from API 
    return render(request, 'treemode/tree_diagram.html', new_context)
   