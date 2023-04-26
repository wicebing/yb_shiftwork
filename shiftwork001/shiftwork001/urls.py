"""shiftwork001 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from app1 import views

# router = DefaultRouter()
# router.register('staff', views.staffViewset)
# router.register('regis', views.UserGenericViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/whoami/', views.get_current_user, name='get_current_user'),
    path('api/regist/', views.UserGenericView.as_view()),
    path('api/regist/<pk>/', views.UserDetailGenericView.as_view()),
    path('api/staff/', views.staffGenericView.as_view()),
    path('api/staff/<pk>/', views.staffDetailGenericView.as_view()),
    path('api/project/', views.projectGenericView.as_view()),
    path('api/project/<pk>/', views.projectDetailGenericView.as_view()),
    path('api/date/', views.dateGenericView.as_view()),
    path('api/date/<pk>/', views.dateDetailGenericView.as_view()),
    path('api/shift/', views.shiftGenericView.as_view()),
    path('api/shift/<pk>/', views.shiftDetailGenericView.as_view()),
    path('api/groupname/', views.groupnameGeneraicView.as_view()),
    path('api/groupname/<pk>/', views.groupnameDetailGenericView.as_view()),
    path('api/group/', views.groupGenericView.as_view()),
    path('api/group/<pk>/', views.groupDetailGenericView.as_view()),


    path('docs/', include_docs_urls(title='My API title')),
    path('token/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
