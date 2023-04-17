from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import MyTokenObtainPairSerializer

from .form import *
from .serializers import *

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# def index(request):
#     myform = Form_staff()
#     return render(request, 'app1/index.html',{'form_obj':myform})

# def var(request):
#     lists = ['Java','Python','C','C#','JS']
#     dicts = {'name':'Tom','age':18, 'sex':'male'}
#     return render(request, 'app2/var.html', {'lists':lists, 'dicts':dicts})

# def user_login(request):
#     info = ''
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             info += '登入成功'
#         else:
#             info += '登入失敗'
#     return render(request, 'app1/index.html', {'info':info})

# def user_register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')

#         if User.objects.filter(username=username).exists():
#             info = '帳號已存在'
#             return render(request, 'app1/user_register.html', {'info':info})
#         else:
#             if User.objects.filter(email=email).exists():
#                 info = '信箱已存在'
#                 return render(request, 'app1/user_register.html', {'info':info})
#             else:
#                 user = User.objects.create_user(username=username, password=password, email=email)
#                 user.save()
#                 info= '註冊成功' 
#                 return render(request, 'app1/user_register.html', {'info':info})
#     return render(request, 'app1/user_register.html')

# class UserGenericView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = User_Serializer

# class staffView(APIView):
#     def get(self, request, *args, **kwargs):
#         staff = Table_staff.objects.all()
#         serializer = Table_staff_Serializer(staff, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = Table_staff_Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserGenericView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return []

class UserDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)


class staffGenericView(generics.ListCreateAPIView):
    queryset = Table_staff.objects.all()
    serializer_class = Table_staff_Serializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class staffDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_staff.objects.all()
    serializer_class = Table_staff_Serializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

