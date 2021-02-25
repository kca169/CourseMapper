from django import forms

class CourseForm(forms.Form):
    department = forms.CharField(max_length=100)
    course_number = forms.CharField(max_length=100)
