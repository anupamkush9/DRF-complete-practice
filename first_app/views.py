from django.shortcuts import render
from first_app.serializer import EmployeeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from first_app.models import Employee
# Create your views here.
from rest_framework import generics

class EmployeeAPIView(generics.ListAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
