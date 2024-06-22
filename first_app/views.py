import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Course
from .serializer import CourseSerializer, StudentSerializer, CourseNoRequiredSerializer, TeachersNoRequiredSerializer
from first_app.models import Employee, Teachers, Student
from rest_framework import generics
from first_app.serializer import TeachersSerializer, EmployeeSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, filters as django_filters_lib
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
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
SERVER_ERROR_MESSAGE = {"detail": "Something went wrong while processing your request"}

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

INTERNAL_SERVER_ERROR_RESPONSE_TYPE = openapi.Response(
    description='Internal Server Error', 
    schema=openapi.Schema(
        type='object', 
        properties={
            'errors': openapi.Schema(
                type='array', 
                items=openapi.Schema(
                    type='object',
                    properties={
                        'detail': openapi.Schema(type='string', description="Something went wrong while processing your request")
                    }
                )
            ),
            'data': openapi.Schema(
                type='null',
                description=None
            ),
            'success': openapi.Schema(
                type='boolean',
                description=None,
            )
        }
    )
)

API_DELETE_RESPONSE = openapi.Response(
    description='',
    schema=openapi.Schema(
        type='object',
        properties={
            'message': openapi.Schema(
                type='string',
                description="record deleted successfully {id}",
            ),
            'success': openapi.Schema(
                type='boolean',
                description="true/false",
            ),
            'data': openapi.Schema(
                type='string',
                description="null",
            ),
        }
    )
)

DETAILS_NOT_FOUND_RESPONSE = openapi.Response(
    description='',
    schema=openapi.Schema(
        type='object',
        properties={
            'detail': openapi.Schema(
                type='string',
                description="Not found",
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
    if request.method == 'GET':
        print("*******os.environ*******",os.environ)
        print("*******POSTGRES_DB*******",os.environ.get('POSTGRES_DB'))
        return Response({"message": "Hello, world!", "POSTGRES_DB":os.environ.get('POSTGRES_DB'), "all_env":os.environ,})

class HelloView(APIView):
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)

class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        # fields = ['name', 'marks']
        fields = {
            'name': ['exact', 'contains'],
            'marks': ['exact', 'gte'],
        }


# REF : https://www.django-rest-framework.org/api-guide/filtering/
# REF : https://www.django-rest-framework.org/api-guide/filtering/

class StudentViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication,BasicAuthentication]
    permission_classes=[IsAuthenticated,]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, django_filters_lib.SearchFilter, django_filters_lib.OrderingFilter]
    # filterset_fields = ['name', 'marks', 'email']
    filterset_class = StudentFilter
    search_fields = ['name', 'marks', 'email', 'id']
    ordering_fields = ['name', 'marks', 'email', 'id']
    ordering = ['id']

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
                    responses={401 : UNAUTHORIZED_RESPONSE_TYPE,200: CourseNoRequiredSerializer(many=True), 400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE})
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=CourseSerializer,
                    # in this api, response body was generated automatically still we have overridden responses for our custom implmentation
                    responses={401 : UNAUTHORIZED_RESPONSE_TYPE, 200: CourseNoRequiredSerializer,  400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE},
                     )

