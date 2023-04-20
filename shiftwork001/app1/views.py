from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .common.permissions import IsStaff
from .serializers import MyTokenObtainPairSerializer
from .form import *
from .serializers import *
from .mypage import MyPageNumberPagination

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class UserGenericView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('is_staff')
    ordering_fields = ('NTUHid','name')
    search_fields = ('is_staff')
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return []
    
    def get_queryset(self):
        queryset = User.objects.all()
        is_staff = self.request.query_params.get('is_staff', None)
        if is_staff is not None:
            if is_staff.lower() == 'true':
                queryset = queryset.filter(is_staff=True)
            elif is_staff.lower() == 'false':
                queryset = queryset.filter(is_staff=False)
        return queryset

class UserDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)


class staffGenericView(generics.ListCreateAPIView):
    queryset = Table_staff.objects.all()
    serializer_class = Table_staff_Serializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('NTUHid','name')
    ordering_fields = ('NTUHid','name')

class staffDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_staff.objects.all()
    serializer_class = Table_staff_Serializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsStaff])
@authentication_classes([JWTAuthentication,SessionAuthentication])
def get_current_user(request):
    user = request.user
    print(request.user.id,request.user.username,request.user.email)

    try:
        table_staff = user.table_staff
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'table_staff': {
                'id': table_staff.id,
                'NTUHid': table_staff.NTUHid,
                'name': table_staff.name,
                'birthday': table_staff.birthday
            }
        }, status=status.HTTP_200_OK)
    except:
        table_staff = None
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'table_staff': table_staff
        }, status=status.HTTP_200_OK)


