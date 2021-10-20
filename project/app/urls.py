from django.urls import path

from . import views

urlpatterns = [
    # ex: /app/
    path('', views.index, name='index'),
    # ex: /activity/id/
    path('activity/<int:activity_id>/', views.detailActivity, name='detailActivity'),
     # ex: /person/id/
    path('person/<int:person_id>/', views.detailPerson, name='detailPerson'),
    
    path('register', views.registerPage, name='register'),

    path('login', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('main', views.mainPage, name='main'),
    path('persons', views.personsPage, name='persons'),
    path('activities', views.activitiesPage, name='activities'),
    
]