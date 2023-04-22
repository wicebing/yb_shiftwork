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

class Table_staff_Serializer(serializers.ModelSerializer):
    # AUTHid = User_Serializer()
    class Meta:
        model = Table_staff
        fields = '__all__'
    
    def validate_NTUHid(self, value):
        if Table_staff.objects.filter(NTUHid=value).exists():
            raise serializers.ValidationError("帳號已存在")
        return value

class Table_groupname_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_groupname
        fields = '__all__'

class Table_groups_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_groups
        fields = '__all__'

class Table_date_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_date
        fields = '__all__'
    
class Table_shift_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_shift
        fields = '__all__'
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token