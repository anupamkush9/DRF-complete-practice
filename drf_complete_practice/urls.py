"""drf_complete_practice path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path('', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.paths import include, path
    2. Add a path to pathpatterns:  path('blog/', include('blog.paths'))
"""
from django.contrib import admin
from django.urls import path, include
from first_app import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register('students',views.StudentViewSet)

# from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', views.hello_world, name ='hello')
    path('courses', views.courseListView),
    path('courses/<int:pk>', views.courseDetailView),
    path('teachersapiview/', views.TeachersApiView.as_view()),
    path('teachersdetailsapiview/<int:pk>', views.TeachersDetailApiView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', views.EmployeeAPIView.as_view()),
    path('hello/', views.HelloView.as_view(), name ='hello'),
    path('hello_world/', views.hello_world, name ='hello_world'),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
	path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
	path('api/token/verify/',jwt_views.TokenVerifyView.as_view(),name ='token_verify'),
    path('',include(router.urls)),
    path('ex/',views.example_view),
    path('example/',views.ExampleView.as_view())
]