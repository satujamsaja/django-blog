from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from martor.models import MartorField
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category',
        verbose_name_plural = 'Categories'


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
    post_featured_image = VersatileImageField(
        'Featured',
        upload_to='post',
        default='',
        blank=True,
        width_field='post_featured_image_width',
        height_field='post_featured_image_height',
        ppoi_field='post_featured_ppoi'
    )
    post_featured_image_height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    post_featured_image_width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    post_featured_ppoi = PPOIField(
        'Image PPOI'
    )
    post_header = VersatileImageField(
        'Header',
        upload_to='post',
        default='',
        blank=True,
        width_field='post_header_image_width',
        height_field='post_header_image_height',
        ppoi_field='post_header_ppoi'
    )
    post_header_image_height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    post_header_image_width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    post_header_ppoi = PPOIField(
        'Image PPOI'
    )

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
    page_header = VersatileImageField(
        'Header',
        upload_to='page',
        default='',
        blank=True,
        width_field='page_header_image_width',
        height_field='page_header_image_height',
        ppoi_field='page_header_ppoi'
    )
    page_header_image_height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    page_header_image_width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    page_header_ppoi = PPOIField(
        'Image PPOI'
    )

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

# Handle image thumbnail generation on save
@receiver(models.signals.post_save, sender=Post)
def warm_post_images(sender, instance, **kwargs):
    """
    Pre-warm post header
    """
    post_header_image_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='header',
        image_attr='post_header'
    )
    post_header_image_warmer.warm()

    """
    Pre-warm post featured image
    """
    post_featured_image_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='featured',
        image_attr='post_featured_image'
    )
    post_featured_image_warmer.warm()

@receiver(models.signals.post_save, sender=Page)
def warm_page_images(sender, instance, **kwargs):
    """
    Pre- warm post header
    """
    page_header_image_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='header',
        image_attr='page_header'
    )
    page_header_image_warmer.warm()

# Handle image deletion on instance delete
@receiver(models.signals.post_delete, sender=Post)
def delete_post_images(sender, instance, **kwargs):
    """
    Delete post featured images
    """
    instance.post_featured_image.delete_all_created_images()
    instance.post_featured_image.delete(save=False)
    """
    Delete post header images
    """
    instance.post_header.delete_all_created_images()
    instance.post_header.delete(save=False)

@receiver(models.signals.post_delete, sender=Page)
def delete_page_images(sender, instance, **kwargs):
    """
    Delete page images
    """
    instance.page_header.delete_all_created_images()
    instance.page_header.delete(save=False)

