from django.shortcuts import get_object_or_404, redirect, render
from .models import Profiles
from userauths.models import User
from .forms import EditProfileForm, UserRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profiles, user=user)
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Hurray, your account was created and you are now logged in!')
                return redirect('index')
            else:
                messages.error(request, 'Authentication failed. Please try again.')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        form = UserRegisterForm()

    return render(request, 'sign-up.html', {'form': form})

def signout(request):
    logout(request)
    messages.success(request, 'you are now signed out')
    return redirect('sign-in')