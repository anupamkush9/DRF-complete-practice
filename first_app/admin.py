from django.contrib import admin

# Register your models here.
from first_app.models import Employee, Teachers
# Register your models here.
admin.site.register(Employee)
admin.site.register(Teachers)
