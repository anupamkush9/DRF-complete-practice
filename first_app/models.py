from django.db import models

# Create your models here.
class Employee(models.Model):
    eno=models.IntegerField()
    ename=models.CharField(max_length=64)
    esal=models.FloatField()
    eaddr=models.CharField(max_length=64)

    def __str__(self):
        return self.ename
    
class Teachers(models.Model):
    teacher_name=models.CharField(max_length=64)
    teacher_sal=models.FloatField()
    teacher_addr=models.CharField(max_length=64)

    def __str__(self):
        return self.teacher_name
