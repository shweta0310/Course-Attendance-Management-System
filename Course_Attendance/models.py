# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

CHOICES = [('P', 'Present'), ('A','Absent')]


class CourseAttendance(models.Model):
    ca_id = models.AutoField(primary_key=True)
    cid = models.ForeignKey('CourseInfo', db_column='cid', blank=True, null=True, on_delete=models.CASCADE)
    sid = models.ForeignKey('StudentInfo', db_column='sid', blank=True, null=True, on_delete=models.CASCADE)
    class_date = models.DateField()
    attendance = models.CharField(max_length=3, choices=CHOICES)
    classes_attended = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Course_Attendance'


class CourseInfo(models.Model):
    cid = models.CharField(primary_key=True, max_length=5, validators=[
        RegexValidator(
            regex=r'[A-Z]{2}[0-9]{3}',
            message='ID should be of form e.g CS100',
            code='invalid_studentID'
        ),
    ])
    cname = models.CharField(max_length=15)
    no_of_classes = models.IntegerField(validators=[MaxValueValidator(40), MinValueValidator(1)])
    course_plan = models.FileField(upload_to='media/', null=True, verbose_name="")
    fid = models.ForeignKey('FacultyInfo', db_column='fid', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Course_Info'


class CourseRegistration(models.Model):
    cr_id = models.AutoField(primary_key=True)
    cid = models.ForeignKey(CourseInfo, db_column='cid', blank=True, null=True, on_delete=models.CASCADE)
    sid = models.ForeignKey('StudentInfo', db_column='sid', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Course_Registration'


class FacultyInfo(models.Model):
    fid = models.CharField(primary_key=True, max_length=8, validators=[
        RegexValidator(
            regex=r'F[0-9]{2}[A-Z]{2}[0-9]{3}',
            message='ID should be of form e.g f19CO101',
            code='invalid_studentID'
        ),
    ])
    fname = models.CharField(max_length=20)
    femail = models.CharField(max_length=30)
    fcontact = models.CharField(max_length=10, validators=[RegexValidator(regex='^[0-9]{10}$'), ])
    fdept = models.CharField(max_length=35)
    finterests = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Faculty_Info'


class StudentInfo(models.Model):
    sid = models.CharField(primary_key=True, max_length=7, validators=[
        RegexValidator(
            regex=r'[0-9]{2}[A-Z]{2}[0-9]{3}',
            message='ID should be of form e.g 19CO101',
            code='invalid_studentID'
        ),
    ])
    sname = models.CharField(max_length=20)
    semail = models.CharField(max_length=30)
    scontact = models.CharField(max_length=10, validators=[
        RegexValidator(
            regex=r'[0-9]{10}',
            message='Contact number should be of 10 digits',
            code='invalid_studentID'
        ),
    ])
    sdept = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'Student_Info'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
