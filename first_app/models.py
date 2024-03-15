from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=40)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    duration= models.FloatField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    ename = models.CharField(max_length=40)
    esal = models.FloatField(default=0)
    eaddr= models.CharField(max_length=400)

    def __str__(self):
        return self.ename

class Teachers(models.Model):
    teacher_name=models.CharField(max_length=64)
    teacher_sal=models.FloatField()
    teacher_addr=models.CharField(max_length=64)

    def __str__(self):
        return self.teacher_name

class Student(models.Model):
    name=models.CharField(max_length=50, blank=True, null=True)
    marks = models.IntegerField(default=0)
    email = models.EmailField(blank=True, null=True)