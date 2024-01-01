import os
import pandas as pd
import pdfkit
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import *
from .forms import *
from .decorators import *


@decorator_for_website_landing_page
def landing_page_view(request: HttpRequest):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            password = fm.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                custom_profile = CustomUserProfile.objects.get(user=user)
                designation = custom_profile.designation
                if designation == 'Master Admin':
                    return redirect("master_admin_home_page_view")
                elif designation == 'Student':
                    obj = Student.objects.get(mis=request.user.username)
                    return redirect("student_home_page_view", id=obj.pk)
                elif designation == 'Faculty':
                    obj = Faculty.objects.get(email=request.user.username)
                    return redirect("faculty_home_page_view", id=obj.pk)
    else:
        fm = AuthenticationForm()

    return render(request, "app/website_landing_page.html", {"form": fm})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect('landing_page_view')


@decorator_for_password_change_page
def password_change_view(request: HttpRequest):
    helper_1 = CustomUserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()

            if (helper_1.designation == 'Master Admin'):
                update_session_auth_hash(request, fm.user)
                return redirect("master_admin_home_page_view")

            elif (helper_1.designation == 'Faculty'):
                obj = Faculty.objects.get(email=request.user.username)
                update_session_auth_hash(request, fm.user)
                return redirect("faculty_home_page_view", id=obj.pk)

            else:
                obj = Student.objects.get(mis=request.user.username)
                update_session_auth_hash(request, fm.user)
                return redirect("student_home_page_view", id=obj.pk)

    else:
        id = None
        if (helper_1.designation == 'Master Admin'):
            back_to_home_path_name = "master_admin_home_page_view"

        elif (helper_1.designation == 'Faculty'):
            obj = Faculty.objects.get(email=request.user.username)
            back_to_home_path_name = "faculty_home_page_view"
            id = obj.pk

        else:
            obj = Student.objects.get(mis=request.user.username)
            back_to_home_path_name = "student_home_page_view"
            id = obj.pk

        fm = PasswordChangeForm(request.user)

    return render(request, "app/password_change_page.html", {"form": fm, "back_to_home_path_name": back_to_home_path_name, "additional_id": id})


@login_required_for_master_admin
def master_admin_home_page_view(request: HttpRequest):
    return render(request, 'app/MA_home_page.html')


@login_required_for_master_admin
def add_student_record_via_csv_file(file):
    with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    csv_file = os.path.abspath(os.path.join(settings.MEDIA_ROOT, file.name))

    df = pd.read_csv(csv_file)
    for i in range(df.shape[0]):
        record = df.loc[i].to_dict()
        obj = Student_Form(data={
            'name': str(record['Student Name ']).strip(),
            'email': str(record['Coep MailId']).strip(),
            'mis': str(record['MIS No']).strip(),
            'phone_number': str(record['Mob No']).strip(),
            'branch': str(record['Branch']).strip(),
            'year': str(record['Year']).strip(),
            'div': str(record['Div']).strip(),
        })

        if obj.is_valid():
            obj.save()

            # First create the entry in the inbuilt user
            username = str(record['MIS No']).strip()
            password = 'COEP1234'
            user = User.objects.create_user(
                username=username, password=password)
            user.save()

            # Now create the entry in custom user
            custom_user = CustomUserProfile.objects.create(
                user=user, designation='Student')
            custom_user.save()

    os.remove(csv_file)


@login_required_for_master_admin
def add_student_record_view(request: HttpRequest):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            add_student_record_via_csv_file(csv_file)

        else:
            fm = Student_Form(request.POST)
            if fm.is_valid():
                fm.save()

                # First create the entry in the inbuilt user
                username = str(fm.cleaned_data['mis']).strip()
                password = 'COEP1234'
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()

                # Now create the entry in custom user
                custom_user = CustomUserProfile.objects.create(
                    user=user, designation='Student')
                custom_user.save()

    fm_1 = Student_Form()
    fm_2 = FileUploadForm()

    return render(request, 'app/MA_add_student_record_page.html', {'form_1': fm_1, 'form_2': fm_2})


