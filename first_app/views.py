from django.shortcuts import render
from first_app.serializer import NameSerializer

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
class TestApiView(APIView):
    def get(self,request,format=None):
        colors=['RED','BLUE','GREEN','YELLOW','INDIGO']
        return Response({'msg':'Welcome to Colorful Year','colors':colors})

    def post(self,request):
        serializer=NameSerializer(data=request.data)
        if serializer.is_valid():
            name=serializer.data.get('name')
            msg='Hello {} Wish You Happy New Year !!!'.format(name)
            return Response({'msg':msg})
        return Response(serializer.errors,status=400)

    def put(self,request,pk=None):
        return Response({'msg':'Response from put method'})

    def patch(self,request,pk=None):
        return Response({'msg':'Response from patch method'})

    def delete(self,request,pk=None):
        return Response({'msg':'Response from delete method'})