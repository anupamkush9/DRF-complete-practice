from django.shortcuts import render
from first_app.serializer import EmployeeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from first_app.models import Employee
# Create your views here.
class EmployeeListAPIView(APIView):
    def get(self,request,format=None):
        qs=Employee.objects.all()
        serializer=EmployeeSerializer(qs,many=True)
        return Response(serializer.data)