@api_view(['GET' , 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def courseListView(request):
    if request.method == 'GET':
        try:
            id = request.GET["id"] if "id" in request.GET and request.GET["id"] is not None and request.GET['id'] != "" else None
            rid = request.GET["rid"] if "rid" in request.GET and request.GET["rid"] is not None and request.GET['rid'] != "" else None
            if id:
                return Response({"success":True, "success_message":"Record found", "pagination":None, "data":f'custom response for id {id} parameter'}, status=status.HTTP_200_OK)
            if rid:
                return Response({"success":True, "success_message":"Record found", "pagination":None, "data":f'custom response for rid {rid} parameter'}, status=status.HTTP_200_OK)
            limit = None
            try:
                limit = int(request.GET["limit"])
            except Exception as e:
                pass
            search_term = request.GET.get("search_term", "")
            if limit and limit < 0:
                return Response({"data":[], "filters":None, "success_message":"", "errors":[{"detail": "Limit value should be greater than Zero"}], "success":False, "pagination":None})
            offset, limit, page, page_size, order = getLimitOffset(request, "desc", 10)
            print("offset, limit, page, page_size, order",offset, limit, page, page_size, order)
            if order.lower() == "asc": 
                query_order = "id" 
            else:
                query_order = "-id"  
            courses_queryset = Course.objects.all().order_by(query_order)
            if search_term is not None and search_term.strip() != "":
                try:
                    search_value = int(search_term)
                    search_filter = Q(price=search_value) | Q(id=search_value)
                except:
                    search_filter = Q(name__icontains=search_term) | Q(author__icontains=search_term)
                courses_queryset = courses_queryset.filter(search_filter)
            if not courses_queryset:
                # here nothing will display on swagger because we have used status code status = status.HTTP_204_NO_CONTENT
                return Response({"filters":None, "success":True, "success_message":"No record found", "errors":[], "pagination":None, "data":None,}, status=status.HTTP_204_NO_CONTENT)
            total_records = len(courses_queryset) 

            courses_queryset = courses_queryset[offset:limit]
            count = len(courses_queryset) 
        
            if page_size > 0: 
                total_pages = math.ceil(total_records/page_size) 
            else: 
                total_pages = 1 
            pagination = {"total_records" : total_records, "count" : count, "page_size" : page_size, "total_pages" : total_pages, "current_page" : page, "order" : order}        
            course_serialize_data = CourseSerializer(courses_queryset , many=True).data 
            return Response({"success":True, "success_message":"Record found", "pagination":pagination, "data":course_serialize_data}, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    elif request.method == 'POST':
        try:
            courseSerializer = CourseSerializer(data = request.data)
            if courseSerializer.is_valid():
                courseSerializer.save()
                return Response(courseSerializer.data , status=status.HTTP_201_CREATED)
            return Response(courseSerializer.errors)
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='get', responses={200: CourseSerializer(), 404:DETAILS_NOT_FOUND_RESPONSE, 400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE})
@swagger_auto_schema(method='put', responses={200: CourseSerializer(), 401 : UNAUTHORIZED_RESPONSE_TYPE, 404:DETAILS_NOT_FOUND_RESPONSE, 400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE})
@swagger_auto_schema(method='delete', responses={200: API_DELETE_RESPONSE, 404:DETAILS_NOT_FOUND_RESPONSE, 400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE})
@api_view(['GET' , 'PUT' , 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def courseDetailView(request , pk):

    # get_object_or_404 is the recommended method
    # below one is error more error prune.
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        try:
            courseSerializer = CourseSerializer(course) 
            return Response(courseSerializer.data)
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        try:
            courseSerializer = CourseSerializer(course , data = request.data)
            if courseSerializer.is_valid():
                courseSerializer.save()
                return Response(courseSerializer.data)
            return Response(courseSerializer.errors)
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        try:
            course.delete()
            return Response({"message":f"record deleted successfully {pk}", "success":True, "data":None})
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    authentication_classes=[TokenAuthentication,BasicAuthentication]
    permission_classes=[IsAuthenticated,]
    # In Swagger (OpenAPI), a tag is used to group related API endpoints together, enhancing the organization and readability of the API documentation.
    @swagger_auto_schema(
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
                    responses={401 : UNAUTHORIZED_RESPONSE_TYPE, 200: TeachersSerializer(many=True), 400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE},
                    tags=['Teachers API'],
                    )
    def get(self, request):
        try:
            id = request.GET["id"] if "id" in request.GET and request.GET["id"] is not None and request.GET['id'] != "" else None
            rid = request.GET["rid"] if "rid" in request.GET and request.GET["rid"] is not None and request.GET['rid'] != "" else None
            if id:
                return Response({"success":True, "success_message":"Record found", "pagination":None, "data":f'custom response for id {id} parameter'}, status=status.HTTP_200_OK)
            if rid:
                return Response({"success":True, "success_message":"Record found", "pagination":None, "data":f'custom response for rid {rid} parameter'}, status=status.HTTP_200_OK)
            limit = None
            try:
                limit = int(request.GET["limit"])
            except Exception as e:
                pass
            search_term = request.GET.get("search_term", "")
            if limit and limit < 0:
                return Response({"data":[], "filters":None, "success_message":"", "errors":[{"detail": "Limit value should be greater than Zero"}], "success":False, "pagination":None})
            offset, limit, page, page_size, order = getLimitOffset(request, "desc", 10)
            print("offset, limit, page, page_size, order",offset, limit, page, page_size, order)
            if order.lower() == "asc": 
                query_order = "id" 
            else:
                query_order = "-id"  
            teachers_queryset = Teachers.objects.all().order_by(query_order)
            if search_term is not None and search_term.strip() != "":
                try:
                    search_value = float(search_term)
                    search_filter = Q(teacher_sal=search_value) 
                except:
                    search_filter = Q(teacher_name__icontains=search_term) | Q(teacher_addr__icontains=search_term)
                teachers_queryset = teachers_queryset.filter(search_filter)
            if not teachers_queryset:
                # here nothing will display on swagger because we have used status code status = status.HTTP_204_NO_CONTENT
                return Response({"filters":None, "success":True, "success_message":"No record found", "errors":[], "pagination":None, "data":None,}, status=status.HTTP_204_NO_CONTENT)
            total_records = len(teachers_queryset) 

            teachers_queryset = teachers_queryset[offset:limit]
            count = len(teachers_queryset) 
        
            if page_size > 0: 
                total_pages = math.ceil(total_records/page_size) 
            else: 
                total_pages = 1 
            pagination = {"total_records" : total_records, "count" : count, "page_size" : page_size, "total_pages" : total_pages, "current_page" : page, "order" : order}        
            teachers_serialize_data = TeachersSerializer(teachers_queryset , many=True).data 
            return Response({"success":True, "success_message":"Record found", "pagination":pagination, "data":teachers_serialize_data}, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # In Swagger (OpenAPI), a tag is used to group related API endpoints together, enhancing the organization and readability of the API documentation.
    @swagger_auto_schema(request_body=TeachersSerializer,
                    # in this api, response body was generated automatically still we have overridden responses for our custom implmentation
                    responses={401 : UNAUTHORIZED_RESPONSE_TYPE, 200: TeachersSerializer,  400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE},
                    tags=['Teachers API'],
                     )
    def post(self,request):
        try:
            serializer=TeachersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data, 'status':200})
            return Response(serializer.errors,status=400)
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TeachersDetailApiView(APIView):
    authentication_classes=[TokenAuthentication, BasicAuthentication]
    permission_classes=[IsAuthenticated,]
    @swagger_auto_schema(responses={200:  openapi.Response(
                            description="OK",
                            schema=TeachersNoRequiredSerializer()
                        ), 404:DETAILS_NOT_FOUND_RESPONSE, 401 : UNAUTHORIZED_RESPONSE_TYPE, 400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE})
    def get(self, request, pk=None):
        try:
            teacher = get_object_or_404(Teachers.objects.all(), pk=pk)
            serializer = TeachersSerializer(teacher)
            return Response({"data":serializer.data, "status":200})
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=TeachersSerializer,
                    # in this api, response body was generated automatically still we have overridden responses for our custom implmentation
                    responses={401 : UNAUTHORIZED_RESPONSE_TYPE, 200:  openapi.Response(
                    description="OK",
                    schema=TeachersNoRequiredSerializer()
                ),  400: 'Bad Request', 404:DETAILS_NOT_FOUND_RESPONSE, 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE})
    def put(self,request,pk=None):
        try:
            teacher = get_object_or_404(Teachers.objects.all(), pk=pk)
            serializer = TeachersSerializer(teacher, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(responses={200: API_DELETE_RESPONSE, 404:DETAILS_NOT_FOUND_RESPONSE, 401 : UNAUTHORIZED_RESPONSE_TYPE, 400: 'Bad Request', 500:INTERNAL_SERVER_ERROR_RESPONSE_TYPE})
    def delete(self, request, pk=None, format=None) -> Response:
        """ For deleting a post, HTTP method: DELETE """
        try:
            teacher = get_object_or_404(Teachers.objects.all(), pk=pk)
            teacher.delete()
            return Response({"message":f"record deleted successfully {pk}", "success":True, "data":None})
        except Exception as e:
            return Response({"errors":[SERVER_ERROR_MESSAGE], "data":None, "success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
