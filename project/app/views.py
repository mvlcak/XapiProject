from django.shortcuts import redirect, render

from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import  CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, authenticate, login, logout

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for'+ user)
            return redirect('login')

    context = {'form':form}
    return render(request, 'app/register.html',context)

def loginPage(request):
    if request.method == 'POST':
        request.POST.get('username')
        request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            messages.info(request, 'Username or password is incorrect')    
    return render(request, 'app/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

def mainPage(request):
    return render(request, 'app/main.html')

def activitiesPage(request):
    return render(request, 'app/activities.html')  

def personsPage(request):
    return render(request, 'app/persons.html')        

def index(request):
    return render(request, 'app/index.html')

def detailPerson(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    return render(request, 'app/detailPerson.html', {'person': person})

def detailActivity(request, activity_id):
    return HttpResponse("You're looking at activity %s." %activity_id)
    