@login_required_for_master_admin
def all_student_records_view(request: HttpRequest):
    if request.method == 'POST':
        search_query = str(request.POST.get('search_area')).strip()

        if not search_query:
            all_records = Student.objects.all()
        else:
            all_records = Student.objects.filter(name__icontains=search_query)

            all_records = all_records.union(
                Student.objects.filter(email__icontains=search_query))

            all_records = all_records.union(
                Student.objects.filter(mis__icontains=search_query))

            all_records = all_records.union(
                Student.objects.filter(phone_number__icontains=search_query))

            all_records = all_records.union(
                Student.objects.filter(branch__icontains=search_query))

            all_records = all_records.union(
                Student.objects.filter(year__icontains=search_query))

            all_records = all_records.union(
                Student.objects.filter(div__icontains=search_query))

    else:
        all_records = Student.objects.all()

    return render(request, 'app/MA_see_all_student_records_page.html', {'all_records': all_records})


@login_required_for_master_admin
def update_student_record_view(request, id):
    if request.method == "POST":
        pi = Student.objects.get(pk=id)
        fm = Update_Student_Form(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = Student.objects.get(pk=id)
        fm = Update_Student_Form(instance=pi)

    return render(request, "app/MA_update_student_record_page.html", {"form": fm})


@login_required_for_master_admin
def delete_student_record_view(request, id):
    if request.method == 'POST':
        pi_1 = Student.objects.get(pk=id)
        pi_2 = User.objects.get(username=pi_1.mis)

        pi_2.delete()
        pi_1.delete()

        return redirect("all_student_records_view")


@login_required_for_master_admin
def year_end_student_update_view(request: HttpRequest):
    # Step 1 : 4th year -> delete
    temp = Student.objects.filter(year='Fourth Year')
    for record in temp:
        user_record = User.objects.get(username=record.mis)
        user_record.delete()
        record.delete()

    # Step 2: 3rd year -> 4th year
    Student.objects.filter(year='Third Year').update(year='Fourth Year')

    # Step 3 : 2nd year -> 3rd year
    Student.objects.filter(year='Second Year').update(year='Third Year')

    # Step 4 : 1st year -> 2nd year
    Student.objects.filter(year='First Year').update(year='Second Year')

    return redirect('all_student_records_view')


@login_required_for_master_admin
def add_faculty_record_via_csv_file(file):
    with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    csv_file = os.path.abspath(os.path.join(settings.MEDIA_ROOT, file.name))

    df = pd.read_csv(csv_file)
    for i in range(df.shape[0]):
        record = df.loc[i].to_dict()
        obj = Faculty_Form(data={
            'name': str(record['Name']).strip(),
            'email': str(record['Email Id ']).strip(),
            'department': str(record['Department']).strip(),
        })

        if obj.is_valid():
            obj.save()

            # First create the entry in the inbuilt user
            username = str(record['Email Id ']).strip()
            password = 'COEP1234'
            user = User.objects.create_user(
                username=username, password=password)
            user.save()

            # Now create the entry in custom user
            custom_user = CustomUserProfile.objects.create(
                user=user, designation='Faculty')
            custom_user.save()

    os.remove(csv_file)


@login_required_for_master_admin
def add_faculty_record_view(request: HttpRequest):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            add_faculty_record_via_csv_file(csv_file)
        else:
            fm = Faculty_Form(request.POST)
            if fm.is_valid():
                fm.save()

                # First create the entry in the inbuilt user
                username = str(fm.cleaned_data['email']).strip()
                password = 'COEP1234'
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()

                # Now create the entry in custom user
                custom_user = CustomUserProfile.objects.create(
                    user=user, designation='Faculty')
                custom_user.save()

    fm_1 = Faculty_Form()
    fm_2 = FileUploadForm()

    return render(request, 'app/MA_add_faculty_record_page.html', {'form_1': fm_1, 'form_2': fm_2})


@login_required_for_master_admin
def all_faculty_records_view(request: HttpRequest):
    if request.method == 'POST':
        search_query = str(request.POST.get('search_area')).strip()

        if not search_query:
            all_records = Faculty.objects.all()
        else:
            all_records = Faculty.objects.filter(name__icontains=search_query)

            all_records = all_records.union(
                Faculty.objects.filter(email__icontains=search_query))

            all_records = all_records.union(
                Faculty.objects.filter(department__icontains=search_query))

    else:
        all_records = Faculty.objects.all()

    return render(request, 'app/MA_see_all_faculty_records_page.html', {'all_records': all_records})


@login_required_for_master_admin
def update_faculty_record_view(request, id):
    if request.method == 'POST':
        pi = Faculty.objects.get(pk=id)
        fm = Update_Faculty_Form(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = Faculty.objects.get(pk=id)
        fm = Update_Faculty_Form(instance=pi)

    return render(request, 'app/MA_update_faculty_record_page.html', {'form': fm})


@login_required_for_master_admin
def delete_faculty_record_view(request, id):
    if request.method == 'POST':
        pi_1 = Faculty.objects.get(pk=id)
        pi_2 = User.objects.get(username=pi_1.email)

        pi_2.delete()
        pi_1.delete()

        return redirect("all_faculty_records_view")


@login_required_for_master_admin
def add_course_record_via_csv_file(file):
    with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    csv_file = os.path.abspath(os.path.join(settings.MEDIA_ROOT, file.name))

    df = pd.read_csv(csv_file)
    for i in range(df.shape[0]):
        record = df.loc[i].to_dict()
        obj = Course_Form(data={
            'name': str(record['Course Name']).strip(),
            'year': str(record['Year']).strip(),
            'sem': str(record['Semester']).strip(),
            'branch': str(record['Branch']).strip()
        })

        if obj.is_valid():
            obj.save()

    os.remove(csv_file)


@login_required_for_master_admin
def add_course_record_view(request: HttpRequest):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            add_course_record_via_csv_file(csv_file)
        else:
            fm = Course_Form(request.POST)
            if fm.is_valid():
                fm.save()

    fm_1 = Course_Form()
    fm_2 = FileUploadForm()

    return render(request, 'app/MA_add_course_record_page.html', {'form_1': fm_1, 'form_2': fm_2})


@login_required_for_master_admin
def all_course_records_view(request: HttpRequest):
    if request.method == 'POST':
        search_query = str(request.POST.get('search_area')).strip()

        if not search_query:
            all_records = Course.objects.all()
        else:
            all_records = Course.objects.filter(name__icontains=search_query)

            all_records = all_records.union(
                Course.objects.filter(year__icontains=search_query))

            all_records = all_records.union(
                Course.objects.filter(sem__icontains=search_query))

            all_records = all_records.union(
                Course.objects.filter(branch__icontains=search_query))
    else:
        all_records = Course.objects.all()

    return render(request, 'app/MA_see_all_course_records_page.html', {'all_records': all_records})


@login_required_for_master_admin
def delete_course_record_view(request, id):
    if request.method == 'POST':
        pi_1 = Course.objects.get(pk=id)
        pi_1.delete()

    return redirect("all_course_records_view")


@login_required_for_master_admin
def add_course_faculty_record_via_csv_file(file):
    with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    csv_file = os.path.abspath(os.path.join(settings.MEDIA_ROOT, file.name))

    df = pd.read_csv(csv_file)
    for i in range(df.shape[0]):
        record = df.loc[i].to_dict()
        course_record = Course.objects.get(
            name=str(record['Course Name']).strip(),
            year=str(record['Year']).strip(),
            sem=str(record['Semester']).strip(),
            branch=str(record['Branch']).strip()
        )
        faculty_record = Faculty.objects.get(
            name=str(record['Faculty Name']).strip(),
            email=str(record['Email Id ']).strip(),
            department=str(record['Department']).strip()
        )

        obj = Course_Faculty_Form(data={
            'course': course_record,
            'faculty': faculty_record,
            'div': str(record['Divison']).strip()
        })

        if obj.is_valid():
            obj.save()

    os.remove(csv_file)


@login_required_for_master_admin
def add_course_faculty_record_view(request: HttpRequest):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            add_course_faculty_record_via_csv_file(csv_file)
        else:
            fm = Course_Faculty_Form(request.POST)
            if fm.is_valid():
                fm.save()

    fm_1 = Course_Faculty_Form()
    fm_2 = FileUploadForm()

    return render(request, 'app/MA_add_course_faculty_record_page.html', {'form_1': fm_1, 'form_2': fm_2})


@login_required_for_master_admin
def all_course_faculty_records_view(request: HttpRequest):
    if request.method == 'POST':
        search_query = str(request.POST.get('search_area')).strip()

        if not search_query:
            all_records = Course_Faculty.objects.all()
        else:
            all_records = Course_Faculty.objects.filter(
                course__name__icontains=search_query)

            all_records = all_records.union(
                Course_Faculty.objects.filter(course__year__icontains=search_query))

            all_records = all_records.union(
                Course_Faculty.objects.filter(course__sem__icontains=search_query))

            all_records = all_records.union(
                Course_Faculty.objects.filter(course__branch__icontains=search_query))

            all_records = all_records.union(
                Course_Faculty.objects.filter(faculty__name__icontains=search_query))

            all_records = all_records.union(
                Course_Faculty.objects.filter(faculty__email__icontains=search_query))

            all_records = all_records.union(
                Course_Faculty.objects.filter(faculty__department__icontains=search_query))

            all_records = all_records.union(
                Course_Faculty.objects.filter(div__icontains=search_query))
    else:
        all_records = Course_Faculty.objects.all()

    return render(request, 'app/MA_see_all_course_faculty_records_page.html', {'all_records': all_records})


@login_required_for_master_admin
def update_course_faculty_view(request, id):
    if request.method == 'POST':
        pi = Course_Faculty.objects.get(pk=id)
        fm = Update_Course_Faculty_Form(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = Course_Faculty.objects.get(pk=id)
        fm = Update_Course_Faculty_Form(instance=pi)

    return render(request, 'app/MA_update_course_faculty_record_page.html', {'form': fm})


@login_required_for_master_admin
def delete_course_faculty_view(request, id):
    if request.method == 'POST':
        pi_1 = Course_Faculty.objects.get(pk=id)
        pi_1.delete()

    return redirect("all_course_faculty_records_view")


@login_required_for_faculty
def faculty_home_page_view(request, id):
    faculty_info = Faculty.objects.get(pk=id)

    all_course_records = Course_Faculty.objects.all()
    courses_of_this_faculty = []
    for record in all_course_records:
        if record.faculty.id == id:
            courses_of_this_faculty.append(record)

    return render(request, 'app/F_home_page.html', {'personal_info': faculty_info, 'faculty_courses': courses_of_this_faculty})


@login_required_for_faculty
def add_attendance_record_view(request: HttpRequest, course_faculty_record_id):
    user_id = Faculty.objects.get(email=request.user.username).pk
    if request.method == 'POST':
        fm = Attendance_Form(request.POST)
        if fm.is_valid():
            obj = Attendance()

            obj.course_faculty = Course_Faculty.objects.get(
                pk=course_faculty_record_id)

            obj.date = fm.cleaned_data["date"]

            obj.start_time = fm.cleaned_data["start_time"]

            obj.end_time = fm.cleaned_data["end_time"]

            obj.save()

            all_present_students = fm.cleaned_data["total_students"]
            obj.present_students.set(all_present_students)

            all_students = Student.objects.filter(
                branch=obj.course_faculty.course.branch, year=obj.course_faculty.course.year, div=obj.course_faculty.div)
            obj.absent_students.set(
                student for student in all_students if student not in all_present_students)

            return redirect("faculty_home_page_view", id=user_id)
    else:
        helper_1 = Course_Faculty.objects.get(pk=course_faculty_record_id)
        all_records = Student.objects.filter(
            branch=helper_1.course.branch, year=helper_1.course.year, div=helper_1.div)
        fm = Attendance_Form()
        fm.fields['total_students'].queryset = all_records

        return render(request, 'app/F_add_attendance_record_page.html', {'form': fm, 'user_id': user_id})


@login_required_for_master_admin
def all_attendance_records_view(request: HttpRequest):
    if request.method == 'POST':
        search_query = str(request.POST.get('search_area')).strip()

        if not search_query:
            all_records = Attendance.objects.all()
        else:
            all_records = Attendance.objects.filter(
                course_faculty__course__name__icontains=search_query)

            all_records = all_records.union(Attendance.objects.filter(
                course_faculty__course__year__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                course_faculty__course__sem__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                course_faculty__course__branch__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                course_faculty__faculty__name__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                course_faculty__faculty__email__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                course_faculty__faculty__department__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                course_faculty__div__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                date__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                start_time__icontains=search_query))

            all_records = all_records.union(Attendance.objects.filter(
                end_time__icontains=search_query))

    else:
        all_records = Attendance.objects.all()

    return render(request, 'app/MA_see_all_attendance_records_page.html', {'all_records': all_records})


@login_required_for_master_admin
def sem_end_delete_all_attendance_records_view(request):
    Attendance.objects.all().delete()
    return redirect("all_attendance_records_view")


@login_required_for_master_admin
def sem_end_students_attendance_report_view(request: HttpRequest):
    if request.method == 'POST':
        fm = Cumulative_Student_Attendance_Form(request.POST)
        if fm.is_valid():
            course_faculty_instance = fm.cleaned_data["course_faculty"]

            # Step 1 : Creation of dataframe
            data = []
            all_related_student_records = Student.objects.filter(
                branch=course_faculty_instance.course.branch, year=course_faculty_instance.course.year, div=course_faculty_instance.div)

            for student in all_related_student_records:
                helper = {}
                helper["Name"] = student.name
                helper["Email"] = student.email
                helper["MIS"] = student.mis
                helper["Phone Number"] = student.phone_number
                helper["Branch"] = student.branch
                helper["Year"] = student.year
                helper["Div"] = student.div

                all_related_Attendance_records = Attendance.objects.filter(
                    course_faculty=course_faculty_instance)

                helper["Attendance Percentage"] = '0.00'
                total_count = all_related_Attendance_records.count()
                if total_count != 0:
                    helper["Attendance Percentage"] = str(sum(
                        1 for attendance_record in all_related_Attendance_records if student in attendance_record.present_students.all())*100/total_count)

                data.append(helper)

            df = pd.DataFrame(data)

            # Step 2 : DataFrame -> HTML file
            html_file_path = os.path.abspath(
                os.path.join(settings.MEDIA_ROOT, 'temp.html'))
            df.to_html(html_file_path, index=False)

            # Step 3 : HTML file -> PDF File
            pdf_file_path = os.path.abspath(
                os.path.join(settings.MEDIA_ROOT, 'Report.pdf'))
            pdfkit.from_file(html_file_path, pdf_file_path)
            os.remove(html_file_path)

            # Step 4 : Sending Pdf_file
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Report.pdf"'

            # Step 5: Write the PDF to the response
            with open(pdf_file_path, 'rb') as pdf_file:
                response.write(pdf_file.read())
            os.remove(pdf_file_path)

            return response

    else:
        fm = Cumulative_Student_Attendance_Form()

    return render(request, 'app/MA_sem_end_students_attendance_report_page.html', {'form': fm})


@login_required_for_student
def student_home_page_view(request, id):
    student_info = Student.objects.get(pk=id)

    all_course_faculty_records = Course_Faculty.objects.all()
    courses_facultys_of_this_student = []
    for record in all_course_faculty_records:
        if record.course.year == student_info.year and record.course.branch == student_info.branch and record.div == student_info.div:
            courses_facultys_of_this_student.append(record)

    return render(request, 'app/S_home_page.html', {'personal_info': student_info, 'all_records': courses_facultys_of_this_student})


@login_required_for_student
def student_course_faculty_attendance_detailed_view(request: HttpRequest, course_faculty_id):
    student_instance = Student.objects.get(mis=request.user.username)

    helper = Attendance.objects.filter(course_faculty__pk=course_faculty_id)
    total_records = len(helper)

    status_arr = [1 if student_instance in record.present_students.all(
    ) else 0 for record in helper]
    present_percentage = (sum(status_arr) / total_records) * \
        100 if total_records != 0 else 0

    combined_records = zip(helper, status_arr)

    return render(request, 'app/S_see_all_course_faculty_attendance_records_page.html', {'all_records': combined_records, 'present_percentage': present_percentage, 'student_id': student_instance.pk})
