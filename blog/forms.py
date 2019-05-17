from django import forms

class CommentForm(forms.Form):
    comment_name = forms.CharField(label='Your name', max_length=150)
    comment_email = forms.EmailField(label='Your email', max_length=150)
    comment_body = forms.CharField(label='Your comment', widget=forms.Textarea, help_text='Please enter your comment')
