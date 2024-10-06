"""
URL configuration for legend_of_lexi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),  # Custom login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Built-in logout view
    path('', views.index, name='index'),
    path('hub/', views.hub, name='hub'),  # Hub route
    path('lore/', views.lore_list, name='lore_list'),
    path('lore/<slug:slug>/', views.lore_detail, name='lore_detail'),
    path('register/', views.register, name='register'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback/thanks/', views.thank_you, name='feedback_thanks'),
    path('forum/', views.forum_categories, name='forum_categories'),
    path('forum/category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('forum/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/category/<int:category_id>/new/', views.create_post, name='create_post'),
    path('forum/post/<int:post_id>/reply/', views.reply_to_post, name='reply_to_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)