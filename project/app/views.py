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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests,json


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('main')
	else:
		return render(request, 'app/register.html')


def loginPage(request):
	return render(request, 'app/login.html')

def logoutUser(request):
	logout(request)
	return redirect('loginPage')

@login_required(login_url='loginIn')
def mainPage(request):
    return render(request, 'app/main.html')

@login_required(login_url='loginIn')
def activitiesPage(request):
	response = requests.get('https://watershedlrs.com/api/organizations/15941/query/export?type=json',
                            auth=('a8970a17258465', '1acab410733815'))
	text = json.loads(response.text)
	activityList=[]
	for activity in text:
		list=[]
		list.append(activity['actor']['name'])
		list.append(activity['verb']['display']['en'])
		list.append(activity['object']['definition']['name']['en'])
		list.append(activity['timestamp'])
		list.append(activity['id'])
		activityList.append(list)
	return render(request, 'app/activities.html', {'activityList':activityList})  

@login_required(login_url='loginIn')
def personsPage(request):
    return render(request, 'app/persons.html')        

def index(request):
    return render(request, 'app/index.html')

@login_required(login_url='loginIn')
def detailPerson(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    return render(request, 'app/detailPerson.html', {'person': person})

@login_required(login_url='loginIn')
def detailActivity(request, activity_id):
    return HttpResponse("You're looking at activity %s." %activity_id)

def loginIn(request):
	username = request.POST.get('username')
	password =request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return render(request, 'app/main.html')
	else:
		return redirect('loginPage')

def register(request):
	username = request.POST.get('username')
	password =request.POST.get('password1')
	email=request.POST.get('email')		
	user = User.objects.create_user(username, email, password)
	user.save
	return redirect('loginPage')