from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

# النصائح
class AdviceBaby(models.Model):
    advice_baby = models.CharField(max_length=200 ,null=True)
    def __str__(self): return self.advice_baby

class AdviceMoon(models.Model):
    advice_baby = models.CharField(max_length=200 ,null=True)
    def __str__(self): return self.advice_baby

class AdviceBottel(models.Model):
    advice_baby = models.CharField(max_length=200 ,null=True)
    def __str__(self): return self.advice_baby

class AdviceBad(models.Model):
    advice_bad = models.CharField(max_length=200 ,null=True)
    def __str__(self): return self.advice_bad

class AdviceMother(models.Model):
    advice_mather = models.CharField(max_length=200 ,null=True)
    def __str__(self): return self.advice_mather

# تعريف نموذج Mother بدون حقل user
class Mother(models.Model):
    first_name = models.CharField(max_length=190, null=True)
    last_name = models.CharField(max_length=190, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.first_name


# ✅ بعد كده: تعريف Child
class Child(models.Model):
    Type = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    mother = models.ForeignKey(Mother, on_delete=models.CASCADE, related_name='children', null=True)
    baby = models.CharField(max_length=190, null=True) 
    birth_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=200, null=True, choices=Type)
    feedings = models.CharField(max_length=190, null=True) 
    sleeping = models.CharField(max_length=190, null=True) 
    Diapers = models.CharField(max_length=190, null=True)
    weight = models.FloatField(null=False, default=0.0)
    height = models.FloatField(null=False, default=0.0)
    photo = models.ImageField(blank=True, null=True, default="super.png")

    def __str__(self):
        return self.baby

# Task
class Task(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='tasks', default=1)
    datetime = models.DateTimeField(default=datetime.now)
    content = models.TextField(null=True)
    def __str__(self): return f"Task for {self.child} on {self.datetime}"

# HowTo
class HowTo(models.Model):
    content = models.TextField(null=True)
    datetime = models.DateTimeField(default=datetime.now)
    advice_moon = models.ForeignKey(AdviceMother, on_delete=models.SET_NULL, null=True, blank=True, related_name='howto_moon')
    advice_bottle = models.ForeignKey(AdviceBaby, on_delete=models.SET_NULL, null=True, blank=True, related_name='howto_bottle')
    advice_bad = models.ForeignKey(AdviceBad, on_delete=models.SET_NULL, null=True, blank=True, related_name='howto_bad')
    advice_mother = models.ForeignKey(AdviceMother, on_delete=models.SET_NULL, null=True, blank=True, related_name='howto_mother')

    def __str__(self):
        return f"HowTo: {self.content[:30] if self.content else 'No content available'}..."

# GrowthRecord
class GrowthRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='growth_records', default=1)
    weight = models.FloatField(null=False, default=0.0)
    height = models.FloatField(null=False, default=0.0)
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Growth record for {self.child} on {self.datetime}"
