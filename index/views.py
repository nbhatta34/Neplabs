from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, UserAdminCreationForm
from .auth import unauthenticated_user
import uuid
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
def index_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user_obj = User.objects.filter(email = email).first()

            profile_obj = Profile.objects.filter(user = user_obj).first()

            if not profile_obj.is_verified:
                messages.warning(request, 'Account is not verified. Please check your email.')
                return redirect('/')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/userDash')

            else:
                messages.add_message(
                    request, messages.ERROR, 'Invalid username or password')
                return render(request, 'index/index.html', {'form': form})
    context = {
        'form': LoginForm,
        "activate_login": 'active'
    }
    return render(request, 'index/index.html', context)


def user_dashboard(request):
    context = {}
    return render(request, 'index/userDash.html', context)


def user_sign_up(request):
    if request.method == "POST":
        email = request.POST.get('email')
        form = UserAdminCreationForm(request.POST)
        if form.is_valid:
            user = form.save()
            us_id = user.id
            user_id = User.objects.get(id=us_id)
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_id , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/token')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error in registering User')
            return render(request, 'accounts/userSignUp.html', {'form': form})
    context = {
        'form': UserAdminCreationForm,
        'activate_signup': 'active'
    }
    return render(request, 'index/userSignUp.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')


def send_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def token_send(request):
    return render(request, 'index/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.info(request, 'Your account is already been verified.')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Congratulations your account has been verified.')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
