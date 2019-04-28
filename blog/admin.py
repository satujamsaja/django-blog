from django.contrib import admin
from blog.models import Category, Post, Comment, Page, Section, Menu
from martor.widgets import AdminMartorWidget
from django.db import models

# Post actions.


def publish_post(self, request, queryset):
    publish_row = queryset.update(post_status='1')
    if publish_row == 1:
        publish_message = "1 post has been"
    else:
        publish_message = "%s posts has been" % publish_row
    self.message_user(request, "%s successfully published." % publish_message)


def unpublish_post(self, request, queryset):
    unpublish_row = queryset.update(post_status='0')
    if unpublish_row == 1:
        unpublish_message = "1 post has been"
    else:
        unpublish_message = "%s posts has been" % unpublish_row
    self.message_user(request, "%s successfully unpublished." % unpublish_message)

# Page actions.


def publish_page(self, request, queryset):
    publish_row = queryset.update(page_status='1')
    if publish_row == 1:
        publish_message = "1 page has been"
    else:
        publish_message = "%s pages has been" % publish_row
    self.message_user(request, "%s successfully published." % publish_message)


def unpublish_page(self, request, queryset):
    unpublish_row = queryset.update(page_status='0')
    if unpublish_row == 1:
        unpublish_message = "1 page has been"
    else:
        unpublish_message = "%s pages has been" % unpublish_row
    self.message_user(request, "%s successfully unpublished." % unpublish_message)


# Comment Actions.

def publish_comment(self, request, queryset):
    publish_row = queryset.update(comment_status='1')
    if publish_row == 1:
        publish_message = "1 comment has been"
    else:
        publish_message = "%s comments has been" % publish_row
    self.message_user(request, "%s successfully published." % publish_message)


def unpublish_comment(self, request, queryset):
    unpublish_row = queryset.update(comment_status='0')
    if unpublish_row == 1:
        unpublish_message = "1 comment has been"
    else:
        unpublish_message = "%s comments has been" % unpublish_row
    self.message_user(request, "%s successfully unpublished." % unpublish_message)


# Section Actions
def show_section(self, request, queryset):
    show_row = queryset.update(section_status='1')
    if show_row == 1:
        show_message = "1 section has been"
    else:
        show_message = "%s sections has been" % show_row
    self.message_user(request, "%s successfully displayed." % show_message)


def hide_section(self, request, queryset):
    hide_row = queryset.update(section_status='0')
    if hide_row == 1:
        hide_message = "1 section has been"
    else:
        hide_message = "%s sections has been" % hide_row
    self.message_user(request, "%s successfully hidden." % hide_message)

# Menu Actions


def show_menu(self, request, queryset):
    show_row = queryset.update(menu_status='1')
    if show_row == 1:
        show_message = "1 menu has been"
    else:
        show_message = "%s menus has been" % show_row
    self.message_user(request, "%s successfully displayed." % show_message)


def hide_menu(self, request, queryset):
    hide_row = queryset.update(menu_status='0')
    if hide_row == 1:
        hide_message = "1 menu has been"
    else:
        hide_message = "%s menus has been" % hide_row
    self.message_user(request, "%s successfully hidden." % hide_message)


# ModelAdmin definitions.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'post_title',
        'category',
        'post_summary',
        'post_author',
        'post_date',
        'post_headline',
        'post_featured',
        'post_status',
    )
    list_filter = (
        'post_date',
        'post_status',
        'post_headline',
        'post_featured'
    )
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    actions = [publish_post, unpublish_post]

    @staticmethod
    def category(obj):
        return ", " . join([c.category_name for c in obj.post_category.all()])


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_post', 'comment_name', 'comment_email', 'comment_body',  'comment_date', 'comment_status')
    list_filter = ('comment_date', 'comment_status')
    actions = [publish_comment, unpublish_comment]


class PageAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'page_status', 'page_date')
    list_filter = ('page_date', 'page_status')
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    actions = [publish_page, unpublish_page]


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'section_status')
    actions = [show_section, hide_section]


class MenuAdmin(admin.ModelAdmin):
    list_display = ('menu_name', 'menu_page', 'menu_status')
    actions = [show_menu, hide_menu]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Menu, MenuAdmin)
