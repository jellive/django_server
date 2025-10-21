from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'writer', 'div', 'deleted', 'cdatetime', 'udatetime']
    list_filter = ['div', 'deleted', 'cdatetime']
    search_fields = ['title', 'context', 'writer']
    list_per_page = 20
    ordering = ['-cdatetime']
    readonly_fields = ['cdatetime', 'udatetime']

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'writer', 'div')
        }),
        ('내용', {
            'fields': ('context',)
        }),
        ('상태', {
            'fields': ('deleted',)
        }),
        ('타임스탬프', {
            'fields': ('cdatetime', 'udatetime'),
            'classes': ('collapse',)
        }),
    )
