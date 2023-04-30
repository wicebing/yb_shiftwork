from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

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
from .permissions import IsOwnerOrAdmin

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
    permission_classes = (IsOwnerOrAdmin, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class staffGenericView(generics.ListCreateAPIView):
    queryset = Table_staff.objects.all()
    serializer_class = Table_staff_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('NTUHid','name')
    ordering_fields = ('NTUHid','name')

class staffDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_staff.objects.all()
    serializer_class = Table_staff_Serializer
    permission_classes = (IsOwnerOrAdmin,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class projectGenericView(generics.ListCreateAPIView):
    queryset = Table_project.objects.all()
    serializer_class = Table_project_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('status',)
    ordering_fields = ('name','status')

    def get_queryset(self):
        queryset = Table_project.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            if status.lower() == 'true':
                queryset = queryset.filter(status=True)
            elif status.lower() == 'false':
                queryset = queryset.filter(status=False)
        return queryset

class projectDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_project.objects.all()
    serializer_class = Table_project_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class dateGenericView(generics.ListCreateAPIView):
    queryset = Table_date.objects.all()
    serializer_class = Table_date_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('date',)
    ordering_fields = ('date',)
    search_fields = ('date',)

class dateDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_date.objects.all()
    serializer_class = Table_date_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class shiftGenericView(generics.ListCreateAPIView):
    queryset = Table_shift.objects.all()
    serializer_class = Table_shift_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('charactor','name',)
    ordering_fields = ('name','charactor','time')
    search_fields = ('name','charactor','time',)

class shiftDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_shift.objects.all()
    serializer_class = Table_shift_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class groupnameGeneraicView(generics.ListCreateAPIView):
    queryset = Table_groupname.objects.all()
    serializer_class = Table_groupname_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('name','priority')
    ordering_fields = ('turn','priority')
    search_fields = ('name',)

    queryset = Table_groupname.objects.all().order_by('priority', 'turn')

class groupnameDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_groupname.objects.all()
    serializer_class = Table_groupname_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class groupGenericView(generics.ListCreateAPIView):
    queryset = Table_groups.objects.all()
    serializer_class = Table_groups_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ()
    ordering_fields = ('turn','priority')
    search_fields = ('staff',)
    queryset = Table_groups.objects.all().order_by('priority', 'turn')

    def get_queryset(self):
        groupname_id = self.request.query_params.get('groupname_id', None)
        queryset = Table_groups.objects.all().order_by('priority', 'turn')

        if groupname_id is not None:
            groupname_instance = get_object_or_404(Table_groupname, id=groupname_id)
            queryset = queryset.filter(groupname=groupname_instance)

        return queryset

class groupDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_groups.objects.all()
    serializer_class = Table_groups_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

    def get_largest_turn_with_priority_1(self, groupname):
        largest_turn = Table_groups.objects.filter(groupname=groupname, priority=1).order_by('-turn').first()
        return 1+largest_turn.turn if largest_turn else 0

    def perform_destroy(self, instance):
        groupname = instance.groupname
        instance.delete()
        groupname.mod = self.get_largest_turn_with_priority_1(groupname)
        groupname.save()

class projectAttendGenericView(generics.ListCreateAPIView):
    queryset = Table_project_attend.objects.all()
    serializer_class = Table_project_attend_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('project',)
    ordering_fields = ('sequence',)
    search_fields = ('project',)

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id', None)
        queryset = Table_project_attend.objects.all().order_by('sequence', )

        if project_id is not None:
            project_instance = get_object_or_404(Table_project, id=project_id)
            queryset = queryset.filter(project=project_instance)

        return queryset


class projectAttendDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_project_attend.objects.all()
    serializer_class = Table_project_attend_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

    def perform_destroy(self, instance):
        project = instance.project
        instance.delete()
        attend_count = Table_project_attend.objects.filter(project=project, groupname__priority=9).count()
        project.mod = attend_count
        project.save()







class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
# @permission_classes([IsStaff])
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


