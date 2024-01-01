from django.urls import path
from .views import *

urlpatterns = [
    # All General Views
    path('', landing_page_view, name='landing_page_view'),
    path('logout/', logout_view, name='logout_view'),
    path('change_password/', password_change_view, name='password_change_view'),

    # All views related to Master_Admin
    path('master_admin/home_page', master_admin_home_page_view,
         name='master_admin_home_page_view'),

    # All view related to Master_Admin-Student
    path('master_admin/add_student_record',
         add_student_record_view, name='add_student_record_view'),
    path('master_admin/all_students_records',
         all_student_records_view, name='all_student_records_view'),
    path('master_admin/update_student_record/<int:id>',
         update_student_record_view, name='update_student_record_view'),
    path('master_admin/delete_student_record/<int:id>',
         delete_student_record_view, name='delete_student_record_view'),
    path('master_admin/year_end_student_update',
         year_end_student_update_view, name='year_end_student_update_view'),

    # All views realted to Master_Admin-Faculty
    path('master_admin/add_faculty_record',
         add_faculty_record_view, name='add_faculty_record_view'),
    path('master_admin/see_all_faculty_records',
         all_faculty_records_view, name='all_faculty_records_view'),
    path('master_admin/update_faculty_record/<int:id>',
         update_faculty_record_view, name='update_faculty_record_view'),
    path('master_admin/delete_faculty_record/<int:id>',
         delete_faculty_record_view, name='delete_faculty_record_view'),

    # All views realted to Master_Admin-Course
    path('master_admin/add_course_record',
         add_course_record_view, name='add_course_record_view'),
    path('master_admin/see_all_course_records',
         all_course_records_view, name='all_course_records_view'),
    path('master_admin/delete_course_record/<int:id>',
         delete_course_record_view, name='delete_course_record_view'),

    # All views realted to Master_Admin-Course_Faculty
    path('master_admin/add_course_faculty_record',
         add_course_faculty_record_view, name='add_course_faculty_record_view'),
    path('master_admin/see_all_course_faculty_records',
         all_course_faculty_records_view, name='all_course_faculty_records_view'),
    path('master_admin/update_course_faculty_record/<int:id>',
         update_course_faculty_view, name='update_course_faculty_view'),
    path('master_admin/delete_course_faculty_record/<int:id>',
         delete_course_faculty_view, name='delete_course_faculty_view'),

    # All views realted to Master_Admin-Attendance
    path('master_admin/see_all_attendance_records',
         all_attendance_records_view, name='all_attendance_records_view'),
    path('master_admin/sem_end_delete_attendance', sem_end_delete_all_attendance_records_view,
         name='sem_end_delete_all_attendance_records_view'),
    path('master_admin/get_sem_end_student_attendance_report',
         sem_end_students_attendance_report_view, name='sem_end_students_attendance_report_view'),

    # All views related to Faculty
    path('faculty/home_page/<int:id>', faculty_home_page_view,
         name='faculty_home_page_view'),

    # All view related Faculty-Attendance
    path('faculty/add_attendance_record/<int:course_faculty_record_id>',
         add_attendance_record_view, name='add_attendance_record_view'),

    # All views related to Student
    path('student/home_page/<int:id>', student_home_page_view,
         name='student_home_page_view'),

    # All view related to Student-Attendance
    path('student/student_course_faculty_attendance/<int:course_faculty_id>',
         student_course_faculty_attendance_detailed_view, name='student_course_faculty_attendance_detailed_view'),
]
