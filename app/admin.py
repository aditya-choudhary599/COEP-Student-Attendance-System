from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUserProfile)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Course_Faculty)
admin.site.register(Attendance)
admin.site.register(Cumulative_Student_Attendance)
