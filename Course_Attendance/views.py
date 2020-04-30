import os

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from django.urls import reverse
import datetime

from reportlab.pdfgen import canvas

from .forms import StudentSignupForm, StudentProfileForm, CourseIDForm, AttendanceForm, CourseAttendanceForm, \
    FacultyProfileForm, CourseForm, FacultySignupForm
from .models import StudentInfo, CourseRegistration, CourseAttendance, CourseInfo, FacultyInfo


def index(request):
    return render(request, 'Course_Attendance/index.html')


def archive(request):
    course_instance = CourseInfo.objects.all()
    len_courses = len(course_instance)

    print(course_instance)
    course_rows = {}
    i = 0
    while i < len_courses:
        temp = []
        print('i=' + str(i))
        j = 0
        while j < 3:
            print('j=' + str(j))
            if i + j < len_courses:
                temp.append(course_instance[i + j])
            j += 1

        course_rows[i] = temp
        i += 3
    print(course_rows)
    return render(request, 'Course_Attendance/archive.html', {'course_rows': course_rows,
                                                              'len_courses': len_courses})


def course_detail(request, course_id):
    course_instance = CourseInfo.objects.get(cid=course_id)
    print(course_instance)
    try:
        filename = course_instance.course_plan
        filename1 = filename.decode('utf-8')
        print(filename1)
        dir = '/home/shweta/PycharmProjects/Course_Attendance_Management_Project/CourseAttendance_ManagementProject/media/'
        filepath = dir + filename1
        print(filepath)
        return FileResponse(open(filepath,'rb'), content_type='application/pdf')
    except:
        template = 'Course_Attendance/archive.html'
        error_message = 'Course Plan of this course cannot be viewed.'
        return render(request, template, {'error_message': error_message})


def login_student(request):
    template = 'Course_Attendance/login_student.html'
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # get user id
            user_id = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate user
            user = authenticate(username=user_id, password=password)
            if user is not None:
                # log the user in
                login(request, user)
                return HttpResponseRedirect(reverse('Course_Attendance:dashboardStudent', args=(user_id,)))
            else:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Invalid Username or Password'
                })
    else:
        form = AuthenticationForm()
    return render(request, template, {'form': form})


def register_student(request):
    template = 'Course_Attendance/register_student.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentSignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['sid']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists'
                })
            elif User.objects.filter(email=form.cleaned_data['semail']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match'
                })
            else:
                # save the table info to the database
                form.save()
                # create user
                user = User.objects.create_user(
                    form.cleaned_data['sid'],
                    form.cleaned_data['semail'],
                    form.cleaned_data['password']
                )
                user.sname = form.cleaned_data['sname']
                user.scontact = form.cleaned_data['scontact']
                user.sdept = form.cleaned_data['sdept']
                user_id = user.username

                # save the user
                user.save()
                # login the user
                login(request, user)

                # redirect to dashboard
                return HttpResponseRedirect(reverse('Course_Attendance:dashboardStudent', args=(user_id,)))
    else:
        form = StudentSignupForm()

    return render(request, template, {'form': form})


def dashboard_student(request, username):
    student_instance = get_object_or_404(StudentInfo, sid=username)
    print(student_instance.sid)
    student_courses = list(CourseRegistration.objects.filter(sid=username))
    if not student_courses:
        len_courses = 0
    else:
        len_courses = len(student_courses)
    print(len_courses)

    course_instance = []
    course_attendance_list = {}
    percent_present = {}
    for i in range(len_courses):
        course = student_courses[i].cid
        course_id = course.cid
        print(course_id)
        course1 = get_object_or_404(CourseInfo, cid=course_id)
        total_classes = course1.no_of_classes
        print(total_classes)
        course_instance.append(course1)
        temp = list(CourseAttendance.objects.filter(sid=username, cid=course_id).order_by('-class_date'))
        course_attendance_list[course_id] = []
        if temp:
            course_attendance_list[course_id] = temp
            no_of_classes_attended = temp[0].classes_attended
            percent_of_class_attended = (no_of_classes_attended / total_classes) * 100
            percent_present[course_id] = percent_of_class_attended
            print(percent_of_class_attended)
        else:
            percent_present[course_id] = 0.0

    print(course_instance)
    print(course_attendance_list)
    print(percent_present)

    return render(request, 'Course_Attendance/dashboard_student.html', {'student_instance': student_instance,
                                                                        'len_courses': len_courses,
                                                                        'course_instance': course_instance,
                                                                        'course_attendance_list': course_attendance_list,
                                                                        'percent_present': percent_present
                                                                        })


