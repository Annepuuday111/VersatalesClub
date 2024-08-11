from django.urls import path
from . import views

urlpatterns = [
    # Home and General Pages
    path('', views.index, name='index'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('knowmore/', views.knowmore, name='knowmore'),
    path('contact/', views.contact, name='contact'),

    # Authentication and User Management
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

    # Events Management
    path('addevent/', views.addevent, name='addevent'),
    path('bulkupload/', views.bulkupload, name='bulkupload'),
    path('viewevents/', views.viewevents, name='viewevents'),
    path('vieweventlist/', views.vieweventlist, name='vieweventlist'),
    path('downloadevents/', views.downloadevents, name='downloadevents'),
    path('deleteevent/<int:event_id>/', views.deleteevent, name='deleteevent'),

    # Gallery Management
    path('gallery/', views.gallery, name='gallery'),
    path('addgallery/', views.addgallery, name='addgallery'),
    path('viewgallery/', views.viewgallery, name='viewgallery'),
    path('deletegalleryimage/<int:image_id>/', views.deletegalleryimage, name='deletegalleryimage'),

    # Team Management
    path('teammembers/', views.teammembers, name='teammembers'),
    path('addteam/', views.addteam, name='addteam'),
    path('addmember/', views.addmember, name='addmember'),
    path('bulkteamupload/', views.bulkteamupload, name='bulkteamupload'),
    path('bulkmemberupload/', views.bulkmemberupload, name='bulkmemberupload'),
    path('viewteam/', views.viewteam, name='viewteam'),
    path('downloadteammembers/', views.downloadteammembers, name='downloadteammembers'),
    path('downloadmembers/', views.downloadmembers, name='downloadmembers'),
    path('deleteteammember/<int:member_id>/', views.deleteteammember, name='deleteteammember'),
    path('deletemember/<int:member_id>/', views.deletemember, name='deletemember'),

    # Stories Management
    path('addstory/', views.addstory, name='addstory'),
    path('viewstory/', views.viewstory, name='viewstory'),
    path('userstory/', views.userstory, name='userstory'),
    path('updatestorystatus/<int:story_id>/', views.updatestorystatus, name='updatestorystatus'),

    # Queries
    path('viewqueries/', views.viewqueries, name='viewqueries'),
    path('deletequery/<int:query_id>/', views.deletequery, name='deletequery'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('updatemarquee/', views.updatemarquee, name='updatemarquee'),
]
