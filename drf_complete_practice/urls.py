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
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
# router=routers.DefaultRouter()
# router.register('api',views.EmployeeCRUDCBV)
urlpatterns = [
    path('admin/', admin.site.urls),
    # path("v/",include(router.urls)),
    path('hello/', views.HelloView.as_view(), name ='hello'),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
	path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
	path('api/token/verify/',jwt_views.TokenVerifyView.as_view(),name ='token_verify'),

]