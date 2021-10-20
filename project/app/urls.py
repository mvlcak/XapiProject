from django.urls import path

from . import views

urlpatterns = [
    # ex: /app/
    path('', views.index, name='index'),
    # ex: /activity/id/
    path('activity/<int:activity_id>/', views.detailActivity, name='detailActivity'),
     # ex: /person/id/
    path('person/<int:person_id>/', views.detailPerson, name='detailPerson'),
    # ex: /register/
    path('register', views.registerPage, name='registerPage'),
    
]