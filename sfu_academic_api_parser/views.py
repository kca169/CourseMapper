from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import Http404, HttpResponseNotFound
from .models import Course
from django.template import loader 

#from .forms import CourseForm
import requests
import json

# Refs: [3], [4], [10]

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
   
def automatic_parser(request):

    ''' REFERENCE:
    >>> print(url_dict[0]['value'])
    2013
    >>> print(url_dict[1]['value'])
    2014
    >>> print(url_dict[2]['value'])
    2015
    '''
    # getting user input
    max_year = request.POST.get('max_year', '')
    min_year = request.POST.get('min_year', '')
    button_pressed = True if request.POST.get('Submit') == 'Submit' else False

    # get all years from API
    years_url = "http://www.sfu.ca/bin/wcm/academic-calendar"
    years_url = requests.get(years_url) # sending GET request
    years_json = years_url.json() # intepret as JSON file
    years_str = json.dumps(years_json)   # Convert 'years_raw' to a JSON string 
    years_dict = json.loads(years_str)      # Convert to a Python dictionary
    years_all = [] # declare list that will be filled by for-loop below

    # converting all years to integers and appending them to the years_all list
    for x in range(len(years_dict)):
        years_all.append(int(years_dict[x]['value']))
    
    years_to_search = [] # declaring list that shall be a subset of all years, which shall be searched

    # If there is input and the button has been pressed, then get all years that are within the range selected.
    if max_year != '' and min_year != '' and button_pressed == True:
        
        max_year_int = int(max_year) # converting inputs to integers
        min_year_int = int(min_year)

        # filter out years within range
        for x in years_all:
            if years_all[x] >= min_year_int and years_all[x] <= max_year_int:
                years_to_search.append(years_all[x])

    # else if the button has been pressed but no input, just get the current (maximum) year
    elif button_pressed == True:
        # get maximum year
        years_to_search.append(years_all[-1])
    
    # else, do nothing.

    # This is where the fun begins.
    # Loop 0 - Search all years
    if button_pressed == False:
        return render(request, 'sfu_academic_api_parser/automatic_input.html')


    for x in range(len(years_to_search)):
        year_str = str(years_to_search[x]) # convert current year to string
        
        print(years_to_search[x])

        # get all semesters for that year from API
        semester_url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year_str}' # construct URL
        semester_url = requests.get(semester_url) # send GET request
        semester_json = semester_url.json() # interpret as JSON file
        semester_str = json.dumps(semester_json) # convert to JSON string
        semester_dic = json.loads(semester_str) # convert to list of dictionaries
        semester_list = [] # declare list for the filtered out semester data

        # filter semesters
        # this may be updated with an IF statement if we implement semester-by-semester selection
        for i in range(len(semester_dic)):
            semester_list.append(semester_dic[i]['value'])
        
        # Loop 1 - search within semesters for departments (course codes)
        for i in range(len(semester_list)):
            departments_url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year_str}/{semester_list[i]}/courses' # construct URL
            departments_url = requests.get(departments_url) # send GET request
            departments_json = departments_url.json() # convert to json file
            departments_str = json.dumps(departments_json) # save as string
            departments_dic = json.loads(departments_str) # save as list of dictionaries
            departments_list = [] # declare list of all departments
            
            # copying all departments to list
            for k in range(len(departments_dic)):
                departments_list.append(departments_dic[k]['value'])
            
            print(semester_list[i]) # debug
            
            # Loop 2 - getting course numbers in department
            for k in range(len(departments_list)):
                course_n_url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year_str}/{semester_list[i]}/courses/{departments_list[k]}' # construct URL
                course_n_url = requests.get(course_n_url) # send GET request
                course_n_json = course_n_url.json() # convert to json file
                course_n_str = json.dumps(course_n_json) # save as string
                course_n_dic = json.loads(course_n_str) # save as list of dictionaries
                course_n_list = [] # declare list of all departments

                print(departments_list[k]) # debug

                # Copying course numbers
                for course_n_counter in range(len(course_n_dic)):
                    course_n_list.append(course_n_dic[course_n_counter]['value'])
                
                # Loop 3 - saving courses into database
                for course_n_counter in range(len(course_n_list)):
                    course_url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year_str}/{semester_list[i]}/courses/{departments_list[k]}/{course_n_list[course_n_counter]}' # construct URL
                    course_url = requests.get(course_url) # send GET request
                    course_json = course_url.json() # convert to json file
                    course_str = json.dumps(course_json) # save as string
                    course_dic = json.loads(course_str) # save as list of dictionaries
                    
                    w_course = False

                    print(course_n_list[course_n_counter])

                    # Sanitize number for chars
                    number_sanitized = int()
                    try:
                        number_sanitized = int(course_dic['number'])
                    except:
                        # checking for w course
                        if course_dic['number'][-1] == "w":
                            number_sanitized = int(course_dic['number'][-1])
                            w_course = True
                        else:
                            print("Parser: Unexpected number!")
                    
                    # creating object

                    try: 
                        new_course = Course.objects.create(
                            code=departments_list[k],
                            title=course_dic['title'],
                            description=course_dic['description'],
                            prerequisites_str=course_dic['prerequisites'],
                            number=number_sanitized,
                            units=course_dic['units'],
                            year=years_to_search[x],
                            semester=semester_list[i],
                            w_course=w_course
                        )
                        # generating signature
                        new_course.signature = new_course.gen_signature()
                        new_course.save()
                    except:
                        print("Course Already added!")
                    
                    

                    # done!
    return render(request, 'sfu_academic_api_parser/automatic_input.html')


def directions(request):
    return render(request, 'sfu_academic_api_parser/directions.html')