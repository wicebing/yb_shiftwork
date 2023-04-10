from django import forms
from django.forms import ModelForm
from .models import Table_staff,Table_groupname,Table_groups,Table_date,Table_shift,Table_project
from .models import Table_Shift_Schedule,Table_meeting,Table_class

class Form_staff(ModelForm):
    class Meta:
        model = Table_staff
        fields = '__all__' 
        labels = {
            'name':'姓名',
            'email':'電子郵件',
            'phone':'電話',
            'status':'狀態',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'name':{
                'required':'姓名不可為空',
            },
            'email':{
                'required':'電子郵件不可為空',
            },
            'phone':{
                'required':'電話不可為空',
            },
            'status':{
                'required':'狀態不可為空',
            }, 
        }


class Form_groupname(ModelForm):
    class Meta:
        model = Table_groupname
        fields = '__all__' 
        labels = {
            'name':'群組名稱',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'name':{
                'required':'群組名稱不可為空', 
            },
        }

class Form_groups(ModelForm):
    class Meta:
        model = Table_groups
        fields = '__all__' 
        labels = {
            'groupname':'群組名稱',
            'staff':'人員',
            'turn':'順序碼',
        }

class Form_date(ModelForm):
    class Meta:
        model = Table_date
        fields = '__all__' 
        labels = {
            'date':'日期',
        }

class Form_shift(ModelForm):
    class Meta:
        model = Table_shift
        fields = '__all__' 
        labels = {
            'name':'班別名稱',
            'time':'班別時間',
            'charactor':'白夜班',
        }

class Form_project(ModelForm):
    class Meta:
        model = Table_project
        fields = '__all__' 
        labels = {
            'name':'專案名稱',
            'date':'日期',
            'shift':'班別',
            'group':'群組',
            'staff':'人員',
            'status':'狀態',
        }   