def profile_student_view(request, username):
    template = 'Course_Attendance/profile_student.html'
    student_instance = get_object_or_404(StudentInfo, sid=username)
    print(student_instance.sid)

    return render(request, template, {'student_instance': student_instance})


def profile_student_edit(request, username):
    template = 'Course_Attendance/profile_student_edit.html'
    student_instance = StudentInfo.objects.get(sid=username)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_instance)
        if form.is_valid():
            temp = form.cleaned_data['semail']
            if User.objects.filter(email=temp).exists() and temp != student_instance.semail:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists'
                })
            form.save()
            print(student_instance)
            print(form)
            return HttpResponseRedirect(reverse('Course_Attendance:profileStudentView', args=(student_instance.sid,)))
    else:
        form = StudentProfileForm()
    return render(request, template, {'form': form, 'student_instance': student_instance})


def courses_student(request, username):
    template = 'Course_Attendance/courses_student.html'
    student_instance = StudentInfo.objects.get(sid=username)
    print(student_instance.sid)

    student_courses = list(CourseRegistration.objects.filter(sid=username))
    if not student_courses:
        len_courses = 0
    else:
        len_courses = len(student_courses)
    print(len_courses)

    course_instance = []
    for i in range(len_courses):
        course = student_courses[i].cid
        course_id = course.cid
        print(course_id)
        course1 = get_object_or_404(CourseInfo, cid=course_id)
        course_instance.append(course1)
    print(course_instance)

    course_rows = {}
    i = 0
    while i < len_courses:
        temp = []
        print('i=' + str(i))
        j = 0
        while j < 3:
            print('j=' + str(j))
            if i + j < len_courses:
                temp.append(course_instance[i + j])
            j += 1

        course_rows[i] = temp
        i += 3
    print(course_rows)

    return render(request, template, {'student_instance': student_instance, 'len_courses': len_courses,
                                      'course_rows': course_rows, 'course_instance': course_instance})


def course_attendance_student(request, username, course_id):
    template = 'Course_Attendance/view_attendance_student.html'
    student_instance = StudentInfo.objects.get(sid=username)
    print(student_instance.sid)
    course_instance = CourseInfo.objects.get(cid=course_id)
    course_attendance_list = list(CourseAttendance.objects.filter(sid=username, cid=course_id).order_by('-class_date'))
    print(course_attendance_list)

    return render(request, template, {'student_instance': student_instance, 'course_instance': course_instance,
                                      'course_attendance_list': course_attendance_list})


def register_course_student(request, username):
    template = 'Course_Attendance/register_course_student.html'
    student_instance = StudentInfo.objects.get(sid=username)
    print(student_instance.sid)

    if request.method == 'POST':
        print("post")
        form = CourseIDForm(request.POST)
        if form.is_valid():
            print("form valid")
            course_id = form.cleaned_data['cid']
            print(course_id)
            course_opted = CourseInfo.objects.filter(cid=course_id).exists()
            print(course_opted)
            if not course_opted:
                message = 'Entered Course ID does not exist.'
                print(message)
                return render(request, template, {'student_instance': student_instance, 'form': form,
                                                  'message': message})
            else:
                has_registered = CourseRegistration.objects.filter(cid=course_id, sid=username).exists()
                if has_registered:
                    message = 'You have already registered for this course'
                    print(message)
                    return render(request, template, {'student_instance': student_instance, 'form': form,
                                                      'message': message})
                else:
                    course_obj = CourseInfo.objects.get(cid=course_id)
                    print(course_obj.cid)
                    obj = CourseRegistration(cid=course_obj, sid=student_instance)
                    obj.save()
                    message = 'You have successfully registered for this course.'
                    print(message)
                    return render(request, template, {'student_instance': student_instance, 'form': form,
                                                      'message': message})
        else:
            message = 'Invalid Input'
            print(message)
            return render(request, template, {'student_instance': student_instance, 'form': form,
                                              'message': message})
    else:
        form = CourseIDForm()
    return render(request, template, {'student_instance': student_instance, 'form': form})


