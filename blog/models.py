from django.db import models
from django.contrib.auth.models import User
from martor.models import MartorField

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    POST_STATUS_CHOICES = (
        ('1', 'Published'),
        ('0', 'UnPublished'),
    )
    POST_HEADLINE_CHOICES = (
        ('1', 'Yes'),
        ('0', 'No'),
    )
    POST_FEATURED_CHOICES = (
        ('1', 'Yes'),
        ('0', 'No'),
    )
    post_title = models.CharField(max_length=255)
    post_summary = models.TextField(blank=False, default='')
    post_body = MartorField(default='')
    post_category = models.ManyToManyField(Category)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField('post date')
    post_headline = models.CharField(max_length=1, choices=POST_HEADLINE_CHOICES, default='1')
    post_featured = models.CharField(max_length=1, choices=POST_FEATURED_CHOICES, default='1')
    post_status = models.CharField(max_length=1, choices=POST_STATUS_CHOICES, default='1')
    post_header = models.ImageField(upload_to='post', default='')

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    COMMENT_STATUS_CHOICE = (
        ('1', 'Published'),
        ('0', 'UnPublished'),
    )
    comment_name = models.CharField(max_length=255)
    comment_email = models.CharField(max_length=255)
    comment_body = models.TextField(blank=False)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_date = models.DateTimeField('comment date')
    comment_status = models.CharField(max_length=1, choices=COMMENT_STATUS_CHOICE, default='1')

    def __str__(self):
        return self.comment_name


class Page(models.Model):
    PAGE_STATUS_CHOICE = (
        ('1', 'Published'),
        ('0', 'UnPublished'),
    )
    page_name = models.CharField(max_length=255)
    page_body = MartorField(default='')
    page_author = models.ForeignKey(User, on_delete=models.CASCADE)
    page_date = models.DateTimeField('page date')
    page_status = models.CharField(max_length=1, choices=PAGE_STATUS_CHOICE, default='1')
    post_header = models.ImageField(upload_to='page', default='')

    def __str__(self):
        return self.page_name


class Section(models.Model):
    SECTION_STATUS_CHOICE = (
        ('1', 'Visible'),
        ('0', 'Hidden'),
    )
    section_name = models.CharField(max_length=255)
    section_status = models.CharField(max_length=1, choices=SECTION_STATUS_CHOICE, default='1')

    def __str__(self):
        return self.section_name


class Menu(models.Model):
    MENU_STATUS_CHOICE = (
        ('1', 'Visible'),
        ('0', 'Hidden'),
    )
    menu_name = models.CharField(max_length=255)
    menu_page = models.ForeignKey(Page, on_delete=models.SET(''))
    menu_section = models.ForeignKey(Section, on_delete=models.SET(''))
    menu_status = models.CharField(max_length=1, choices=MENU_STATUS_CHOICE, default='1')

    def __str__(self):
        return self.menu_name
