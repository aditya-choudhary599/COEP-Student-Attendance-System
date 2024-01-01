from django import forms
from .models import *


class FileUploadForm(forms.Form):
    file = forms.FileField()


class Student_Form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email", "mis",
                  "phone_number", "branch", "year", "div"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-dark text-light"}),

            "email": forms.EmailInput(attrs={"class": "form-control bg-dark text-light"}),

            "mis": forms.TextInput(attrs={"class": "form-control bg-dark text-light"}),

            "phone_number": forms.TextInput(attrs={"class": "form-control bg-dark text-light"}),

            "branch": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "year": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "div": forms.Select(attrs={"class": "form-control bg-dark text-light"}),
        }

    def clean_mis(self):
        mis = str(self.cleaned_data["mis"])
        if mis.isdigit() and len(mis) == 9:
            return mis

        raise forms.ValidationError(
            "MIS Number should be exactly of 9 digits!")

    def clean_phone_number(self):
        phone_number = str(self.cleaned_data["phone_number"])
        if phone_number.isdigit() and len(phone_number) == 10:
            return phone_number

        raise forms.ValidationError(
            "Phone number should be exactly 10 digits and contain only digits."
        )


class Update_Student_Form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email", "phone_number", "branch", "year", "div"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-dark text-light"}),

            "email": forms.EmailInput(attrs={"class": "form-control bg-dark text-light"}),

            "phone_number": forms.TextInput(attrs={"class": "form-control bg-dark text-light"}),

            "branch": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "year": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "div": forms.Select(attrs={"class": "form-control bg-dark text-light"}),
        }

    def clean_phone_number(self):
        phone_number = str(self.cleaned_data["phone_number"])
        if phone_number.isdigit() and len(phone_number) == 10:
            return phone_number

        raise forms.ValidationError(
            "Phone number should be exactly 10 digits and contain only digits."
        )


class Faculty_Form(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ["name", "email", "department"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-dark text-light"}),

            "email": forms.EmailInput(attrs={"class": "form-control bg-dark text-light"}),

            "department": forms.Select(attrs={"class": "form-control bg-dark text-light"})
        }


class Update_Faculty_Form(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-dark text-light"})
        }


class Course_Form(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "year", "sem", "branch"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-dark text-light"}),

            "year": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "sem": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "branch": forms.Select(attrs={"class": "form-control bg-dark text-light"})
        }


class Course_Faculty_Form(forms.ModelForm):
    class Meta:
        model = Course_Faculty
        fields = ["course", "faculty", "div"]
        widgets = {
            "course": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "faculty": forms.Select(attrs={"class": "form-control bg-dark text-light"}),

            "div": forms.Select(attrs={"class": "form-control bg-dark text-light"})
        }


class Update_Course_Faculty_Form(forms.ModelForm):
    class Meta:
        model = Course_Faculty
        fields = ["faculty"]
        widgets = {
            "faculty": forms.Select(attrs={"class": "form-control bg-dark text-light"})
        }


class Attendance_Form(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["total_students", 'date', 'start_time', 'end_time']
        widgets = {
            "total_students": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input bg-dark text-light"}),
            "date": forms.DateInput(attrs={'type': 'date', "class": "form-control bg-dark text-light"}),
            "start_time": forms.TimeInput(attrs={'class': 'form-control bg-dark text-light'}),
            "end_time": forms.TimeInput(attrs={'class': 'form-control bg-dark text-light'}),
        }


class Cumulative_Student_Attendance_Form(forms.ModelForm):
    class Meta:
        model = Cumulative_Student_Attendance
        fields = ['course_faculty']
        widgets = {
            "course_faculty": forms.Select(attrs={"class": "form-control bg-dark text-light"})
        }
