from django.contrib import admin

from .models import News,Comment,NewsStatus,CommentStatus

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(NewsStatus)
admin.site.register(CommentStatus)

# Register your models here.
