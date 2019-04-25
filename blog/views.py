from django.shortcuts import render

from blog.models import Post

# Create your views here.

def homepage(request):
    return render(request, 'post/post_index.html')


def post_year_archive(request, year):
    post_list = Post.objects.filter(post_date__year=year)
    context = {'year': year, 'post_list': post_list}
    return render(request, 'post/post_year.html', context)


def post_month_archive(request, year, month):
    post_list = Post.objects.filter(post_date__year=year, post_date__month=month)
    context = {'year': year, 'month' : month, 'post_list': post_list}
    return render(request, 'post/post_month.html', context)


def post_detail(request, year, month, id):
    post_list = Post.objects.filter(post_date__year=year, post_date__month=month, id=id)
    context = {'year': year, 'month': month, 'id': id, 'post_list': post_list}
    return render(request, 'post/post_detail.html', context)
