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
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests,json
from operator import itemgetter
import datetime

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
	activityCount=Activity.objects.count()
	personCount=Person.objects.count()
	lastActivities=Activity.objects.all()[::-1][:5]
	persons=Person.objects.all()
	personsInteractions=[]
	for pers in persons:
		personsInteractions.append([pers.person_name,Activity.objects.filter(person=pers).count()])
	personsInteractions=sorted(personsInteractions, key=itemgetter(1))[::-1][:5]
	activities=Activity.objects.distinct()
	activitiesInteractions=[]
	myset=set()
	for act in activities:
		myset.add(act.verb)
	for act in myset:
		activitiesInteractions.append([act,Activity.objects.filter(verb=act).count()])
	activitiesInteractions=sorted(activitiesInteractions, key=itemgetter(1))[::-1][:10]
	last7=[]
	for act in activities:
		if act.timestamp[:9] == (datetime.datetime.now() - datetime.timedelta(days=7)).date():
			last7.append([(datetime.datetime.now() - datetime.timedelta(days=7)).date(),
			Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
		if act.timestamp[:9] == (datetime.datetime.now() - datetime.timedelta(days=6)).date():
			last7.append([(datetime.datetime.now() - datetime.timedelta(days=6)).date(),
			Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
		if act.timestamp[:9] == (datetime.datetime.now() - datetime.timedelta(days=5)).date():
			last7.append([(datetime.datetime.now() - datetime.timedelta(days=5)).date(),
			Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
		if act.timestamp[:9] == (datetime.datetime.now() - datetime.timedelta(days=4)).date():
			last7.append([(datetime.datetime.now() - datetime.timedelta(days=4)).date(),
			Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
		if act.timestamp[:9] == (datetime.datetime.now() - datetime.timedelta(days=3)).date():
			last7.append([(datetime.datetime.now() - datetime.timedelta(days=3)).date(),
			Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
		if act.timestamp[:9] == (datetime.datetime.now() - datetime.timedelta(days=2)).date():
			last7.append([(datetime.datetime.now() - datetime.timedelta(days=2)).date(),
			Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
		if act.timestamp[:9] == (datetime.datetime.now() - datetime.timedelta(days=1)).date():		
			last7.append([(datetime.datetime.now() - datetime.timedelta(days=1)).date(),
			Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
	(datetime.datetime.now() - datetime.timedelta(days=7)).date()
	return render(request, 'app/main.html',{'activityCount':activityCount,'personCount':personCount,
	'lastActivities':lastActivities,
	'personsInteractions':personsInteractions,'activitiesInteractions':activitiesInteractions,'last7':last7})

@login_required(login_url='loginIn')
def activitiesPage(request):
	activityList=Activity.objects.all()[::-1]
	return render(request, 'app/activities.html', {'activityList':activityList})  

@login_required(login_url='loginIn')
def personsPage(request):
	persons=Person.objects.all
	return render(request, 'app/persons.html',{'persons':persons})        

@login_required(login_url='loginIn')
def index(request):
    return render(request, 'app/index.html')

@login_required(login_url='loginIn')
def detailPerson(request, person_id):
	lastActivities=Activity.objects.filter(person=person_id)[::-1][:5]
    
	person = get_object_or_404(Person, pk=person_id)
	return render(request, 'app/personDetail.html', {'person': person,'lastActivities':lastActivities})

@login_required(login_url='loginIn')
def detailActivity(request, activity_id):
    return HttpResponse("You're looking at activity %s." %activity_id)

def loginIn(request):
	username = request.POST.get('username')
	password =request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('main')
	else:
		return redirect('loginPage')

def register(request):
	username = request.POST.get('username')
	password =request.POST.get('password1')
	email=request.POST.get('email')		
	user = User.objects.create_user(username, email, password)
	user.save
	return redirect('loginPage')

@login_required(login_url='loginIn')
def loadDb(request):
	response = requests.get('https://watershedlrs.com/api/organizations/15941/query/export?type=json',
                            auth=('a8970a17258465', '1acab410733815'))
	text = json.loads(response.text)
	for activity in text:
		if not Person.objects.filter(person_name=activity['actor']['name']):
			person=Person(person_name=activity['actor']['name'])
			person.save()
		else: 
			person=Person.objects.get(person_name=activity['actor']['name'])
		act=Activity(person=person,
		actor=activity['actor']['name'],
		verb=activity['verb']['display']['en'],
		object=activity['object']['definition']['name']['en'],
		pub_date=timezone.now(),
		timestamp =activity['timestamp'],
		id_activity=activity['id'])	
		activities=Activity.objects.filter(id_activity=activity['id'])
		if not activities:
			act.save()
	return redirect('main')		
		
