from django.forms import ModelForm, CharField, EmailField, Textarea
from blog.models import Comment


class CommentForm(ModelForm):
    comment_name = CharField(label='Your name', max_length=150)
    comment_email = EmailField(label='Your email', max_length=150)
    comment_body = CharField(label='Your comment', widget=Textarea, help_text='Please enter your comment')

    class Meta:
        model = Comment
        fields = [
            'comment_name',
            'comment_email',
            'comment_body',
            'comment_post',
        ]


