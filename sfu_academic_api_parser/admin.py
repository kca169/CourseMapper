from django.contrib import admin
from .models import Course

#class CourseAdmin(admin.ModelAdmin):
#    fields = ['

admin.site.register(Course)