def remove_course_student(request, username):
    template = 'Course_Attendance/remove_course_student.html'
    student_instance = StudentInfo.objects.get(sid=username)
    print(student_instance.sid)

    if request.method == 'POST':
        print("post")
        form = CourseIDForm(request.POST)
        if form.is_valid():
            print("form valid")
            course_id = form.cleaned_data['cid']
            print(course_id)
            course_opted = CourseInfo.objects.filter(cid=course_id).exists()
            print(course_opted)
            if not course_opted:
                message = 'Entered Course ID does not exist.'
                print(message)
                return render(request, template, {'student_instance': student_instance, 'form': form,
                                                  'message': message})
            else:
                has_registered = CourseRegistration.objects.filter(cid=course_id, sid=username).exists()
                if not has_registered:
                    message = 'You have not registered for this course'
                    print(message)
                    return render(request, template, {'student_instance': student_instance, 'form': form,
                                                      'message': message})
                else:
                    course_obj = CourseInfo.objects.get(cid=course_id)
                    attendance_instance = CourseAttendance.objects.filter(cid=course_obj, sid=student_instance)
                    attendance_instance.delete()
                    instance = CourseRegistration.objects.get(cid=course_obj, sid=student_instance)
                    instance.delete()
                    message = 'You have successfully removed this course from your courses.'
                    print(message)
                    return render(request, template, {'student_instance': student_instance, 'form': form,
                                                      'message': message})
        else:
            message = 'Invalid Input'
            print(message)
            return render(request, template, {'student_instance': student_instance, 'form': form,
                                              'message': message})
    else:
        form = CourseIDForm()
    return render(request, template, {'student_instance': student_instance, 'form': form})


def delete_account_student(request, username):
    student_instance = StudentInfo.objects.get(sid=username)
    student_instance.delete()
    user_object = User.objects.get(username=username)
    user_object.delete()
    return HttpResponseRedirect(reverse('Course_Attendance:index'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Course_Attendance:index'))


def login_faculty(request):
    template = 'Course_Attendance/login_faculty.html'
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print('valid')
            # get user id
            user_id = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate user
            user = authenticate(username=user_id, password=password)
            if user is not None:
                # log the user in
                login(request, user)
                return HttpResponseRedirect(reverse('Course_Attendance:dashboardFaculty', args=(user_id,)))
            else:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Invalid Username or Password'
                })
        else:
            print('wrong')
            return render(request, template, {
                'form': form,
                'error_message': 'Invalid Username or Password'
            })
    else:
        print('invalid')
        form = AuthenticationForm()
    return render(request, template, {'form': form})


def register_faculty(request):
    template = 'Course_Attendance/register_faculty.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FacultySignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['fid']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists'
                })
            elif User.objects.filter(email=form.cleaned_data['femail']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match'
                })
            else:
                # save the table info to the database
                form.save()
                # create user
                user = User.objects.create_user(
                    form.cleaned_data['fid'],
                    form.cleaned_data['femail'],
                    form.cleaned_data['password']
                )
                user.fname = form.cleaned_data['fname']
                user.fcontact = form.cleaned_data['fcontact']
                user.fdept = form.cleaned_data['fdept']
                user.finterests = form.cleaned_data['finterests']
                user_id = user.username

                # save the user
                user.save()
                # login the user
                login(request, user)

                # redirect to dashboard
                return HttpResponseRedirect(reverse('Course_Attendance:dashboardFaculty', args=(user_id,)))
    else:
        form = FacultySignupForm()

    return render(request, template, {'form': form})


