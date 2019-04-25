from django.contrib import admin
from blog.models import Category, Post, Comment, Page, Section, Menu

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'category', 'post_body', 'post_author')

    @staticmethod
    def category(obj):
        return ", " . join([c.category_name for c in obj.post_category.all()])


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_post', 'comment_name', 'comment_email', 'comment_body')


class PageAdmin(admin.ModelAdmin):
    list_display = ('page_name',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name',)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('menu_name', 'menu_page')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Menu, MenuAdmin)
