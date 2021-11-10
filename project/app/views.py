from django.shortcuts import redirect, render

from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from operator import itemgetter
from datetime import date
import requests
import json
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
	objectsInteractions=[]
	mysetObjects=set()
	for act in activities:
		mysetObjects.add(act.object)
	for act in mysetObjects:
		objectsInteractions.append([act,Activity.objects.filter(object=act).count()])
	objectsInteractions=sorted(objectsInteractions, key=itemgetter(1))[::-1][:10]
	lastDays=[]
	for act in activities:
		if act.timestamp[:10] == (date.today() - datetime.timedelta(days=7)):
			lastDays.append([(datetime.datetime.now() - datetime.timedelta(days=7)).date(),
							  Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=7)).count()])
		if act.timestamp[:10] == date.today() - datetime.timedelta(days=6):
			lastDays.append([(datetime.datetime.now() - datetime.timedelta(days=6)).date(),
							  Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=6)).count()])
		if act.timestamp[:10] == date.today() - datetime.timedelta(days=5):
			lastDays.append([(datetime.datetime.now() - datetime.timedelta(days=5)).date(),
							  Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=5)).count()])
		if act.timestamp[:10] == date.today() - datetime.timedelta(days=4):
			lastDays.append([(datetime.datetime.now() - datetime.timedelta(days=4)).date(),
							  Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=4)).count()])
		if act.timestamp[:10] == date.today() - datetime.timedelta(days=3):
			lastDays.append([(datetime.datetime.now() - datetime.timedelta(days=3)).date(),
							  Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=3)).count()])
		if act.timestamp[:10] == date.today() - datetime.timedelta(days=2):
			lastDays.append([(datetime.datetime.now() - datetime.timedelta(days=2)).date(),
							  Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=2)).count()])
		if act.timestamp[:10] == date.today() - datetime.timedelta(days=1):		
			lastDays.append([(datetime.datetime.now() - datetime.timedelta(days=1)).date(),
							  Activity.objects.filter(timestamp__contains=datetime.datetime.now() - datetime.timedelta(days=1)).count()])
	(datetime.datetime.now() - datetime.timedelta(days=7)).date()
	return render(request, 'app/main.html',{'activityCount':activityCount,'personCount':personCount,
				  'lastActivities':lastActivities,'personsInteractions':personsInteractions,
				  'activitiesInteractions':activitiesInteractions, 'objectsInteractions':objectsInteractions,
				  'lastDays':lastDays})

@login_required(login_url='loginIn')
def activitiesPage(request):
	activityList=Activity.objects.all()[::-1]
	page = request.GET.get('page', 1)	
	paginator = Paginator(activityList, 20)
	try:
		activityList = paginator.page(page)
	except PageNotAnInteger:
		activityList = paginator.page(1)
	except EmptyPage:
		activityList= paginator.page(paginator.num_pages)
	return render(request, 'app/activities.html', {'activityList':activityList})  

@login_required(login_url='loginIn')
def personsPage(request):
	person_list = Person.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(person_list, 10)
	try:
		persons = paginator.page(page)
	except PageNotAnInteger:
		persons = paginator.page(1)
	except EmptyPage:
		persons= paginator.page(paginator.num_pages)

	return render(request, 'app/persons.html',{'persons':persons})        

@login_required(login_url='loginIn')
def index(request):
    return render(request, 'app/index.html')

@login_required(login_url='loginIn')
def detailPerson(request, person_id):
	person = get_object_or_404(Person, pk=person_id)
	lastActivities=Activity.objects.filter(person=person_id)[::-1][:5]
	activities=Activity.objects.filter(person=person_id).distinct()
	activitiesInteractions=[]
	myset=set()
	for act in activities:
		myset.add(act.verb)
	for act in myset:
		activitiesInteractions.append([act,Activity.objects.filter(verb=act).count()])
	activitiesInteractions=sorted(activitiesInteractions, key=itemgetter(1))[::-1][:10]
	objectsInteractions=[]
	mysetObjects=set()
	for act in activities:
		mysetObjects.add(act.object)
	for act in mysetObjects:
		objectsInteractions.append([act,Activity.objects.filter(object=act).count()])
	objectsInteractions=sorted(objectsInteractions, key=itemgetter(1))[::-1][:10]
	response = requests.get('http://host.docker.internal/webservice/rest/server.php?wstoken=73703163bf6f50182787e0c8ee5c63cd&wsfunction=core_enrol_get_users_courses&userid='+person.id_lms+'&moodlewsrestformat=json')
	courses = json.loads(response.text)
	coursesList=[]
	for course in courses:
		coursesList.append(course['fullname'])
	return render(request, 'app/personDetail.html', {'person': person,'lastActivities':lastActivities,
				  'activitiesInteractions':activitiesInteractions,'objectsInteractions':objectsInteractions,'coursesList':coursesList})

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
			person=Person(id_lms=activity['actor']['account']['name'],person_name=activity['actor']['name'])
			
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

