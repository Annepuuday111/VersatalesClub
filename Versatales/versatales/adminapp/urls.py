from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('knowmore/', views.knowmore, name='knowmore'),
    path('contact/', views.contact, name='contact'),
    path('viewqueries/', views.viewqueries, name='viewqueries'),
    path('gallery/', views.gallery, name='gallery'),
    path('teammembers/', views.teammembers, name='teammembers'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('addevent/', views.addevent, name='addevent'),
    path('viewevents/', views.viewevents, name='viewevents'),
    path('addgallery/', views.addgallery, name='addgallery'),
    path('addteam/', views.addteam, name='addteam'),
]
