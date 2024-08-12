from django import forms
from .models import Signup
from .models import Contact
from .models import Event
from .models import Story
from .models import GalleryImage
from .models import TeamMember
from .models import Member


class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['name', 'email', 'username', 'password', 'gender', 'phone', 'location']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 15:
            raise forms.ValidationError("Password should not exceed 15 characters.")
        return password

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'choosefile', 'message']

    choosefile = forms.FileField()

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'poster', 'location', 'description']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'Select date',
                'class': 'form-control',
            }),
        }

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'date', 'image', 'content', 'creator']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'Select date',
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your story here',
                'class': 'form-control',
                'rows': 4,
            }),
            'creator': forms.TextInput(attrs={
                'placeholder': 'Enter creator name',
                'class': 'form-control',
            }),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'description']

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'email', 'phone', 'profile_picture', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'position', 'email', 'phone', 'profile_picture', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
