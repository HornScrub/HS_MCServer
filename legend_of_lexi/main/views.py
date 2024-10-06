from django.shortcuts import render, redirect, get_object_or_404
from .models import Lore
from .forms import UserRegistrationForm
from .models import Profile
from django.contrib.auth import login, authenticate
from .forms import FeedbackForm, ProfileUpdateForm
from .models import Feedback
from django.contrib.auth.decorators import login_required
from .models import Category, Post, Reply
from .forms import PostForm, ReplyForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

# main/views.py


def index(request):
    if request.user.is_authenticated:
        return redirect('hub')  # Redirect to the hub page if the user is logged in
    form = AuthenticationForm()  # Create an instance of the login form for non-logged-in users
    return render(request, 'main/index.html', {'form': form})

def login_view(request):
    # Redirect logged-in users to the home page
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home page after login
        # If form is not valid, re-render the form on the index page
        return render(request, 'main/index.html', {'form': form})

    # For GET requests, show an empty login form on the landing page
    form = AuthenticationForm()
    return render(request, 'main/index.html', {'form': form})

@login_required
def hub(request):
    return render(request, 'main/hub.html')

@login_required
def lore_list(request):
    lore_list = Lore.objects.all().order_by('-date')  # Sort by date, newest first
    return render(request, 'main/lore_list.html', {'lore_list': lore_list})

def lore_detail(request, slug):
    lore = get_object_or_404(Lore, slug=slug)  # Retrieve lore by its slug
    return render(request, 'main/lore_detail.html', {'lore': lore})



def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user with password handling
            minecraft_username = form.cleaned_data.get('minecraft_username')
            # Create a profile with the Minecraft username
            Profile.objects.create(user=user, minecraft_username=minecraft_username)
            login(request, user)  # Automatically log in the user after registration
            return redirect('index')  # Redirect to home or another page
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_thanks')
    else:
        form = FeedbackForm()
    return render(request, 'main/submit_feedback.html', {'form': form})

def thank_you(request):
    return render(request, 'main/feedback_thanks.html')

@login_required
def forum_categories(request):
    categories = Category.objects.all()
    return render(request, 'main/forum_categories.html', {'categories': categories})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all()  # Get all replies for this post
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.save()
            return redirect('post_detail', post_id=post_id)
    else:
        reply_form = ReplyForm()

    return render(request, 'main/post_detail.html', {'post': post, 'reply_form': reply_form})

@login_required
def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.posts.all()
    return render(request, 'main/category_posts.html', {'category': category, 'posts': posts})

@login_required
def create_post(request, category_id):
    # Ensure the category exists
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.author = request.user
            post.save()
            return redirect('category_posts', category_id=category_id)
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {'form': form, 'category': category})

@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.save()
            return redirect('post_detail', post_id=post_id)
        
    else:
        form = ReplyForm()
    return render(request, 'main/reply_to_post.html', {'form': form, 'post': post})

@login_required
def update_profile(request):

    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'main/update_profile.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    return render(request, 'main/profile.html', {'profile': profile})

