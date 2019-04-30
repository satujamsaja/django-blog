import os
import json
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from martor.utils import LazyEncoder
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Post, Category, Menu, Page

# Martor image upload view.


@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))


# Post view

class PostIndexView(ListView):
    template_name = 'post/post_index.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """
        Menu Header.
        """
        try:
            menu_header = Category.objects.order_by('category_name')
        except Category.DoesNotExist:
            menu_header = None
        context['menu_header'] = menu_header

        """
        Headline.
        """
        try:
            menu_header = Post.objects.get(
                post_status__exact='1',
                post_headline__exact='1',
            )
        except Post.DoesNotExist:
            menu_header = None
        context['headline'] = menu_header

        """
        Featured.
        """
        try:
            featured = Post.objects.filter(
                post_status__exact='1',
                post_featured__exact='1',
            )[:2]
        except Post.DoesNotExist:
            featured = None
        context['featured'] = featured

        """
        Posts.
        """
        try:
            posts = Post.objects.filter(
                post_status__exact='1',
                post_featured__exact='0',
                post_headline__exact='0',
            )[:5]
        except Post.DoesNotExist:
            posts = None
        context['posts'] = posts

        """
        Sidebar Menu.
        """
        try:
            menu_sidebar = Menu.objects.filter(
                menu_status__exact='1',
                menu_section__section_name__exact='Sidebar',
            )
        except Menu.DoesNotExist:
            menu_sidebar = None
        context['menu_sidebar'] = menu_sidebar

        return context


class PostDetailView(DetailView):
    template_name = 'post/post_detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """
        Menu Header.
        """
        try:
            menu_header = Category.objects.order_by('category_name')
        except Category.DoesNotExist:
            menu_header = None
        context['menu_header'] = menu_header

        """
        Menu Sidebar.
        """
        try:
            menu_sidebar = Menu.objects.filter(
                menu_status__exact='1',
                menu_section__section_name__exact='Sidebar',
            )
        except Menu.DoesNotExist:
            menu_sidebar = None
        context['menu_sidebar'] = menu_sidebar

        return context

# Page view


class PageDetailView(DetailView):
    template_name = 'page/page_detail.html'
    model = Page
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """
        Menu Header.
        """
        try:
            menu_header = Category.objects.order_by('category_name')
        except Category.DoesNotExist:
            menu_header = None
        context['menu_header'] = menu_header

        """
        Menu Sidebar.
        """
        try:
            menu_sidebar = Menu.objects.filter(
                menu_status__exact='1',
                menu_section__section_name__exact='Sidebar',
            )
        except Menu.DoesNotExist:
            menu_sidebar = None
        context['menu_sidebar'] = menu_sidebar

        return context

# Category view


class CategoryIndexView(ListView):
    template_name = 'category/category_index.html'
    model = Post
    context_object_name = 'posts'
    category = object

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(post_category__exact=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryIndexView, self).get_context_data(**kwargs)

        """
        Menu Header.
        """
        try:
            menu_header = Category.objects.order_by('category_name')
        except Category.DoesNotExist:
            menu_header = None
        context['menu_header'] = menu_header

        """
        Headline.
        """
        try:
            menu_headline = Post.objects.get(
                post_status__exact='1',
                post_headline__exact='1',
                post_category__exact= self.category,
            )
        except Post.DoesNotExist:
            menu_headline = None
        context['headline'] = menu_headline

        """
        Featured.
        """
        try:
            featured = Post.objects.filter(
                post_status__exact='1',
                post_featured__exact='1',
                post_category__exact= self.category,
            )[:2]
        except Post.DoesNotExist:
            featured = None
        context['featured'] = featured

        """
        Posts.
        """
        try:
            posts = Post.objects.filter(
                post_status__exact='1',
                post_featured__exact='0',
                post_headline__exact='0',
                post_category__exact=self.category,
            )[:5]
        except Post.DoesNotExist:
            posts = None
        context['posts'] = posts

        """
        Menu Sidebar.
        """
        try:
            menu_sidebar = Menu.objects.filter(
                menu_status__exact='1',
                menu_section__section_name__exact='Sidebar'
            )
        except Menu.DoesNotExist:
            menu_sidebar = None
        context['menu_sidebar'] = menu_sidebar

        context['category'] = self.category

        return context
