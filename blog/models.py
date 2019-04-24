from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_body = models.TextField(blank=False)
    post_category = models.ManyToManyField(Category)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField('post date')

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    comment_name = models.CharField(max_length=255)
    comment_email = models.CharField(max_length=255)
    comment_body = models.TextField(blank=False)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_date = models.DateTimeField('comment date')

    def __str__(self):
        return self.comment_name
