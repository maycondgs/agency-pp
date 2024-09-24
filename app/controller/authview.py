from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from app.forms import CustomUserForm

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully!")
            return redirect('login')

    context = {'form': form}
    return render(request, "auth/register.html", context=context)

def loginview(request):
    if request.user.is_authenticated:
        messages.warning(request, "You Logged in")
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passw = request.POST.get('password')

            user = authenticate(request, username=name, password=passw)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid Credentials")
                return redirect('login')

        return render(request, "auth/login.html")
    
def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out")
    return redirect('/')
    