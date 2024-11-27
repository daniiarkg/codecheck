from django.shortcuts import render, HttpResponse, redirect
from .forms import RegistrationForm
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def registration(request):
    if request.user.is_authenticated:
        logout(request) 
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            get_data = form.cleaned_data
            my_group = Group.objects.get(name='Обычный')
            new_user = User.objects.create(username=get_data['login'], password=make_password(get_data['password']), is_staff=True)
            new_user.save()
            my_group.user_set.add(new_user)
            new_citizen = Coder(fio=get_data['fio'], user=new_user)
            new_citizen.save()
            user = authenticate(request, username=get_data['login'], password=get_data['password'])
            print(user)
            if user is not None:
                login(request, user)
                return redirect('admin:index')
            else:
                return HttpResponse('UNEXPECTED ERROR')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html',{'form':form})