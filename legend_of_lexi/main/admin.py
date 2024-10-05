from django.contrib import admin
from .models import Profile
from .models import Lore
from .models import Feedback

# Register your models here.

admin.site.register(Lore)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'minecraft_username']

admin.site.register(Profile, ProfileAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at')
    search_fields = ('user__username', 'subject', 'message')

admin.site.register(Feedback, FeedbackAdmin)