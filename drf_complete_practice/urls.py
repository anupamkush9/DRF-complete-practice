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
router=routers.DefaultRouter()
router.register('test-viewset',views.TestViewSet,basename='test-viewset')
urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^api/', views.TestApiView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('',include(router.urls))
]