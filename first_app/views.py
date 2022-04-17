
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class HelloView(APIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)


#  from django.shortcuts import render
# from first_app.models import Employee
# from first_app.serializer import EmployeeSerializer
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

# class EmployeeCRUDCBV(ModelViewSet):
#     authentication_classes=[TokenAuthentication,]
#     permission_classes=[AllowAny,]
#     serializer_class=EmployeeSerializer
#     queryset=Employee.objects.all()

# from rest_framework import mixins
# from rest_framework import generics

# from first_app.models import Employee
# from first_app.serializer import EmployeeSerializer

# class EmployeeListModelMixin(mixins.CreateModelMixin,mixins.ListModelMixin,
#                             generics.GenericAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
# class EmployeeDetailAPIViewMixin(mixins.UpdateModelMixin,mixins.DestroyModelMixin,
#                                 generics.GenericAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
#     def patch(self,request,*args,**kwargs):
#         return self.partial_update(request,*args,**kwargs)
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)


# from django.shortcuts import render
# from first_app.serializer import EmployeeSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from first_app.models import Employee
# # Create your views here.

# class EmployeeCreateAPIView(generics.CreateAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer

# class EmployeeUpdateAPIView(generics.UpdateAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer
#     lookup_field='id'
# class EmployeeDetailAPIView(generics.RetrieveAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer

# class EmployeeDeleteAPIView(generics.DestroyAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer
#     lookup_field='id'
# # class EmployeeAPIView(generics.ListAPIView):
# #     # queryset=Employee.objects.all()
# #     serializer_class=EmployeeSerializer

# #     def get_queryset(self):
# #         qs=Employee.objects.all()
# #         name=self.request.GET.get('ename')
# #         if name is not None:
# #             qs=qs.filter(ename__icontains=name)
# #         return qs



# class EmployeeAPIView(generics.ListAPIView):
#     queryset=Employee.objects.all()
#     serializer_class=EmployeeSerializer