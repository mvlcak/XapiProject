from django.urls import path

from . import views

urlpatterns = [
    # ex: /app/
    path('', views.index, name='index'),
    # ex: /activity/5/
    path('<int:activity_id>/', views.detailActivity, name='detail'),
     # ex: /person/5/
    path('<int:person_id>/', views.detailPerson, name='detail'),
    
]