from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('archive/', views.archive, name='archive'),
    re_path('courseDetail/(?P<course_id>[A-Z]{2}[0-9]{3})', views.course_detail, name='courseDetail'),
    path('loginStudent/', views.login_student, name='loginStudent'),
    path('registerStudent/', views.register_student, name='registerStudent'),
    re_path('dashboardStudent/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/', views.dashboard_student, name='dashboardStudent'),
    re_path('profileStudentView/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/', views.profile_student_view, name='profileStudentView'),
    re_path('profileStudentEdit/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/', views.profile_student_edit, name='profileStudentEdit'),
    re_path('coursesStudent/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/', views.courses_student, name='coursesStudent'),
    re_path('studentCourseAttendance/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/(?P<course_id>[A-Z]{2}[0-9]{3})/',
            views.course_attendance_student, name='studentCourseAttendance'),
    re_path('studentCourseRegister/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/', views.register_course_student,
            name='studentCourseRegister'),
    re_path('studentCourseRemove/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/', views.remove_course_student,
            name='studentCourseRemove'),
    re_path('studentDeleteAccount/(?P<username>[0-9]{2}[A-Z]{2}[0-9]{3})/', views.delete_account_student,
            name='studentDeleteAccount'),
    path('logout/', views.logout_user, name='logout'),
    path('loginFaculty/', views.login_faculty, name='loginFaculty'),
    path('registerFaculty/', views.register_faculty, name='registerFaculty'),
    re_path('dashboardFaculty/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/', views.dashboard_faculty, name='dashboardFaculty'),
    re_path('facultyCourseAttendanceDate/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/(?P<course_id>[A-Z]{2}[0-9]{3})',
            views.attendance_date_faculty, name='facultyCourseAttendanceDate'),
    re_path('facultyGiveAttendanceDate/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/(?P<course_id>[A-Z]{2}[0-9]{3})',
            views.give_attendance_date_faculty, name='facultyGiveAttendanceDate'),
    re_path('facultyGiveAttendance/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/(?P<course_id>[A-Z]{2}[0-9]{3})/(?P<date>\d{4}-\d{2}-\d{2})',
            views.give_attendance, name='facultyGiveAttendance'),
    re_path('profileFacultyView/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/', views.profile_faculty_view, name='profileFacultyView'),
    re_path('profileFacultyEdit/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/', views.profile_faculty_edit, name='profileFacultyEdit'),
    re_path('addCourse/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/', views.add_course, name='addCourse'),
    re_path('facultyCourseDelete/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/', views.delete_course_faculty,
            name='facultyCourseDelete'),
    re_path('facultyDeleteAccount/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/', views.delete_account_faculty,
            name='facultyDeleteAccount'),
]

'''
For Edit Course:
    re_path('editCourseCid/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/', views.edit_course_enter_cid, name='editCourseCid'),
    re_path('editCourse/(?P<username>F[0-9]{2}[A-Z]{2}[0-9]{3})/(?P<course_id>[A-Z]{2}[0-9]{3})', views.edit_course,
            name='editCourse')
'''