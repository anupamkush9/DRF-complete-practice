from django.shortcuts import render
from first_app.serializer import EmployeeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from first_app.models import Employee, Teachers
from rest_framework import generics
from first_app.serializer import TeachersSerializer
from rest_framework.generics import get_object_or_404

class EmployeeAPIView(generics.ListAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

class TeachersApiView(APIView):
    def get(self, request):
            queryset = Teachers.objects.all()
            serializer = TeachersSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self,request):
        serializer=TeachersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'status':200})
        return Response(serializer.errors,status=400)

class TeachersDetailApiView(APIView):

    def get(self, request, pk=None):
        teacher = get_object_or_404(Teachers.objects.all(), pk=pk)
        serializer = TeachersSerializer(teacher)
        return Response({"data":serializer.data, "status":200})

    def put(self,request,pk=None):
        teacher = get_object_or_404(Teachers.objects.all(), pk=pk)
        serializer = TeachersSerializer(teacher, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk=None, format=None) -> Response:
        """ For deleting a post, HTTP method: DELETE """
        teacher = get_object_or_404(Teachers.objects.all(), pk=pk)
        teacher.delete()
        return Response({"status":200})