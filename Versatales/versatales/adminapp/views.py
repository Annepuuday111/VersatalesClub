from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse
from .models import GalleryImage
from .models import Signup
from .forms import ContactForm
from .models import Contact
from .models import TeamMember
from .models import Event
from .models import Story
from .forms import StoryForm
from .forms import EventForm
from .forms import GalleryImageForm
from .forms import TeamMemberForm

# Define fixed admin username and password
FIXED_ADMIN_USERNAME = 'admin'
FIXED_ADMIN_PASSWORD = 'admin@123'

def index(request):
    return render(request, "index.html")

def adminhome(request):
    if request.session.get('is_admin'):
        return render(request, "adminhome.html")
    return redirect('login')

def home(request):
    if request.session.get('is_admin') is not None:
        return render(request, "home.html")
    return redirect('login')

def about(request):
    return render(request, 'about.html')

def knowmore(request):
    return render(request, 'knowmore.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def viewqueries(request):
    submissions = Contact.objects.all()
    return render(request, 'viewqueries.html', {'submissions': submissions})

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})

def teammembers(request):
    team_members = TeamMember.objects.all()
    return render(request, 'teammembers.html', {'team_members': team_members})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check fixed admin credentials
        if username == FIXED_ADMIN_USERNAME and password == FIXED_ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return redirect('adminhome')

        # Check for user in Signup model
        try:
            user = Signup.objects.get(username=username)
            if check_password(password, user.password):
                request.session['is_admin'] = False
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
        except Signup.DoesNotExist:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Signup.objects.filter(username=username).exists():
            messages.error(request, 'The username is already taken, please choose a different username.')
        elif Signup.objects.filter(email=email).exists():
            messages.error(request, 'The email is already registered, please use a different email.')
        elif len(password) > 15:
            messages.error(request, 'Password must be at most 15 characters long.')
        else:

            hashed_password = make_password(password)
            Signup.objects.create(name=name, email=email, username=username, password=hashed_password)
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')

    return render(request, "signup.html")

def logout(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def addevent(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('addevent')
    else:
        form = EventForm()

    return render(request, 'addevent.html', {'form': form})

def viewevents(request):
    events = Event.objects.all()
    return render(request, 'viewevents.html', {'events': events})

def addgallery(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image added successfully!')
            form = GalleryImageForm()
    else:
        form = GalleryImageForm()

    return render(request, 'addgallery.html', {
        'form': form
    })

def addteam(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('addteam')
    else:
        form = TeamMemberForm()

    return render(request, 'addteam.html', {
        'form': form
    })

def addstory(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Story added successfully!')
            form = StoryForm()
    else:
        form = StoryForm()

    return render(request, 'addstory.html', {'form': form})

def viewstory(request):
    accepted_stories = Story.objects.filter(status='accepted')
    return render(request, 'viewstory.html', {'stories': accepted_stories})
def userstory(request):
    stories = Story.objects.all()
    return render(request, 'userstory.html', {'stories': stories})

def updatestorystatus(request, story_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        if status not in ['accepted', 'rejected']:
            return JsonResponse({'message': 'Invalid status.'}, status=400)

        story = get_object_or_404(Story, id=story_id)
        if status == 'rejected':
            story.delete()
            return JsonResponse({'message': 'Story rejected and deleted successfully!'})

        story.status = status
        story.save()
        return JsonResponse({'message': 'Story status updated successfully!'})

    return JsonResponse({'message': 'Invalid request.'}, status=400)

def vieweventlist(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'vieweventlist.html', {'events': events})

def deleteevent(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully'}, status=204)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
def viewteam(request):
    team_members = TeamMember.objects.all()
    return render(request, 'viewteam.html', {'team_members': team_members})

def deleteteammember(request, member_id):
    if request.method == 'POST':
        try:
            team_member = TeamMember.objects.get(pk=member_id)
            team_member.delete()
            return JsonResponse({'message': 'Team member deleted successfully'}, status=204)
        except TeamMember.DoesNotExist:
            return JsonResponse({'error': 'Team member not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def viewgallery(request):
    gallery_images = GalleryImage.objects.all()
    return render(request, 'viewgallery.html', {'gallery_images': gallery_images})

def deletegalleryimage(request, image_id):
    if request.method == 'POST':
        try:
            image = GalleryImage.objects.get(pk=image_id)
            image.delete()
            return JsonResponse({'message': 'Gallery image deleted successfully'}, status=204)
        except GalleryImage.DoesNotExist:
            return JsonResponse({'error': 'Gallery image not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

