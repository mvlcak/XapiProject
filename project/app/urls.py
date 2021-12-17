from django.urls import path

from . import views

urlpatterns = [
    # ex: /app/
    path('', views.mainPage, name='main'),
    # ex: /activity/id/
    path('activity/<int:activity_id>/', views.detailActivity, name='detailActivity'),
     # ex: /person/id/
    path('person/<int:person_id>/', views.detailPerson, name='detailPerson'),
    path('course/<int:course_id>/', views.detailCourse, name='detailCourse'),

    path('registerPage', views.registerPage, name='registerPage'),
    path('register', views.register, name='register'),
    path('search_persons', views.search_persons, name='search_persons'),
    path('search_courses', views.search_courses, name='search_courses'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name="logout"),
    path('main', views.mainPage, name='main'),
    path('persons', views.personsPage, name='persons'),
    path('courses', views.coursesPage, name='courses'),
    path('activities', views.activitiesPage, name='activities'),
    path('loginIn', views.loginIn, name='loginIn'),
   

    
]