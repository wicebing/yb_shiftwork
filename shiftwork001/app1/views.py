from datetime import datetime, timedelta

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, get_list_or_404

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
    queryset = Table_staff.objects.all().order_by('NTUHid')
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
 
class projectShiftScheduleGenericView(generics.ListCreateAPIView):
    queryset = Table_Shift_Schedule.objects.all()
    serializer_class = Table_Shift_Schedule_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    ordering_fields = ('date','shift')

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id', None)
        queryset = Table_Shift_Schedule.objects.all().order_by('date','shift' )

        if project_id is not None:
            project_instance = get_object_or_404(Table_project, id=project_id)
            queryset = queryset.filter(project=project_instance)

        return queryset

class projectShiftScheduleDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_Shift_Schedule.objects.all()
    serializer_class = Table_Shift_Schedule_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class projectShiftScheduleStatisticsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication, SessionAuthentication,)

    def get(self, request):
        project_id = request.query_params.get("project_id", None)
        queryset = Table_Shift_Schedule.objects.all().order_by("date", "shift")

        if project_id is not None:
            project_instance = get_object_or_404(Table_project, id=project_id)
            queryset = queryset.filter(project=project_instance)

        # Calculate the statistics for character, holiday, and name
        statistics = self.get_shift_schedule_statistics(queryset)

        return Response(statistics)

    def get_shift_schedule_statistics(self, queryset):
        total_count = queryset.count()
        # Get the value count for character
        character_count = queryset.values("shift__charactor__name").annotate(count=Count("shift__charactor__name")).order_by("shift__charactor__name")
        print(character_count)
        # Get the value count for holiday
        holiday_count = queryset.values("date__holiday").annotate(count=Count("date__holiday")).order_by("date__holiday")

        # Get the value count for name
        name_count = queryset.values("shift__name").annotate(count=Count("shift__name")).order_by("shift__name")

        intersection_counts = queryset.values("shift__charactor__name", "date__holiday",).annotate(count=Count("id")).order_by("shift__charactor__name", "date__holiday")

        # Combine the counts into a single dictionary
        statistics = {
            "total_count": total_count,
            "character_count": list(character_count),
            "holiday_count": list(holiday_count),
            "name_count": list(name_count),
            "intersection_counts": list(intersection_counts)
        }

        return statistics


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

    def create(self, request, *args, **kwargs):
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')

        if not start_date_str or not end_date_str:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if start_date > end_date:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        date_list = []
        current_date = start_date

        while current_date <= end_date:
            is_weekend = current_date.weekday() == 5 or current_date.weekday() == 6
            date_exists = Table_date.objects.filter(date=current_date).exists()
            
            if not date_exists:
                date_list.append(Table_date(date=current_date, holiday=is_weekend))

            current_date += timedelta(days=1)

        Table_date.objects.bulk_create(date_list)

        return Response(status=status.HTTP_201_CREATED)

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
    ordering_fields = ('id','name','charactor','time')
    search_fields = ('name','charactor','time',)

class shiftCharactorGenericView(generics.ListCreateAPIView):
    queryset = Table_shift_charactor.objects.all().order_by('name')
    serializer_class = Table_shift_charactor_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    ordering_fields = ('id','name')

class shiftCharactorDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_shift_charactor.objects.all()
    serializer_class = Table_shift_charactor_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

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
        groupname_name = self.request.query_params.get('groupname_name', None)

        queryset = Table_groups.objects.all().order_by('priority', 'turn')

        if groupname_id is not None:
            groupname_instance = get_object_or_404(Table_groupname, id=groupname_id)
            queryset = queryset.filter(groupname=groupname_instance)
        elif groupname_name is not None:
            groupname_instance = get_object_or_404(Table_groupname, name=groupname_name)
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

class extraGenericView(generics.ListCreateAPIView):
    queryset = Table_extra.objects.all()
    serializer_class = Table_extra_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    ordering_fields = ('id',)

class extraDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_extra.objects.all()
    serializer_class = Table_extra_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class staffExtraGenericView(generics.ListCreateAPIView):
    queryset = Table_staff_extra.objects.all()
    serializer_class = Table_staff_extra_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    ordering_fields = ('id',)

    def get_queryset(self):
        staff_id = self.request.query_params.get('staff_id', None)
        queryset = Table_staff_extra.objects.all().order_by('extra__id')

        if staff_id is not None:
            staff_instance = get_object_or_404(Table_staff, id=staff_id)
            queryset = queryset.filter(staff=staff_instance)

        return queryset

class staffExtraDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_staff_extra.objects.all()
    serializer_class = Table_staff_extra_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class staffRelaxGenericView(generics.ListCreateAPIView):
    queryset = Table_staff_relax.objects.all()
    serializer_class = Table_staff_relax_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    ordering_fields = ('id',)

    def get_queryset(self):
        staff_id = self.request.query_params.get('staff_id', None)
        queryset = Table_staff_relax.objects.all().order_by('relax__id')

        if staff_id is not None:
            staff_instance = get_object_or_404(Table_staff, id=staff_id)
            queryset = queryset.filter(staff=staff_instance)

        return queryset

class staffRelaxDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_staff_relax.objects.all()
    serializer_class = Table_staff_relax_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class relaxGenericView(generics.ListCreateAPIView):
    queryset = Table_relax.objects.all()
    serializer_class = Table_relax_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    ordering_fields = ('id',)

class relaxDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_relax.objects.all()
    serializer_class = Table_relax_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class ruleGenericView(generics.ListCreateAPIView):
    queryset = Table_rule.objects.all()
    serializer_class = Table_rule_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    ordering_fields = ('id',)

    def get_queryset(self):
        staffOnly = self.request.query_params.get('staffOnly', None)
        queryset = Table_rule.objects.all()

        if staffOnly is not None:
            if staffOnly.lower() == 'true':
                queryset = queryset.filter(staffOnly=True)
            elif staffOnly.lower() == 'false':
                queryset = queryset.filter(staffOnly=False)
        return queryset
    

class ruleDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_rule.objects.all()
    serializer_class = Table_rule_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

class projectAttendRuleGenericView(generics.ListCreateAPIView):
    queryset = Table_project_attend_rule.objects.all()
    serializer_class = Table_project_attend_rule_Serializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    # pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    ordering_fields = ('id',)

    def get_queryset(self):
        project_attend_id = self.request.query_params.get('project_attend', None)
        queryset = Table_project_attend_rule.objects.all()

        if project_attend_id is not None:
            project_attend_instance = get_object_or_404(Table_project_attend, id=project_attend_id)
            queryset = queryset.filter(project_attend=project_attend_instance)
        return queryset


class projectAttendRuleDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_project_attend_rule.objects.all()
    serializer_class = Table_project_attend_rule_Serializer
    permission_classes = (IsOwnerOrAdmin,permissions.IsAdminUser,)
    authentication_classes = (JWTAuthentication,SessionAuthentication,)

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

    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    ordering_fields = ('id',)

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





@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
def create_shift_schedules(request):
    start_date_str = request.data.get('start_date')
    end_date_str = request.data.get('end_date')
    shift_ids = request.data.get('shift_ids')
    project_id = request.data.get('project')

    if not start_date_str or not end_date_str or not shift_ids:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    dates = Table_date.objects.filter(date__range=(start_date, end_date))
    shifts = get_list_or_404(Table_shift, id__in=shift_ids)
    project = get_object_or_404(Table_project, id=project_id)

    shift_schedules_to_create = []

    for date in dates:
        for shift in shifts:
            # Check if the entry already exists
            entry_exists = Table_Shift_Schedule.objects.filter(date=date, shift=shift, project=project).exists()

            # If the entry does not exist, add it to the list of instances to be created
            if not entry_exists:
                shift_schedules_to_create.append(Table_Shift_Schedule(date=date, shift=shift, project=project))

    # Bulk create the new instances
    Table_Shift_Schedule.objects.bulk_create(shift_schedules_to_create)

    return Response(status=status.HTTP_201_CREATED)




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


