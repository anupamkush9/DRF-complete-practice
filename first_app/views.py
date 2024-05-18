from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Course
from .serializer import CourseSerializer, StudentSerializer
from first_app.models import Employee, Teachers, Student
from rest_framework import generics
from first_app.serializer import TeachersSerializer, EmployeeSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from .utility import getLimitOffset
import math


test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)

UNAUTHORIZED_RESPONSE_TYPE = openapi.Response(
    description='Unauthorized',
    schema=openapi.Schema(
        type='object',
        properties={
            'detail': openapi.Schema(
                type='string',
                description='Authentication credentials were not provided'
            )
        }
    )
)

PAGINATION_LIST = [
    openapi.Parameter(
        name='limit',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_NUMBER,
        description='',
        required=False,
    ),
    openapi.Parameter(
        name='page',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_NUMBER,
        description='Enter page number',
        required=False,
    ),
    openapi.Parameter(
        name='page_size',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_NUMBER,
        description='Enter page size',
        required=False,
    ),
    openapi.Parameter(
        name='order',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='Enter the order of the list. (asc or desc)',
        required=False,
    ),
]


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})

class HelloView(APIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)


class StudentViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication,]
    permission_classes=[IsAuthenticated,]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# 'method' can be used to customize a single HTTP method of a view
@swagger_auto_schema(method='get',
                     manual_parameters = [ 
                        openapi.Parameter(
                            name='id',
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_NUMBER,
                            description='Enter ID',
                            required=False,
                        ),
                        openapi.Parameter(
                            name='rid',
                            in_=openapi.IN_QUERY,
                            type=openapi.TYPE_NUMBER,
                            description='Enter RID',
                            required=False,
                        ),
                    ] + PAGINATION_LIST, 
                    responses={200: "ok"})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=CourseSerializer,
                    # in this api, response body was generated automatically still we have overridden responses for our custom implmentation
                    responses={401 : UNAUTHORIZED_RESPONSE_TYPE, 200: CourseSerializer,  400: 'Bad Request'},
                     )

@api_view(['GET' , 'POST'])
def courseListView(request):
    if request.method == 'GET':
        id = request.GET["id"] if "id" in request.GET and request.GET["id"] is not None and request.GET['id'] != "" else None
        rid = request.GET["rid"] if "rid" in request.GET and request.GET["rid"] is not None and request.GET['rid'] != "" else None
        if id:
            return Response({"success":True, "success_message":"Record found", "pagination":None, "data":f'custom response for id {id} parameter'}, status=status.HTTP_200_OK)
        if rid:
            return Response({"success":True, "success_message":"Record found", "pagination":None, "data":f'custom response for rid {rid} parameter'}, status=status.HTTP_200_OK)
        
        offset, limit, page, page_size, order = getLimitOffset(request)
        print("offset, limit, page, page_size, order",offset, limit, page, page_size, order)
        if order.lower() == "asc": 
            query_order = "id" 
        else:
            query_order = "-id"  
        courses_queryset = Course.objects.all().order_by(query_order)
        if not courses_queryset:
            # here nothing will display on swagger because we have used status code status = status.HTTP_204_NO_CONTENT
            return Response({"filters":None, "success":True, "success_message":"No record found", "errors":[], "pagination":None, "data":None,}, status=status.HTTP_204_NO_CONTENT)
        total_records = len(courses_queryset) 

        courses_queryset = courses_queryset[offset:limit]
        count = len(courses_queryset) 
        if total_records == count or page == 0: 
            page = 1 
    
        if page_size == 0: 
            page_size = total_records 
        
        if page_size > 0: 
            total_pages = math.ceil(total_records/page_size) 
        else: 
            total_pages = 1 
        pagination = {"total_records" : total_records, "count" : count, "page_size" : page_size, "total_pages" : total_pages, "current_page" : page, "order" : order}        
        course_serialize_data = CourseSerializer(courses_queryset , many=True).data 
        return Response({"success":True, "success_message":"Record found", "pagination":pagination, "data":course_serialize_data}, status=status.HTTP_200_OK)


    elif request.method == 'POST':
        courseSerializer = CourseSerializer(data = request.data)
        if courseSerializer.is_valid():
            courseSerializer.save()
            return Response(courseSerializer.data , status=status.HTTP_201_CREATED)
        
        return Response(courseSerializer.errors)
@swagger_auto_schema(method='get', responses={200: CourseSerializer()})
@swagger_auto_schema(method='put', responses={200: CourseSerializer()})
@api_view(['GET' , 'PUT' , 'DELETE'])
def courseDetailView(request , pk):

    # get_object_or_404 is the recommended method
    # below one is error more error prune.
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
        return Response({"message":f"record deleted successfully {pk}"})

class EmployeeAPIView(generics.ListAPIView):
    # queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer

    def get_queryset(self):
        qs=Employee.objects.all()
        name=self.request.GET.get('ename')
        if name is not None:
            qs=qs.filter(ename__icontains=name)
        return qs

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


class ExampleView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted in class based APIView'
        }
        return Response(content)

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted in function based api_view'
    }
    return Response(content)
