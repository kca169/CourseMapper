from django.test import TestCase
from .models import Course
import json
import requests

# Refs: [9]

# Create course from REST API
# class Create_Courses(TestCase):

# Model tests
# Tests that duplicate courses cannot be added
class UniquenessTestCase(TestCase):
    
    def test_initialize(self):
        """ Create test course object """
        test_1 = Course.objects.create(
            title="Test Course",
            description="This is a test course for CourseMapper.",
            semester="Spring",
            code="TEST",
            number=101,
            units=3)
        # generate signature for test_1
        test_1.signature = test_1.gen_signature()

         # ensure that the signature is expected.        
        self.assertEquals(str(test_1.signature), str(test_1.year) + test_1.semester + test_1.code + test_1.title + test_1.description + str(test_1.number) + str(test_1.units), True)

        # save object into database
        test_1.save()

    def test_copy(self):
        """ tries to create a duplicate course"""
        test_1 = Course.objects.create(
            title="Test Course",
            description="This is a test course for CourseMapper.",
            semester="Spring",
            code="TEST",
            number=101,
            units=3
        )

        test_1.signature = test_1.gen_signature()
        # Save original
        test_1.save()
        
        # create identical course
        test_2 = Course.objects.create (
            title="Test Course",
            description="This is a test course for CourseMapper.",
            semester="Spring",
            code="TEST",
            number=101,
            units=3
        )
        # Generate signature
        test_2.signature = test_2.gen_signature()

        # Test to make sure an exception is raised when a duplicate is saved.
        with self.assertRaises(Exception):
            test_2.save() 

class rest_api_test(TestCase):
    

    def test_init(self):
        ''' Testing inserting courses into the REST API, and then cross referencing them after. We pull from CMPT and PHYS, for Spring 2021, up to 200 level courses'''
        # Initial values
        departments = ['cmpt', 'phys']
        semesters = ['spring']
        year = 2020
        upper_bound = 200

        for dep in departments:
            for sem in semesters:
                for num in range(100, upper_bound):
                    
                    url = f'http://www.sfu.ca/bin/wcm/academic-calendar?{year}/{sem}/courses/{dep}/{num}'
                    url = requests.get(url)
                    courses = url.json()
                    courses_str = json.dumps(courses)   # Convert 'courses' to a JSON string 
                    data = json.loads(courses_str)      # Convert to a Python dictionary

                    if url.status_code == 200:
                        course_data = Course(
                            title=data["title"],
                            code=dep.upper(),
                            year=int(year),
                            semester=sem.capitalize(),
                            number=int(data["number"]), # real number
                            description=data["description"],
                            units=int(data["units"]),
                        )
                        # debug
                        course_data.signature = course_data.gen_signature()
                        course_data.save()
                        
                        # Cross referencing
                        self.assertEquals(course_data.title, data["title"])
                        self.assertEquals(course_data.code, dep.upper())
                        self.assertEquals(course_data.year, int(year))
                        self.assertEquals(course_data.semester, sem.capitalize())
                        self.assertEquals(course_data.number, int(data["number"]))
                    
                    print(dep.upper() + " " + str(num) + " -- " + str(url.status_code))









