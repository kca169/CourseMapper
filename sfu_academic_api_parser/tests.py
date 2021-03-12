from django.test import TestCase

from sfu_academic_api_parser.models import Course
from sfu_academic_api_parser.views import manual_input
from sfu_academic_api_parser.views import search
# Refs: [9]

# View tests
class Create_Courses(TestCase):
     print("Hello world!") # Placeholder


# Model tests
# Tests that duplicate courses cannot be added
class Test_Uniqueness(TestCase):

    def initialize_test(self):
        # Create object
        Course.objects.create()
