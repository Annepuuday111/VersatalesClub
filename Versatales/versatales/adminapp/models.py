from django.db import models

class Signup(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

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
    poster = models.ImageField(upload_to='event/')
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
    profile_picture = models.ImageField(upload_to='team_members/')
    bio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "teammembers_table"

    def __str__(self):
        return self.name