from django.db import models
from django.contrib.auth.models import User


class CustomUserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="custom_profile"
    )
    DESIGNATION_CHOICES = [
        ('Master Admin', 'Master Admin'),
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    ]
    designation = models.CharField(
        max_length=100, blank=False, null=False, choices=DESIGNATION_CHOICES)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Custom User Profile"
        verbose_name_plural = "Custom User Profiles"


class Student(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=False)
    mis = models.CharField(max_length=9, null=False, blank=False, unique=True)
    phone_number = models.CharField(
        max_length=10, null=False, blank=False, unique=True)

    BRANCH_CHOICES = [
        ('Electronics and Telecommunication Engineering',
         'Electronics and Telecommunication Engineering'),
        ('Manufacturing Science and Engineering',
         'Manufacturing Science and Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Computer Engineering', 'Computer Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Metallurgy and Materials Technology',
         'Metallurgy and Materials Technology'),
        ('Instrumentation and Control Engineering',
         'Instrumentation and Control Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
    ]

    branch = models.CharField(
        max_length=200, choices=BRANCH_CHOICES, null=False, blank=False)

    YEAR_CHOICES = [
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year')
    ]

    year = models.CharField(
        max_length=100, choices=YEAR_CHOICES, null=False, blank=False)

    DIV_CHOICES = [
        ('Div 1', 'Div 1'),
        ('Div 2', 'Div 2')
    ]

    div = models.CharField(
        max_length=50, choices=DIV_CHOICES, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.mis}_{self.name.replace(' ', '_')}"


class Faculty(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(
        max_length=250, null=False, blank=False, unique=True)

    DEPARTMENT_CHOICES = [
        ('Department of Applied Science', 'Department of Applied Science'),
        ('Bhau Institute of Innovation, Entrepreneurship and Leadership',
         'Bhau Institute of Innovation, Entrepreneurship and Leadership'),
        ('Department of Civil Engineering', 'Department of Civil Engineering'),
        ('Department of Computer Engineering & IT',
         'Department of Computer Engineering & IT'),
        ('Department of Electrical Engineering',
         'Department of Electrical Engineering'),
        ('Department of Electronics and Telecommunication Engineering',
         'Department of Electronics and Telecommunication Engineering'),
        ('Department of Instrumentation and Control Engineering',
         'Department of Instrumentation and Control Engineering'),
        ('Department of Mathematics', 'Department of Mathematics'),
        ('Department of Mechanical Engineering',
         'Department of Mechanical Engineering'),
        ('Department of Metallurgy and Materials Engineering',
         'Department of Metallurgy and Materials Engineering'),
        ('Department of Manufacturing Engineering and Industrial Management',
         'Department of Manufacturing Engineering and Industrial Management'),
        ('Department of Physics', 'Department of Physics'),
    ]

    department = models.CharField(
        max_length=450, blank=False, null=False, choices=DEPARTMENT_CHOICES)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    name = models.CharField(
        max_length=300, null=False, blank=False)

    YEAR_CHOICES = [
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year')
    ]

    year = models.CharField(
        max_length=100, choices=YEAR_CHOICES, null=False, blank=False)

    SEM_CHOICES = [
        ('Odd Semester', 'Odd Semester'),
        ('Even Semester', 'Even Semester')
    ]

    sem = models.CharField(
        max_length=100, choices=SEM_CHOICES, null=False, blank=False)

    BRANCH_CHOICES = [
        ('Electronics and Telecommunication Engineering',
         'Electronics and Telecommunication Engineering'),
        ('Manufacturing Science and Engineering',
         'Manufacturing Science and Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Computer Engineering', 'Computer Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Metallurgy and Materials Technology',
         'Metallurgy and Materials Technology'),
        ('Instrumentation and Control Engineering',
         'Instrumentation and Control Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
    ]

    branch = models.CharField(
        max_length=200, choices=BRANCH_CHOICES, null=False, blank=False)

    class Meta:
        unique_together = ['name', 'year', 'sem', 'branch']

    def __str__(self) -> str:
        return f'{self.branch}_{self.name}_{self.year}_{self.sem}'


class Course_Faculty(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    DIV_CHOICES = [
        ('Div 1', 'Div 1'),
        ('Div 2', 'Div 2')
    ]
    div = models.CharField(
        max_length=50, choices=DIV_CHOICES, null=False, blank=False)

    class Meta:
        unique_together = ['course', 'faculty', 'div']
        verbose_name_plural = "Course Faculties"

    def __str__(self) -> str:
        return f'{self.course}_{self.div}_{self.faculty}'


class Attendance(models.Model):
    course_faculty = models.ForeignKey(
        Course_Faculty, on_delete=models.CASCADE)
    total_students = models.ManyToManyField(
        Student, related_name='total_student')
    present_students = models.ManyToManyField(
        Student, related_name="present_students")
    absent_students = models.ManyToManyField(
        Student, related_name="absent_students")
    date = models.DateField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)

    class Meta:
        unique_together = ['course_faculty', 'date', 'start_time', 'end_time']

    def __str__(self) -> str:
        return f'{self.course_faculty}_{self.date}_{self.start_time}-{self.end_time}'


class Cumulative_Student_Attendance(models.Model):
    course_faculty = models.ForeignKey(
        Course_Faculty, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['course_faculty']

    def __str__(self) -> str:
        return self.course_faculty
