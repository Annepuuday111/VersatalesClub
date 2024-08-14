from django.urls import path
from . import views

urlpatterns = [
    # Home and General Pages
    path('', views.index, name='index'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('home/', views.home, name='home'),
    path('corehome/', views.corehome, name='corehome'),
    path('about/', views.about, name='about'),
    path('knowmore/', views.knowmore, name='knowmore'),
    path('contact/', views.contact, name='contact'),

    # Authentication and User Management
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

    # Events Management
    path('addevent/', views.addevent, name='addevent'),
    path('coreaddevent/', views.coreaddevent, name='coreaddevent'),
    path('bulkupload/', views.bulkupload, name='bulkupload'),
    path('viewevents/', views.viewevents, name='viewevents'),
    path('editevent/<int:event_id>/', views.editevent, name='editevent'),
    path('coreeditevent/<int:event_id>/', views.coreeditevent, name='coreeditevent'),
    path('vieweventlist/', views.vieweventlist, name='vieweventlist'),
    path('corevieweventlist/', views.corevieweventlist, name='corevieweventlist'),
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
    path('editteammember/<int:id>/', views.editteammember, name='editteammember'),
    path('addmember/', views.addmember, name='addmember'),
    path('editmember/<int:id>/', views.editmember, name='editmember'),
    path('bulkteamupload/', views.bulkteamupload, name='bulkteamupload'),
    path('bulkmemberupload/', views.bulkmemberupload, name='bulkmemberupload'),
    path('viewteam/', views.viewteam, name='viewteam'),
    path('coreviewteam/', views.coreviewteam, name='coreviewteam'),
    path('downloadteammembers/', views.downloadteammembers, name='downloadteammembers'),
    path('downloadmembers/', views.downloadmembers, name='downloadmembers'),
    path('deleteteammember/<int:member_id>/', views.deleteteammember, name='deleteteammember'),
    path('deletemember/<int:member_id>/', views.deletemember, name='deletemember'),

    # Stories Management
    path('addstory/', views.addstory, name='addstory'),
    path('coreaddstory/', views.coreaddstory, name='coreaddstory'),
    path('viewstory/', views.viewstory, name='viewstory'),
    path('userstory/', views.userstory, name='userstory'),
    path('coreviewstory/', views.coreviewstory, name='coreviewstory'),
    path('updatestorystatus/<int:story_id>/', views.updatestorystatus, name='updatestorystatus'),

    # Queries
    path('viewqueries/', views.viewqueries, name='viewqueries'),
    path('deletequery/<int:query_id>/', views.deletequery, name='deletequery'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('users/', views.users, name='users'),
    path('update-user-status/', views.update_user_status, name='update_user_status'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('updatemarquee/', views.updatemarquee, name='updatemarquee'),
]
