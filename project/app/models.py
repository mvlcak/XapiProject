from django.db import models
from django.utils import timezone
import datetime


class Person(models.Model):
    id_lms=models.CharField(max_length=200)
    person_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.person_name
    

class Activity(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    actor = models.CharField(max_length=200)
    verb = models.CharField(max_length=200)
    object = models.CharField(max_length=600)   
    pub_date = models.DateTimeField('date published')
    timestamp =models.CharField(max_length=200)
    id_activity =models.CharField(max_length=200)

    def __str__(self):
        return self.actor +" "+self.verb+" "+self.object
        
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)    
