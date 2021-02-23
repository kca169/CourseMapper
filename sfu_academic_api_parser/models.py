from django.db import models

class Course(models.Model):
    department = models.CharField(max_length=25)
    number = models.CharField(max_length=10)  ##This is not a IntegerField because some courses contain letters (ex. CMPT 105W)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.department + self.number 