def dashboard_faculty(request, username):
    template = 'Course_Attendance/dashboard_faculty.html'

    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)
    faculty_courses = list(CourseInfo.objects.filter(fid=username))
    if not faculty_courses:
        len_courses = 0
    else:
        len_courses = len(faculty_courses)
    print(len_courses)

    course_rows = {}
    i = 0
    while i < len_courses:
        temp = []
        print('i=' + str(i))
        j = 0
        while j < 3:
            print('j=' + str(j))
            if i + j < len_courses:
                temp.append(faculty_courses[i + j])
            j += 1

        course_rows[i] = temp
        i += 3
    print(course_rows)

    courses_attendance_list = {}
    for i in range(len_courses):
        course_id = faculty_courses[i].cid
        print(course_id)
        each_course_attendance_list = {}
        temp = list(CourseAttendance.objects.filter(cid=course_id).order_by('-class_date'))
        if temp:
            attendance_on_that_date_list = {}
            for j in temp:
                date_of_class = j.class_date
                attendance_on_that_date_list[date_of_class] = []
                temp1 = list(CourseAttendance.objects.filter(cid=course_id, class_date=date_of_class).order_by('sid'))
                if temp1:
                    attendance_on_that_date_list[date_of_class] = temp1

            each_course_attendance_list[course_id] = attendance_on_that_date_list

        courses_attendance_list[course_id] = each_course_attendance_list

    print(courses_attendance_list)

    return render(request, template, {'faculty_instance': faculty_instance, 'faculty_courses': faculty_courses,
                                      'len_courses': len_courses, 'course_rows': course_rows,
                                      'courses_attendance_list': courses_attendance_list})


def attendance_date_faculty(request, username, course_id):
    template = 'Course_Attendance/attendance_date_faculty.html'
    title_message = 'View Attendance'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)
    course_instance = CourseInfo.objects.get(cid=course_id)
    print(course_instance.cid)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            print('valid format date')
            date_selected = form.cleaned_data['date_input']
            if date_selected > datetime.date.today():
                print('wrong date')
                return render(request, template, {'form': form,
                                                  'error_message': 'You have selected a future date. Please try again',
                                                  'view': False, 'faculty_instance': faculty_instance,
                                                  'course_instance': course_instance, 'title_message': title_message})
            else:
                print('valid date')
                attendance_obj_exists = CourseAttendance.objects.filter(cid=course_id, class_date=date_selected).exists()
                if not attendance_obj_exists:
                    print('no object')
                    return render(request, template, {'form': form,
                                                      'error_message': 'No class on this date', 'view': False,
                                                      'faculty_instance': faculty_instance,
                                                      'course_instance': course_instance, 'title_message': title_message})
                else:
                    print('well done')
                    attendance_list = list(CourseAttendance.objects.filter(cid=course_id, class_date=date_selected).order_by('sid'))

                    return render(request, 'Course_Attendance/view_attendance_faculty.html',
                                  {'view': True, 'faculty_instance': faculty_instance,
                                   'course_instance': course_instance,'date_selected': date_selected,
                                   'attendance_list': attendance_list, 'title_message': title_message})
    else:
        form = AttendanceForm()
    return render(request, template, {'form': form, 'faculty_instance': faculty_instance,
                                      'course_instance': course_instance, 'title_message': title_message})


def give_attendance_date_faculty(request, username, course_id):
    template = 'Course_Attendance/attendance_date_faculty.html'
    title_message = 'Give Attendance'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)
    course_instance = CourseInfo.objects.get(cid=course_id)
    print(course_instance.cid)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            print('valid format date')
            date_selected = form.cleaned_data['date_input']
            if date_selected > datetime.date.today():
                print('wrong date')
                return render(request, template, {'form': form,
                                                  'error_message': 'You have selected a future date. Please try again',
                                                  'view': False, 'faculty_instance': faculty_instance,
                                                  'course_instance': course_instance, 'title_message': title_message})
            else:
                print('valid date')
                attendance_obj_exists = CourseAttendance.objects.filter(cid=course_id,
                                                                        class_date=date_selected).exists()
                if attendance_obj_exists:
                    print('attendance already marked')
                    message = 'Attendance is already marked for this class date'
                    return render(request, template, {'form': form,
                                                      'error_message': message, 'view': False,
                                                      'faculty_instance': faculty_instance,
                                                      'course_instance': course_instance, 'title_message': title_message})
                else:
                    print('well done')
                    print(date_selected)
                    return HttpResponseRedirect(reverse('Course_Attendance:facultyGiveAttendance',
                                                        args=(username, course_id, date_selected,)))
    else:
        form = AttendanceForm()
    return render(request, template, {'form': form, 'faculty_instance': faculty_instance,
                                      'course_instance': course_instance, 'title_message': title_message})


