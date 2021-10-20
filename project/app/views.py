from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import  CreateUserForm

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'app/register.html',context)

def index(request):
    return render(request, 'app/index.html')

def detailPerson(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    return render(request, 'app/detailPerson.html', {'person': person})

def detailActivity(request, activity_id):
    return HttpResponse("You're looking at activity %s." %activity_id)
    