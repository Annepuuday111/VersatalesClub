from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Signup(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_core_member = models.BooleanField(default=False)

    class Meta:
        db_table = 'signup_table'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    choosefile = models.FileField(upload_to='uploads/', blank=True, null=True)
    message = models.TextField()

    class Meta:
        db_table = "contact_table"

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    location = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        db_table = "event_table"

    def __str__(self):
        return self.title

class Story(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    image = models.ImageField(upload_to='story/')
    content = models.TextField()
    creator = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = "story_table"

    def __str__(self):
        return self.title

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "gallery_table"

    def __str__(self):
        return self.image.name

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='team_members/')
    bio = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = "teammembers_table"

    def __str__(self):
        return self.name

class Member(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='members/', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = "members_table"

    def __str__(self):
        return self.name

class MarqueeContent(models.Model):
    content = models.TextField()

    class Meta:
        db_table = "marqueecontent_table"

    def __str__(self):
        return self.content


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='adminapp_user_set',  # Add related_name to avoid conflict
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='adminapp_user_set',  # Add related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    # Add any additional fields or methods here