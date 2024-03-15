from django.contrib import admin
from first_app.models import Employee, Teachers
from first_app.models import Course

admin.site.register(Course)
admin.site.register(Employee)
admin.site.register(Teachers)
