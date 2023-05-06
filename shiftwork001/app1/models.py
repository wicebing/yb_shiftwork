from django.db import models, transaction
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
    mod = models.IntegerField(verbose_name='同餘', default=0)
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
    id = models.AutoField(primary_key=True, verbose_name='ID')
    date = models.DateField(verbose_name='日期')
    holiday = models.BooleanField(verbose_name='假日', default=False)

    def __str__(self):
        return str(self.id) + str(self.date)

    def save(self, *args, **kwargs):
        # Check if the object is new (id is None)
        if self.id is None:
            # Check if the date is a weekend (Saturday or Sunday)
            if self.date.weekday() == 5 or self.date.weekday() == 6:
                self.holiday = True

        super().save(*args, **kwargs)

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
    turn = models.IntegerField(verbose_name='順序碼', default=0)
    mod = models.IntegerField(verbose_name='同餘', default=0)
    status = models.BooleanField(verbose_name='狀態',default=False)
    def __str__(self):
        return str(self.id)+self.name+str(self.status)

    def save(self, *args, **kwargs):
        # Check if the 'turn' attribute has been changed
        if self.pk is not None:
            # old_turn = Table_project.objects.get(pk=self.pk).turn
            # if old_turn != self.turn:
                super().save(*args, **kwargs)  # Save the updated 'turn' value
                self.update_related_sequences()  # Update related sequences
            # else:
            #     super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def update_related_sequences(self):
        with transaction.atomic():
            # Get all related 'Table_project_attend' instances
            related_project_attends = Table_project_attend.objects.filter(project=self)

            for project_attend in related_project_attends:
                # Update the 'sequence' value
                project_attend.sequence = project_attend.calculate_sequence(self, project_attend.groupname)
                project_attend.save()


class Table_project_attend(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    project = models.ForeignKey(Table_project,on_delete=models.DO_NOTHING,verbose_name='專案')
    groupname = models.ForeignKey(Table_groupname,on_delete=models.DO_NOTHING,verbose_name='群組名稱')
    constraint = models.CharField(max_length=100,verbose_name='限制代碼', null=True)
    sequence = models.IntegerField(verbose_name='順序碼', default=0)
    def __str__(self):
        return str(self.id)

    def calculate_sequence(self, project, groupname):
        priority = groupname.priority
        project_turn = project.turn
        groupname_turn = groupname.turn
        project_mod = project.mod

        if project_mod == 0:
            sequence = priority * 100 + ((groupname_turn - project_turn) % (project_mod + 1))
        else:
            sequence = priority * 100 + ((groupname_turn - project_turn) % (project_mod))
        return sequence

class Table_rule(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='規則名稱')
    description = models.CharField(max_length=1000,verbose_name='規則描述')
    def __str__(self):
        return str(self.id)+self.name+self.description
    
class Table_project_attend_rule(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    project_attend = models.ForeignKey(Table_project_attend,on_delete=models.DO_NOTHING,verbose_name='專案群組')
    rule = models.ForeignKey(Table_rule,on_delete=models.DO_NOTHING,verbose_name='規則')
    def __str__(self):
        return str(self.id)

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