from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance by checking if the id is None
        is_new_instance = self.id is None

        # Call the original save method
        super().save(*args, **kwargs)

        if is_new_instance:
            # If this is a new instance, create a Table_staff_extra instance for every Table_staff
            for extra in Table_extra.objects.all():
                staff_extra, created = Table_staff_extra.objects.get_or_create(staff=self, extra=extra)
                if not created:
                    # If the entry already exists, raise a ValidationError
                    raise ValidationError(f"Staff {self.id} and extra {extra.id} are already associated.")
            for relax in Table_relax.objects.all():
                staff_relax, created = Table_staff_relax.objects.get_or_create(staff=self, relax=relax)
                if not created:
                    # If the entry already exists, raise a ValidationError
                    raise ValidationError(f"Staff {self.id} and relax {relax.id} are already associated.")
    
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
    charactor = models.CharField(max_length=5,verbose_name='白夜班')
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

class Table_extra(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='超排名稱')
    description = models.CharField(max_length=1000,verbose_name='超排描述')
    staff_extra = models.ManyToManyField('Table_staff',through='Table_staff_extra',through_fields=('extra','staff'))
    def __str__(self):
        return str(self.id)+self.name+self.description
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance by checking if the id is None
        is_new_instance = self.id is None

        # Call the original save method
        super().save(*args, **kwargs)

        if is_new_instance:
            # If this is a new instance, create a Table_staff_extra instance for every Table_staff
            for staff in Table_staff.objects.all():
                staff_extra, created = Table_staff_extra.objects.get_or_create(staff=staff, extra=self)
                if not created:
                    # If the entry already exists, raise a ValidationError
                    raise ValidationError(f"Staff {staff.id} and extra {self.id} are already associated.")
    
class Table_staff_extra(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    staff = models.ForeignKey(Table_staff,on_delete=models.CASCADE,verbose_name='人員')
    extra = models.ForeignKey(Table_extra,on_delete=models.CASCADE,verbose_name='超排')
    credit = models.IntegerField(verbose_name='超排分數',default=0)

    class Meta:
        unique_together = ('staff', 'extra')

    def __str__(self):
        return str(self.id)
    
class Table_relax(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='減班名稱')
    description = models.CharField(max_length=1000,verbose_name='減班描述')
    staff_relax = models.ManyToManyField('Table_staff',through='Table_staff_relax',through_fields=('relax','staff'))

    def __str__(self):
        return str(self.id)+self.name+self.description
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance by checking if the id is None
        is_new_instance = self.id is None

        # Call the original save method
        super().save(*args, **kwargs)

        if is_new_instance:
            # If this is a new instance, create a Table_staff_relax instance for every Table_staff
            for staff in Table_staff.objects.all():
                staff_relax, created = Table_staff_relax.objects.get_or_create(staff=staff, relax=self)
                if not created:
                    # If the entry already exists, raise a ValidationError
                    raise ValidationError(f"Staff {staff.id} and relax {self.id} are already associated.")

class Table_staff_relax(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    staff = models.ForeignKey(Table_staff,on_delete=models.CASCADE,verbose_name='人員')
    relax = models.ForeignKey(Table_relax,on_delete=models.CASCADE,verbose_name='減班')
    credit = models.IntegerField(verbose_name='減班分數',default=0)

    class Meta:
        unique_together = ('staff', 'relax')

    def __str__(self):
        return str(self.id)

class Table_rule(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='規則名稱')
    description = models.CharField(max_length=1000,verbose_name='規則描述')
    valueOfRule = models.CharField(max_length=100,verbose_name='規則值',null=True)
    staffOnly = models.BooleanField(verbose_name='因人而異規則',default=False)
    specialGroup = models.BooleanField(verbose_name='特殊編組規則',default=False)
    def __str__(self):
        return str(self.id)+self.name+self.description
    
class Table_project_attend_rule(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='ID')
    project_attend = models.ForeignKey(Table_project_attend,on_delete=models.CASCADE,verbose_name='專案群組')
    rule = models.ForeignKey(Table_rule,on_delete=models.CASCADE,verbose_name='規則')
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