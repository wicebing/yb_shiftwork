from rest_framework import serializers
from django.contrib.auth.models import User
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
    class Meta:
        model = Table_groups
        fields = '__all__'

class Table_groupname_Serializer(serializers.ModelSerializer):
    groups = Table_groups_Serializer(source='table_groups_set',many=True, read_only=True)
    class Meta:
        model = Table_groupname
        fields = ['id','name','priority', 'turn','groups']
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token