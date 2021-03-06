from django.db import models

# Refs: [8]

# Basic course model.
# Signature for this course MUST be generated after instantiation using the gen_signature() method!
class Course(models.Model):

    title = models.CharField(max_length = 100, default='This is an example title')
    description = models.CharField(max_length=1000, default="This is an example description")
    code = models.CharField(max_length=5, default="TEST") ## The (usually) four letter string that preceds the course number
    
    prerequisites_str = models.CharField(max_length=150, default="")
    prereqArray = models.CharField(max_length=1000, default = ["Ford", "Volvo", "BMW"])
    units = models.CharField(max_length=10, default="0")
    number = models.IntegerField(default = 123)
    year = models.IntegerField(default=2021)
    semester = models.CharField(max_length=15, default="New example")

    w_course = models.BooleanField(default=False)

    # Signature is all the str fields concatenated together. with it being set to unique, this prevents duplicates... hopefully.
    signature = models.CharField(max_length=1500, default="Change this.", unique=True)

    # prerequisites = models.CharField(max_length=1000, default = "This is an example of a prerequisite")
    prerequisites = models.ForeignKey('self', null=True, on_delete=models.CASCADE) # Find alterative to CASCADE
    
    # This solution is utter garbage, but it will have to do until I can find a better way.
    def gen_signature(self):
        return str(self.year) + self.semester + self.code + self.title + self.description + str(self.number) + str(self.units)
    
    def __str__(self):
        return str(self.code) + " " + str(self.number) + self.description
    
    pass

