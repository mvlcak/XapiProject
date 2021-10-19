from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detailPerson(request, person_id):
    return HttpResponse("You're looking at person %s." %person_id)

def detailActivity(request, activity_id):
    return HttpResponse("You're looking at activity %s." %activity_id)
    