def give_attendance(request, username, course_id, date):
    template = 'Course_Attendance/give_attendance_faculty.html'

    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)
    course_instance = CourseInfo.objects.get(cid=course_id)
    print(course_instance.cid)
    student_list = CourseRegistration.objects.filter(cid=course_id).order_by('sid')
    print(student_list)
    len_students = len(student_list)
    CourseAttendanceFormSet = formset_factory(CourseAttendanceForm, extra=len_students)
    i = 0
    if len_students!= 0:
        print(student_list[i].sid.sid)
    else:
        message = 'No student has enrolled for this course'
        return render(request, template, {'message': message, 'faculty_instance': faculty_instance,
                                          'course_instance': course_instance, 'date_selected': date})
    if request.method == 'POST':
        print(1)
        formset = CourseAttendanceFormSet(request.POST)
        print(2)
        for form in formset:
            if form.is_valid():
                print(form.cleaned_data)
                student_id = student_list[i].sid.sid
                student_instance = StudentInfo.objects.get(sid=student_id)
                student_attendance = form.cleaned_data['attendance']
                print(student_attendance)
                total_classes_attended = 0
                temp_obj = list(CourseAttendance.objects.filter(sid=student_id, cid=course_id).order_by('-class_date'))
                if temp_obj:
                    print(temp_obj)
                    print(temp_obj[0].classes_attended)
                    if student_attendance == 'P':
                        total_classes_attended = temp_obj[0].classes_attended + 1
                        print('P', total_classes_attended)
                    else:
                        total_classes_attended = temp_obj[0].classes_attended
                        print('A', total_classes_attended)
                else:
                    if student_attendance == 'P':
                        total_classes_attended = 1
                        print('P', total_classes_attended)

                obj = CourseAttendance(cid=course_instance, sid=student_instance,
                                       class_date=date, attendance=student_attendance,
                                       classes_attended=total_classes_attended)
                obj.save()

                i += 1

            return HttpResponseRedirect(reverse('Course_Attendance:facultyGiveAttendanceDate',
                                                args=(username, course_id,)))

        print(formset.forms[0])

        zipped_data = zip(student_list, formset)
        for i,j in zipped_data :
            print(i.sid.sid)
            print(j)
            break
    else:
        formset = CourseAttendanceFormSet()
    return render(request, template, {'formset': formset, 'faculty_instance': faculty_instance,
                                      'course_instance': course_instance, 'date_selected': date,
                                      'student_list': student_list, 'zipped_data': zip(student_list, formset.forms)})


def profile_faculty_view(request, username):
    template = 'Course_Attendance/profile_faculty.html'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)

    return render(request, template, {'faculty_instance': faculty_instance})


def profile_faculty_edit(request, username):
    template = 'Course_Attendance/profile_faculty_edit.html'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)

    if request.method == 'POST':
        form = FacultyProfileForm(request.POST, instance=faculty_instance)
        if form.is_valid():
            temp = form.cleaned_data['femail']
            if User.objects.filter(email=temp).exists() and temp != faculty_instance.femail:
                return render(request, template, {
                    'form': form,
                    'error_message': 'This Email already exists'
                })
            form.save()
            print(faculty_instance)
            print(form)
            return HttpResponseRedirect(reverse('Course_Attendance:profileFacultyView', args=(faculty_instance.fid,)))
    else:
        form = FacultyProfileForm()
    return render(request, template, {'form': form, 'faculty_instance': faculty_instance})


def add_course(request, username):
    template = 'Course_Attendance/add_course.html'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)

    if request.method == 'POST':
        print("post")
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            print("form valid")
            course_id = form.cleaned_data['cid']
            print(course_id)

            course_exists = CourseInfo.objects.filter(cid=course_id).exists()
            print(course_exists)
            if course_exists:
                message = 'Entered Course ID already exists.'
                print(message)
                return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                                  'message': message})
            else:
                course_name = form.cleaned_data['cname']
                course_classes = form.cleaned_data['no_of_classes']

                obj = CourseInfo(cid=course_id, cname=course_name, no_of_classes=course_classes,
                                 fid=faculty_instance, course_plan=request.FILES['course_plan'])
                obj.save()
                message = 'You have successfully added this course.'
                print(message)
                return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                                  'message': message})
        else:
            message = 'Invalid Input'
            print(message)
            return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                              'message': message})
    else:
        form = CourseForm()
    return render(request, template, {'faculty_instance': faculty_instance, 'form': form})


