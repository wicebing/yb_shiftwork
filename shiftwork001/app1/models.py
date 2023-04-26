from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class UserBaseInfo(models.Model):
#     id = models.AutoField(primary_key=True,verbose_name='ID')
#     username = models.CharField(max_length=20,verbose_name='用戶名')
#     password = models.CharField(max_length=20,verbose_name='密碼')
#     status = models.IntegerField(verbose_name='狀態',max_length=1)
#     createdate = models.DateTimeField(auto_now_add=True,verbose_name='創建時間',db_column='createDate')

#     def __str__(self):
#         return str(self.id)+self.username
#     class Meta:
#         managed = True
#         verbose_name = '人員基本信息'
#         db_table = 'UserBaseInfo4'

class Table_staff(models.Model):
    id = models.CharField(primary_key=True,max_length=8,verbose_name='ID')
    NTUHid = models.CharField(max_length=8,verbose_name='NTUH ID')
    name = models.CharField(max_length=100,verbose_name='姓名')
    birthday = models.DateField(verbose_name='生日')
    AUTHid = models.OneToOneField(User,on_delete=models.DO_NOTHING,verbose_name='人員', null=True)

    def __str__(self):
        return str(self.NTUHid)+self.name
    
class Table_groupname(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='群組名稱')
    priority = models.IntegerField(verbose_name='優先碼', default=0)
    turn = models.IntegerField(verbose_name='順序碼', default=0)
    def __str__(self):
        return str(self.id)+self.name
    
class Table_groups(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    groupname = models.ForeignKey(Table_groupname,on_delete=models.DO_NOTHING,verbose_name='群組名稱')
    staff = models.ForeignKey(Table_staff,on_delete=models.DO_NOTHING,verbose_name='人員')
    priority = models.IntegerField(verbose_name='優先碼', default=1)
    turn = models.IntegerField(verbose_name='順序碼', default=0)
    def __str__(self):
        return str(self.id)+self.groupname.name+self.staff.name

class Table_date(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    date = models.DateField(verbose_name='日期')
    def __str__(self):
        return str(self.id)+str(self.date)
    
class Table_shift(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='班別名稱')
    time = models.CharField(max_length=100,verbose_name='班別時間')
    charactor = models.CharField(max_length=1,verbose_name='白夜班')
    def __str__(self):
        return str(self.id)+self.name+self.time+self.charactor

class Table_project(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='專案名稱')
    status = models.BooleanField(verbose_name='狀態',default=False)
    def __str__(self):
        return str(self.id)+self.name+str(self.status)

class Table_Shift_Schedule(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    date = models.ForeignKey(Table_date,on_delete=models.DO_NOTHING,verbose_name='日期')
    shift = models.ForeignKey(Table_shift,on_delete=models.DO_NOTHING,verbose_name='班別')
    project = models.ForeignKey(Table_project,on_delete=models.DO_NOTHING,verbose_name='專案')
    staff = models.ForeignKey(Table_staff,on_delete=models.DO_NOTHING,verbose_name='人員',null=True)
    def __str__(self):
        return str(self.id)+self.date.date+self.shift.name+self.shift.time+self.staff.name
    
class Table_meeting(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    date = models.ForeignKey(Table_date,on_delete=models.DO_NOTHING,verbose_name='日期')
    time = models.CharField(max_length=100,verbose_name='時間')
    name = models.CharField(max_length=100,verbose_name='會議名稱')
    staff = models.ForeignKey(Table_staff,on_delete=models.CASCADE,verbose_name='人員')
    def __str__(self):
        return str(self.id)+self.date.date+self.staff.name

class Table_class(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    date = models.ForeignKey(Table_date,on_delete=models.DO_NOTHING,verbose_name='日期')
    time = models.CharField(max_length=100,verbose_name='時間')
    name = models.CharField(max_length=100,verbose_name='課程名稱')
    staff = models.ForeignKey(Table_staff,on_delete=models.CASCADE,verbose_name='人員')
    def __str__(self):
        return str(self.id)+self.date.date+self.staff.name
    
class Table_personal(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    date = models.ForeignKey(Table_date,on_delete=models.DO_NOTHING,verbose_name='日期')
    time = models.CharField(max_length=100,verbose_name='時間')
    name = models.CharField(max_length=100,verbose_name='事項名稱')
    staff = models.ForeignKey(Table_staff,on_delete=models.CASCADE,verbose_name='人員')
    def __str__(self):
        return str(self.id)+self.date.date++self.staff.name