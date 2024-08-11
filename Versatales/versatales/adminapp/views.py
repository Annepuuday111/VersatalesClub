from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import pandas as pd
import xlwt
from datetime import datetime
from .models import GalleryImage
from .models import Signup
from .forms import ContactForm
from .models import Contact
from .models import TeamMember
from .models import Member
from .models import Event
from .models import Story
from .forms import StoryForm
from .forms import EventForm
from .forms import GalleryImageForm
from .forms import TeamMemberForm
from .forms import MemberForm
from .models import MarqueeContent

# Define fixed admin username and password
FIXED_ADMIN_USERNAME = 'admin'
FIXED_ADMIN_PASSWORD = 'admin@123'

def index(request):
    marquee_content = MarqueeContent.objects.first()
    return render(request, 'index.html', {'marquee_content': marquee_content})

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

def deletequery(request, query_id):
    if request.method == 'POST':
        query = get_object_or_404(Contact, pk=query_id)
        query.delete()
        return JsonResponse({'message': 'Query deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def chatbot(request):
    return render(request, 'chatbot.html')

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

def bulkupload(request):
    if request.method == 'POST' and request.FILES.get('event_file'):
        event_file = request.FILES['event_file']
        try:
            df = pd.read_excel(event_file)
            for _, row in df.iterrows():
                try:
                    event_date = pd.to_datetime(row['Date'], errors='coerce')
                    if pd.isna(event_date):
                        event_date = None

                    Event.objects.create(
                        title=row['Title'],
                        description=row['Description'],
                        date=event_date,
                        poster=None,
                        location=row.get('Location', '')
                    )
                except Exception as e:
                    messages.error(request, f'Error with row: {str(e)}')
                    continue

            messages.success(request, 'Events were uploaded successfully!')
        except Exception as e:
            messages.error(request, f'Error uploading events: {str(e)}')

        return redirect('addevent')

    return render(request, 'addevent.html')

def viewevents(request):
    events = Event.objects.all()
    return render(request, 'viewevents.html', {'events': events})

def downloadevents(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="events.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Events')

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Title', 'Date', 'Poster', 'Location', 'Description']

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], font_style)

    rows = Event.objects.all().values_list('title', 'date', 'poster', 'location', 'description')

    font_style = xlwt.XFStyle()
    for row_num, row in enumerate(rows, start=1):
        for col_num, value in enumerate(row):
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d')
            ws.write(row_num, col_num, value, font_style)

    wb.save(response)
    return response

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

    return render(request, 'addteam.html', {'form': form})

def bulkteamupload(request):
    if request.method == 'POST':
        if 'team_file' in request.FILES:
            file = request.FILES['team_file']

            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                try:
                    df = pd.read_excel(file)

                    print(df.columns)

                    for _, row in df.iterrows():
                        TeamMember.objects.create(
                            name=row.get('name', ''),
                            position=row.get('position', ''),
                            email=row.get('email', ''),
                            phone=row.get('phone', ''),
                            profile_picture=row.get('profile_picture', None),
                            bio=row.get('bio', '')
                        )

                    messages.success(request, 'Team members uploaded successfully!')
                    return redirect('addteam')
                except Exception as e:
                    messages.error(request, f'Error processing file: {e}')
            else:
                messages.error(request, 'Invalid file format. Please upload an Excel file.')

    return render(request, 'addteam.html')

def downloadteammembers(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="team_members.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Team Members')

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Position', 'Email', 'Bio', 'Profile Picture']

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], font_style)

    rows = TeamMember.objects.all().values_list('name', 'position', 'email', 'bio', 'profile_picture')

    font_style = xlwt.XFStyle()
    for row_num, row in enumerate(rows, start=1):
        for col_num, value in enumerate(row):
            if col_num == 4 and isinstance(value, str):
                value = value if value else 'No Picture'
            ws.write(row_num, col_num, value, font_style)

    wb.save(response)
    return response

def addmember(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('addmember')
    else:
        form = MemberForm()

    return render(request, 'addmember.html', {'form': form})

def bulkmemberupload(request):
    if request.method == 'POST':
        if 'team_file' in request.FILES:
            file = request.FILES['team_file']

            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                try:
                    df = pd.read_excel(file)

                    print(df.columns)

                    for _, row in df.iterrows():
                        Member.objects.create(
                            name=row.get('name', ''),
                            position=row.get('position', ''),
                            email=row.get('email', ''),
                            phone=row.get('phone', ''),
                            profile_picture=row.get('profile_picture', None),
                            bio=row.get('bio', '')
                        )

                    messages.success(request, 'Team members uploaded successfully!')
                    return redirect('addmember')
                except Exception as e:
                    messages.error(request, f'Error processing file: {e}')
            else:
                messages.error(request, 'Invalid file format. Please upload an Excel file.')

    return render(request, 'addmember.html')

def downloadmembers(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="members.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Members')

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Position', 'Email', 'Bio', 'Profile Picture']

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], font_style)

    rows = Member.objects.all().values_list('name', 'position', 'email', 'bio', 'profile_picture')

    font_style = xlwt.XFStyle()
    for row_num, row in enumerate(rows, start=1):
        for col_num, value in enumerate(row):
            if col_num == 4 and isinstance(value, str):
                value = value if value else 'No Picture'
            ws.write(row_num, col_num, value, font_style)

    wb.save(response)
    return response

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
        return JsonResponse({'message': 'Event deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def viewteam(request):
    team_members = TeamMember.objects.all()
    members = Member.objects.all()
    return render(request, 'viewteam.html', {'team_members': team_members,'members': members})

def deleteteammember(request, member_id):
    if request.method == 'POST':
        try:
            team_member = TeamMember.objects.get(pk=member_id)
            team_member.delete()
            return JsonResponse({'message': 'Team member deleted successfully'}, status=200)
        except TeamMember.DoesNotExist:
            return JsonResponse({'error': 'Team member not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def deletemember(request, member_id):
    if request.method == 'POST':
        try:
            member = Member.objects.get(pk=member_id)
            member.delete()
            return JsonResponse({'message': 'Member deleted successfully'}, status=200)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def viewgallery(request):
    gallery_images = GalleryImage.objects.all()
    return render(request, 'viewgallery.html', {'gallery_images': gallery_images})

@require_POST
def deletegalleryimage(request, image_id):
    try:
        image = GalleryImage.objects.get(pk=image_id)
        image.delete()
        return JsonResponse({'success': True, 'message': 'Gallery image deleted successfully'}, status=200)
    except GalleryImage.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Gallery image not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

def updatemarquee(request):
    if request.method == 'POST':
        new_content = request.POST.get('content')
        MarqueeContent.objects.update_or_create(id=1, defaults={'content': new_content})
        messages.success(request, 'Marquee content updated successfully!')
        marquee_content = MarqueeContent.objects.first()
        return render(request, 'updatemarquee.html', {'marquee_content': marquee_content})

    marquee_content = MarqueeContent.objects.first()
    return render(request, 'updatemarquee.html', {'marquee_content': marquee_content})