def delete_course_faculty(request, username):
    template = 'Course_Attendance/delete_course_faculty.html'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)

    if request.method == 'POST':
        print("post")
        form = CourseIDForm(request.POST)
        if form.is_valid():
            print("form valid")
            course_id = form.cleaned_data['cid']
            print(course_id)
            course_selected = CourseInfo.objects.filter(cid=course_id).exists()
            print(course_selected)
            if not course_selected:
                message = 'Entered Course ID does not exist.'
                print(message)
                return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                                  'message': message})
            else:
                is_course_faculty = CourseInfo.objects.filter(cid=course_id, fid=username).exists()
                if not is_course_faculty:
                    message = 'You do not teach this course. You can only delete a course you teach.'
                    print(message)
                    return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                                      'message': message})
                else:
                    course_obj = CourseInfo.objects.get(cid=course_id)
                    attendance_instance = CourseAttendance.objects.filter(cid=course_obj)
                    if attendance_instance:
                        attendance_instance.delete()
                    registration_instance = CourseRegistration.objects.filter(cid=course_obj)
                    if registration_instance:
                        registration_instance.delete()

                    filename = course_obj.course_plan
                    filename1 = filename.decode('utf-8')
                    print(filename1)
                    dir = '/home/shweta/PycharmProjects/Course_Attendance_Management_Project/CourseAttendance_ManagementProject/media/'
                    filepath = dir + filename1
                    print(filepath)
                    os.remove(filepath)
                    course_obj.delete()

                    message = 'You have successfully deleted this course.'
                    print(message)
                    return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                                      'message': message})
        else:
            message = 'Invalid Input'
            print(message)
            return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                              'message': message})
    else:
        form = CourseIDForm()
    return render(request, template, {'faculty_instance': faculty_instance, 'form': form})


def delete_account_faculty(request, username):
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)
    faculty_instance.delete()
    user_object = User.objects.get(username=username)
    user_object.delete()
    return HttpResponseRedirect(reverse('Course_Attendance:index'))

'''
def edit_course_enter_cid(request, username):
    template = 'Course_Attendance/course_edit_cid.html'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)

    if request.method == 'POST':
        print("post")
        form = CourseIDForm(request.POST)
        if form.is_valid():
            print("form valid")
            course_id = form.cleaned_data['cid']
            print(course_id)
            course_opted = CourseInfo.objects.filter(cid=course_id).exists()
            print(course_opted)
            if not course_opted:
                message = 'Entered Course ID does not exist.'
                print(message)
                return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                                  'message': message})
            else:
                is_course_faculty = CourseInfo.objects.filter(cid=course_id, fid=username).exists()
                if not is_course_faculty:
                    message = 'You do not take this course. You can only edit a course you teach.'
                    print(message)
                    return render(request, template, {'faculty_instance': faculty_instance, 'form': form,
                                                      'message': message})

                else:
                    return HttpResponseRedirect(reverse('Course_Attendance:editCourse',
                                                        args=(username,course_id)))
    else:
        form = CourseIDForm()
    return render(request, template, {'form':form, 'faculty_instance':faculty_instance})


def edit_course(request, username, course_id):
    template = 'Course_Attendance/course_edit.html'
    faculty_instance = get_object_or_404(FacultyInfo, fid=username)
    print(faculty_instance.fid)
    course_instance = CourseInfo.objects.get(cid=course_id)
    print(course_instance)
    if request.method == 'POST':
        form = CourseEditForm(request.POST, instance=course_instance)
        if form.is_valid():
            form.save()
            print(faculty_instance)
            print(form)
            return render(request, template, {
                'form': form, 'faculty_instance': faculty_instance, 'course_instance':course_instance,
                'message': 'You have successfully edited this Course.'
            })
    else:
        form = CourseEditForm()
    return render(request, template, {'form': form, 'faculty_instance': faculty_instance,
                                      'course_instance':course_instance})
'''








