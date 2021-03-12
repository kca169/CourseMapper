from django.db import models

# Refs: [8]

# Basic course model.
class CourseTree(models.Model):

    name = models.CharField(max_length = 50, default='This is an example title')
    prerequisite = models.CharField(max_length=1000, default = "This is an example of a prerequisite")
    prereqList = models.CharField(max_length=1000, default = ["Ford", "Volvo", "BMW"])
    def __str__(self):
        return self.number_str + self.description
    
    pass
