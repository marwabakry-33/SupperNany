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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=190, null=True)
    last_name = models.CharField(max_length=190, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.first_name


# ✅ بعد كده: تعريف Child
class Child(models.Model):
   
    mother = models.ForeignKey(Mother, on_delete=models.CASCADE, related_name='children', null=True)
    baby = models.CharField(max_length=190, null=True) 
    feedings = models.CharField(max_length=190, null=True) 
    sleeping = models.CharField(max_length=190, null=True) 
    Diapers = models.CharField(max_length=190, null=True)
    weight = models.FloatField(null=False, default=0.0)
    height = models.FloatField(null=False, default=0.0)
    photo = models.ImageField(blank=True, null=True, default="super.png")

    def __str__(self):
        return self.baby

class preChild(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    mother = models.ForeignKey(
        'Mother',
        on_delete=models.CASCADE,
        related_name='pre_children',
        null=False
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=False)
    birth_date = models.DateField(null=False)

   
# Task
class Task(models.Model):
    child = models.ForeignKey(preChild, on_delete=models.CASCADE, related_name='tasks')
    content = models.TextField(null=True)



# HowTo
class HowTo(models.Model):
    content = models.TextField(null=True)
    def __str__(self): return self.content
    
# GrowthRecord
class GrowthRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='growth_records', default=1)
    weight = models.FloatField(null=False, default=0.0)
    height = models.FloatField(null=False, default=0.0)
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Growth record for {self.child} on {self.datetime}"

#أولاً: نحتاج مكان نحفظ فيه الكود
class PasswordResetCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.code}'
