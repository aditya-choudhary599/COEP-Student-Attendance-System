from .models import *
from django.http import HttpResponseForbidden, HttpRequest
from django.shortcuts import redirect


def decorator_for_website_landing_page(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request)
        else:
            custom_user_profile_instance = CustomUserProfile.objects.get(
                user=request.user)

            if custom_user_profile_instance.designation == 'Master Admin':
                return redirect('master_admin_home_page_view')

            elif custom_user_profile_instance.designation == 'Faculty':
                faculty_instance = Faculty.objects.get(
                    email=request.user.username)
                return redirect('faculty_home_page_view', id=faculty_instance.pk)

            elif custom_user_profile_instance.designation == 'Student':
                student_instance = Student.objects.get(
                    mis=request.user.username)
                return redirect('student_home_page_view', id=student_instance.pk)

            else:
                return view_func(request)

    return wrapped_view


def decorator_for_password_change_page(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You don't have permission to access this page.")
        else:
            return view_func(request)

    return wrapped_view


def login_required_for_master_admin(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("landing_page_view")

        else:
            custom_user_profile_instance = CustomUserProfile.objects.get(
                user=request.user)

            if custom_user_profile_instance.designation == 'Master Admin':
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponseForbidden("You don't have permission to access this page.")

    return wrapped_view


def login_required_for_faculty(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("landing_page_view")

        else:
            custom_user_profile_instance = CustomUserProfile.objects.get(
                user=request.user)

            if custom_user_profile_instance.designation == 'Faculty':
                requested_faculty_id = kwargs.get('id')
                curr_faculty_obj = Faculty.objects.get(
                    email=request.user.username)
                if curr_faculty_obj.id == requested_faculty_id:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("Please mind your own buisness instead of looking into others!")

            else:
                return HttpResponseForbidden("You don't have permission to access this page.")

    return wrapped_view


def login_required_for_student(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("landing_page_view")

        else:
            custom_user_profile_instance = CustomUserProfile.objects.get(
                user=request.user)

            if custom_user_profile_instance.designation == 'Student':
                requested_student_id = kwargs.get('id')
                curr_student_obj = Student.objects.get(
                    mis=request.user.username)
                if curr_student_obj.id == requested_student_id:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("Please mind your own buisness instead of looking into others!")

            else:
                return HttpResponseForbidden("You don't have permission to access this page.")

    return wrapped_view
