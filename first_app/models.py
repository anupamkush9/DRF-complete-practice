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
    
class Teachers(models.Model):
    teacher_name=models.CharField(max_length=64)
    teacher_sal=models.FloatField()
    teacher_addr=models.CharField(max_length=64)

    def __str__(self):
        return self.teacher_name
