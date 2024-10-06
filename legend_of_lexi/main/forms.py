from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Feedback
from .models import Post, Reply

class UserRegistrationForm(UserCreationForm):
    minecraft_username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'minecraft_username', 'password1', 'password2']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields =['content']
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        