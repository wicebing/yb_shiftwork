from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import F, ExpressionWrapper, IntegerField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'id','username', 'email', 'password','is_staff','is_superuser')
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("帳號已存在")
        return value
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("信箱已存在")
        return value
    # def validate_mobile(self, value):
    #     if User.objects.filter(mobile=value).exists():
    #         raise serializers.ValidationError("手機已存在")
    #     REGEX_MOBILE = "^09\d{8}$"
    #     if not re.match(REGEX_MOBILE, value):
    #         raise serializers.ValidationError("手機格式錯誤")
    #     return value
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)
    
    # username=serializers.CharField(required=True, allow_blank=False, max_length=20,
    #                                error_messages={
    #                                    'required': '請輸入帳號',
    #                                    'blank': '帳號不能為空',
    #                                    'max_length': '帳號不能超過20個字',
    #                                    }) 

class Table_groups_Serializer(serializers.ModelSerializer):
    # groupname = serializers.StringRelatedField()
    staff_name = serializers.StringRelatedField(source='staff.name', read_only=True)

    def get_largest_turn_with_priority_1(self, groupname):
        largest_turn = Table_groups.objects.filter(groupname=groupname, priority=1).order_by('-turn').first()
        return 1+largest_turn.turn if largest_turn else 0

    class Meta:
        model = Table_groups
        fields = '__all__'
        extra_fields = ['staff_name']

    def create(self, validated_data):
        instance = super().create(validated_data)
        groupname = instance.groupname
        groupname.mod = self.get_largest_turn_with_priority_1(groupname)
        groupname.save()
        return instance

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        groupname = updated_instance.groupname
        groupname.mod = self.get_largest_turn_with_priority_1(groupname)
        groupname.save()
        return updated_instance

class Table_groupname_Serializer(serializers.ModelSerializer):
    groups = Table_groups_Serializer(source='table_groups_set',many=True, read_only=True)
    class Meta:
        model = Table_groupname
        fields = ['id','name','priority','turn','mod','groups']
    def validate_name(self, value):
        if Table_groupname.objects.filter(name=value).exists():
            raise serializers.ValidationError("名稱已存在")
        return value
    def validate(self, attrs):
        turn = attrs.get('turn', None)
        priority = attrs.get('priority', None)

        if turn is not None and priority is not None:
            if Table_groupname.objects.filter(turn=turn, priority=priority).exists():
                raise serializers.ValidationError({"turn": "The combination of turn and priority already exists."})

        return attrs
    
class Table_staff_Serializer(serializers.ModelSerializer):
    # AUTHid = User_Serializer()
    groups = Table_groups_Serializer(source='table_groups_set',many=True, read_only=True)

    class Meta:
        model = Table_staff
        fields = ['id', 'NTUHid', 'name', 'birthday', 'AUTHid', 'groups']
    
    def validate_NTUHid(self, value):
        if Table_staff.objects.filter(NTUHid=value).exists():
            raise serializers.ValidationError("帳號已存在")
        return value
    
class Table_date_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_date
        fields = '__all__'
    def validate_name(self, value):
        if Table_date.objects.filter(date=value).exists():
            raise serializers.ValidationError("日期已存在")
        return value
    
class Table_shift_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_shift
        fields = '__all__'
    def validate_name(self, value):
        if Table_shift.objects.filter(name=value).exists():
            raise serializers.ValidationError("班種名稱已存在")
        return value

class Table_project_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_project
        fields = '__all__'
    def validate_name(self, value):
        if Table_project.objects.filter(name=value).exists():
            raise serializers.ValidationError("專案名稱已存在")
        return value

class Table_project_attend_Serializer(serializers.ModelSerializer):
    groupname_name = serializers.StringRelatedField(source='groupname.name', read_only=True)
    group_members = serializers.SerializerMethodField()

    class Meta:
        model = Table_project_attend
        fields = '__all__' 
        extra_fields = ['groupname_name', 'group_members']

    # def get_group_members(self, obj):
    #     group_members = Table_staff.objects.filter(table_groups__groupname=obj.groupname)
    #     return Table_staff_Serializer(group_members, many=True).data
    
    def get_group_members(self, obj):
        project = obj.project
        K = project.turn

        # Annotate the queryset with the calculated value
        group_members = Table_groups.objects.filter(
            groupname=obj.groupname
        ).annotate(
            order_value=ExpressionWrapper(
                100 * F('priority') + ((F('turn') + K) % F('groupname__mod')),
                output_field=IntegerField()
            )
        ).order_by('order_value')  # Order the queryset using the annotated value

        # Serialize the queryset
        return Table_groups_Serializer(group_members, many=True).data
 
    # def calculate_sequence(self, project, groupname):
    #     priority = groupname.priority
    #     project_turn = project.turn
    #     groupname_turn = groupname.turn
    #     project_mod = project.mod

    #     if project_mod == 0:
    #         sequence = priority * 100 + ((groupname_turn + project_turn) % (1))
    #     else:
    #         sequence = priority * 100 + ((groupname_turn + project_turn) % (project_mod))
    #     return sequence

    def update_project_mod(self, project):
        total_data_count = Table_project_attend.objects.filter(project=project, groupname__priority=9).count()
        project.mod = total_data_count
        project.save()

    def create(self, validated_data):
        project = validated_data['project']
        # groupname = validated_data['groupname']

        # validated_data['sequence'] = self.calculate_sequence(project, groupname)
        instance = super().create(validated_data)
        self.update_project_mod(project)

        return instance








class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token