from django.contrib import admin
from blog.models import Category, Post, Comment

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_title', 'category', 'post_body' , 'post_author')

    def category(self, obj):
        return ", " . join([c.category_name for c in obj.post_category.all()])

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_post', 'comment_name', 'comment_email', 'comment_body')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
