from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import GalleryImage
from .models import Signup
from .forms import ContactForm
from .models import Contact
from .models import TeamMember
from .models import Event
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

        # Check if username or email already exists
        if Signup.objects.filter(username=username).exists():
            messages.error(request, 'The username is already taken, please choose a different username.')
        elif Signup.objects.filter(email=email).exists():
            messages.error(request, 'The email is already registered, please use a different email.')
        elif len(password) > 15:
            messages.error(request, 'Password must be at most 15 characters long.')
        else:
            # Hash the password and create the user
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
        form = EventForm(request.POST)
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