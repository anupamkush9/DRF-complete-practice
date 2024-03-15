from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Course
from .serializer import CourseSerializer
from first_app.models import Employee, Teachers
from rest_framework import generics
from first_app.serializer import TeachersSerializer, EmployeeSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

@api_view(['GET' , 'POST'])
def courseListView(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        courseSerializer = CourseSerializer(courses , many=True)
        return Response(courseSerializer.data)

    elif request.method == 'POST':
        courseSerializer = CourseSerializer(data = request.data)
        if courseSerializer.is_valid():
            courseSerializer.save()
            return Response(courseSerializer.data , status=status.HTTP_201_CREATED)
        
        return Response(courseSerializer.errors)


@api_view(['GET' , 'PUT' , 'DELETE'])
def courseDetailView(request , pk):

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        courseSerializer = CourseSerializer(course) 
        return Response(courseSerializer.data)

    elif request.method == 'PUT':
        courseSerializer = CourseSerializer(course , data = request.data)
        if courseSerializer.is_valid():
            courseSerializer.save()
            return Response(courseSerializer.data)
        return Response(courseSerializer.errors)

    elif request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
