from email.policy import default
from lib2to3.pgen2 import token
import re
import uuid
from django.forms import PasswordInput
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

from django.conf import settings
from django.core.mail import send_mail


def home(request):
    return render(request, 'home.html')


def login_attempt(request):
    return render(request, 'login.html')

def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username, email=email).first():
                messages.success(request, 'Username is taken')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken')
                return redirect('/register')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request, 'register.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

def send_mail_after_registration(token, email):
    subject = 'Your Accounts Need to be verified.'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
