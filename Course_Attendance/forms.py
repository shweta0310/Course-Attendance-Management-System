from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from .models import StudentInfo, CourseInfo, FacultyInfo

user_instance = get_user_model()


class StudentSignupForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": ""}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": ""}))
    sid = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Eg. 17CS001"}))
    scontact = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "10 digts"}))
    semail = forms.EmailField(widget=forms.EmailInput(attrs={'size': 70}))
    sdept = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))
    sname = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))

    class Meta:
        model = StudentInfo
        fields = ('sid', 'sname', 'semail', 'scontact', 'sdept', 'password', 'confirm_password')


class StudentProfileForm(forms.ModelForm):
    scontact = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "10 digts"}))
    semail = forms.EmailField(widget=forms.EmailInput(attrs={'size': 70}))
    sdept = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))
    sname = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))

    class Meta:
        model = StudentInfo
        fields = ('sname', 'semail', 'scontact', 'sdept')


class FacultySignupForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": ""}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": ""}))
    fid = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Eg. F17CS001"}))
    fcontact = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "10 digts"}))
    femail = forms.EmailField(widget=forms.EmailInput(attrs={'size': 70}))
    fdept = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))
    fname = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))
    finterests = forms.CharField(widget=forms.TextInput(attrs={'size': 100}))

    class Meta:
        model = FacultyInfo
        fields = ('fid', 'fname', 'femail', 'fcontact', 'fdept', 'finterests', 'password', 'confirm_password')


class FacultyProfileForm(forms.ModelForm):
    fcontact = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "10 digts"}))
    femail = forms.EmailField(widget=forms.EmailInput(attrs={'size': 70}))
    fdept = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))
    fname = forms.CharField(widget=forms.TextInput(attrs={'size': 70}))
    finterests = forms.CharField(widget=forms.TextInput(attrs={'size': 100}))

    class Meta:
        model = FacultyInfo
        fields = ('fname', 'femail', 'fcontact', 'fdept', 'finterests')


validator = RegexValidator(r"[A-Z]{2}[0-9]{3}", "Invalid Input")


class CourseIDForm(forms.Form):

    cid = forms.CharField(required=True, min_length=5, max_length=5, strip=True,
                          validators=[validator])


class CourseForm(forms.Form):

    cid = forms.CharField(required=True, min_length=5, max_length=5, strip=True,
                          validators=[validator], widget=forms.TextInput(attrs={"placeholder": "Eg. CS123"}))
    no_of_classes = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"placeholder": "(1 to 40)"}))
    cname = forms.CharField(required=True, max_length=15, widget=forms.TextInput(attrs={'size': 25}))
    course_plan = forms.FileField()


class CourseEditForm(forms.ModelForm):
    cname = forms.CharField(widget=forms.TextInput(attrs={'size': 25}))
    no_of_classes = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "(1 to 40)"}))

    class Meta:
        model = CourseInfo
        fields = ('cname', 'no_of_classes')


class DateInput(forms.DateInput):
    input_type = 'date'


class AttendanceForm(forms.Form):

    date_input = forms.DateField(required=True, widget=DateInput)


class CourseAttendanceForm(forms.Form):

    attendance = forms.CharField(required=True, max_length=2)