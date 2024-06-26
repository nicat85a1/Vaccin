from django.db import models
from center.models import Vaccine
from center.models import Center
from django.contrib.auth import get_user_model

User = get_user_model()

class Campagin(models.Model):
    center = models.ForeignKey(Center,on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine,on_delete=models.CASCADE)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    agents = models.ManyToManyField(User)

    def __str__(self):
        return self.center.name + " | " + self.vaccine.name
    
class Slot(models.Model):
    campagin = models.ForeignKey(Campagin, on_delete=models.CASCADE)
    date =models.DateField(null=True, blank=True)
    start_time =models.TimeField(null=True,blank=True)
    end_time =models.TimeField(null=True,blank=True)
    max_capacity = models.IntegerField(default=0,null=True,blank=True)
    reserved = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.date) + " | " +str(self.start_time) + "to" + str(self.end_time)