from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'telephone', 'email']

class CVAdmin(admin.ModelAdmin):
    list_display = ['subject', 'experience', 'education', 'extra_info']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'created_at', 'category']
    list_filter = ['category']

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.CV, CVAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, MPTTModelAdmin)
admin.site.register(models.Comment, MPTTModelAdmin)