@login_required(login_url='loginIn')
def search_persons(request):
	searched=request.POST.get('name')
	persons=Person.objects.filter(person_name__contains=searched)
	return render(request, 'app/persons.html',{'persons':persons}) 		

@login_required(login_url='loginIn')
def coursesPage(request):
	response = requests.get('http://host.docker.internal/webservice/rest/server.php?wstoken=73703163bf6f50182787e0c8ee5c63cd&wsfunction=core_course_get_courses_by_field&value=&moodlewsrestformat=json')
	text = json.loads(response.text)
	courses_list=[]
	for course in text['courses'] :
			courses_list.append([course['id'],course['fullname']])
	page = request.GET.get('page', 1)
	paginator = Paginator(courses_list, 10)
	try:
		courses = paginator.page(page)
	except PageNotAnInteger:
		courses = paginator.page(1)
	except EmptyPage:
		courses= paginator.page(paginator.num_pages)

	return render(request, 'app/courses.html',{'courses':courses}) 

@login_required(login_url='loginIn')
def detailCourse(request, course_id):
	response = requests.get('http://host.docker.internal/webservice/rest/server.php?wstoken=73703163bf6f50182787e0c8ee5c63cd&wsfunction=core_course_get_courses&options[ids][0]='+str(course_id)+'&moodlewsrestformat=json')
	text = json.loads(response.text)
	course=text[0]['fullname']
	lastActivities=Activity.objects.filter(object=course)[::-1][:5]
	responseEnrolled = requests.get('http://host.docker.internal/webservice/rest/server.php?wstoken=73703163bf6f50182787e0c8ee5c63cd&wsfunction=core_enrol_get_enrolled_users&courseid='+str(course_id)+'&moodlewsrestformat=json')
	textEnrolled = json.loads(responseEnrolled.text)
	persons=Person.objects.all()
	personsInteractions=[]
	df = pd.DataFrame( columns=['person_name', 'interactions'])
	for pers in persons:
		df.append(pers.person_name,Activity.objects.filter(person=pers,object=course).count())
		personsInteractions.append([pers.person_name,Activity.objects.filter(person=pers,object=course).count()])
	
	personsInteractions=sorted(personsInteractions, key=itemgetter(1))[::-1][:5]
	activitiesInteractions=[]
	activities=Activity.objects.distinct()
	myset=set()
	for act in activities:
		myset.add(act.verb)
	for act in myset:
		activitiesInteractions.append([act,Activity.objects.filter(verb=act).count()])
	activitiesInteractions=sorted(activitiesInteractions, key=itemgetter(1))[::-1][:10]
	enrolledPersons=[]
	for pers in textEnrolled:
		enrolledPersons.append(pers['fullname'])
	page = request.GET.get('page', 1)	
	paginator = Paginator(enrolledPersons, 10)
	try:
		persons = paginator.page(page)
	except PageNotAnInteger:
		persons = paginator.page(1)
	except EmptyPage:
		persons= paginator.page(paginator.num_pages)
	return render(request, 'app/courseDetail.html',{'course':course,'persons':persons,'lastActivities':lastActivities
				  ,'personsInteractions':personsInteractions,'activitiesInteractions':activitiesInteractions})	

@login_required(login_url='loginIn')
def search_courses(request):
	searched=request.POST.get('name')
	persons=Person.objects.filter(person_name__contains=searched)
	return render(request, 'app/persons.html',{'persons':persons}) 						  
