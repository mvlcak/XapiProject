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
import pandas as pd
from sklearn.cluster import KMeans



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
	
	return render(request, 'app/main.html',{'activityCount':activityCount,'personCount':personCount,
				  'lastActivities':lastActivities,'personsInteractions':personsInteractions,
				  'activitiesInteractions':activitiesInteractions, 'objectsInteractions':objectsInteractions,})

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
		activitiesInteractions.append([act,Activity.objects.filter(verb=act).filter(person=person_id).count()])
	activitiesInteractions=sorted(activitiesInteractions, key=itemgetter(1))[::-1][:10]
	objectsInteractions=[]
	mysetObjects=set()
	for act in activities:
		mysetObjects.add(act.object)
	for act in mysetObjects:
		objectsInteractions.append([act,Activity.objects.filter(object=act).filter(person=person_id).count()])
	objectsInteractions=sorted(objectsInteractions, key=itemgetter(1))[::-1][:10]
	response = requests.get('http://host.docker.internal/webservice/rest/server.php?wstoken=73703163bf6f50182787e0c8ee5c63cd&wsfunction=core_enrol_get_users_courses&userid='+person.id_lms+'&moodlewsrestformat=json')
	courses = json.loads(response.text)
	coursesList=[]
	for course in courses:
		coursesList.append(course['fullname'])
	lastDays=[]
	for i in range(6,0,-1):
		time=datetime.datetime.now() - datetime.timedelta(days=i)
		lastDays.append(["-"+str(i)+" days",Activity.objects.filter(timestamp__contains=time.strftime('%Y-%m-%d')).filter(person=person_id).count()])
	time=time=datetime.datetime.now()
	lastDays.append(["today",Activity.objects.filter(timestamp__contains=time.strftime('%Y-%m-%d')).filter(person=person_id).count()])
	response2 = requests.get('http://host.docker.internal/webservice/rest/server.php?wstoken=73703163bf6f50182787e0c8ee5c63cd&wsfunction=gradereport_overview_get_course_grades&userid='+str(person.id_lms)+'&moodlewsrestformat=json')
	text2 = json.loads(response2.text)
	gradeList=[]
	try:
		for grade in text2['grades']:
			response3 = requests.get('http://host.docker.internal/webservice/rest/server.php?wstoken=73703163bf6f50182787e0c8ee5c63cd&wsfunction=core_course_get_courses&options[ids][0]='+str(grade['courseid'])+'&moodlewsrestformat=json')			
			text3 = json.loads(response3.text)
			gradeList.append([text3[0]['fullname'],grade['grade']])	
	except:
		gradeList=0

					
	return render(request, 'app/personDetail.html', {'person': person,'lastActivities':lastActivities,
				  'activitiesInteractions':activitiesInteractions,'objectsInteractions':objectsInteractions,'coursesList':coursesList,'lastDays':lastDays,
				'gradeList':gradeList})

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
def search_persons(request):
	searched=request.POST.get('name')
	persons=Person.objects.filter(person_name__icontains=searched)
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
	enrolledPersons=[]
	
	for pers in textEnrolled:
		enrolledPersons.append(pers['fullname'])
	
	df=pd.DataFrame(columns=['name', 'interactions'])
	personsInteractions=[]
	
	for pers in enrolledPersons:
		person=Person(person_name=pers)
		df=df.append({'name':pers,'interactions':Activity.objects.filter(actor=pers).filter(object=course).count()}, ignore_index=True)
		personsInteractions.append([pers,Activity.objects.filter(actor=pers).filter(object=course).count()])
	if len(df.index)>5:
		X = df[[ 'interactions']]
		kmeans = KMeans(n_clusters=5).fit(X)
		clusteredPersons=[]
		i=0
		for person in kmeans.labels_:
			clusteredPersons.append([df.loc[i,'name'],person+1])
			i=i+1
	else:
		clusteredPersons=0
	personsInteractions=sorted(personsInteractions, key=itemgetter(1))[::-1][:5]
	activitiesInteractions=[]
	activities=Activity.objects.filter(object=course).distinct()
	myset=set()
	for act in activities:
		myset.add(act.verb)
	for act in myset:
		activitiesInteractions.append([act,Activity.objects.filter(verb=act).filter(object=course).count()])
	activitiesInteractions=sorted(activitiesInteractions, key=itemgetter(1))[::-1][:10]
	lastDays=[]
	for i in range(6,0,-1):
		time=datetime.datetime.now() - datetime.timedelta(days=i)
		lastDays.append(["-"+str(i)+" days",Activity.objects.filter(timestamp__contains=time.strftime('%Y-%m-%d')).filter(object=course).count()])
	lastDays.append(["today",Activity.objects.filter(timestamp__contains=time.strftime('%Y-%m-%d')).filter(object=course).count()])
	
	return render(request, 'app/courseDetail.html',{'course':course,'persons':persons,'lastActivities':lastActivities,'enrolledPersons':enrolledPersons
				  ,'personsInteractions':personsInteractions,'activitiesInteractions':activitiesInteractions,'clusteredPersons':clusteredPersons
				  ,'lastDays':lastDays})	

@login_required(login_url='loginIn')
def search_courses(request):
	searched=request.POST.get('name')
	persons=Person.objects.filter(person_name__contains=searched)
	return render(request, 'app/persons.html',{'persons':persons}) 						  
