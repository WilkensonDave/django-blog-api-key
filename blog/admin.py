from django.contrib import admin
from .models import Blog, Author, Comment
# Register your models here.


class BlogAdming(admin.ModelAdmin):
    list_display = ("title", "author_name")
    list_filter = ("title", "author_name")
    list_select_related = ("author",)
    
    def author_name(self, obj):
        return obj.author.name

class CommentAdmin(admin.ModelAdmin):
    list_filter = ["description"]
    list_display = ["description"]

class AuthorAdmin(admin.ModelAdmin):
    list_filter = ["name", "job_title"]
    list_display = ["name", "job_title"]
    
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Blog)