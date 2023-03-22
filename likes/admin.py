from django.contrib import admin
from likes.models import Likes

# Register your models here.
@admin.register(Likes)
class LikeAdmin(admin.ModelAdmin):
    like_display = (
        'user',
        'content_type',
        'object_id',
        'content_object',
        'created_at',
    )
    like_filter = ('content_type',)
    date_hierarchy = 'created_at'
