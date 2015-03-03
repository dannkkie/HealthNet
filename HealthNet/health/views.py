from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
import datetime
from . import sanitizer
from .models import *


@login_required
def index(request):
    return render(request, 'index.html', {"user": request.user,
                                          "navbar":"home"})


def login_view(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('health:index')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('health:index')

@login_required
def prescriptions(request):
    return render(request, 'prescriptions.html', {"user": request.user,
                                                  "navbar":"prescriptions"})

signup_context = {
    "year_range": range(1900, datetime.date.today().year + 1),
    "day_range": range(1, 32),
    "months": [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]
}


def signup(request):
    if request.POST:
        password = request.POST.get("password")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")

        email = request.POST.get("email")
        phone = sanitizer.sanitize_phone(request.POST.get("phone"))
        month = int(request.POST.get("month"))
        day = int(request.POST.get("day"))
        year = int(request.POST.get("year"))
        date = datetime.date(month=month, day=day, year=year)
        user = User.objects.create_user(email, email=email, password=password,
            date_of_birth=date, phone_number=phone, first_name=firstname,
                last_name=lastname)
        if user is not None:
            policy = request.POST.get("policy")
            company = request.POST.get("company")
            insurance = Insurance.objects.create(policy_number=policy,
                company=company, patient=user)
            if insurance is not None:
                return redirect('health:index')

    return render(request, 'signup.html', signup_context)


@login_required
def schedule(request):
    return render(request, 'schedule.html', {"user": request.user,
                                             "navbar":"schedule"})