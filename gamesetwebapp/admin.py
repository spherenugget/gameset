
from django.contrib import admin
from .models import Game, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty comment forms to display

class GameAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Game, GameAdmin)
admin.site.register(Comment)