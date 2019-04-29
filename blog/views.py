import os
import json
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from martor.utils import LazyEncoder
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Post, Category, Menu

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
        context['menu_header'] = Category.objects.order_by('category_name')
        context['headline'] = Post.objects.get(
            post_status__exact='1',
            post_headline__exact='1')
        context['featured'] = Post.objects.filter(
            post_status__exact='1',
            post_featured__exact='1')[:2]
        context['posts'] = Post.objects.filter(
            post_status__exact='1',
            post_featured__exact='0',
            post_headline__exact='0')[:5]
        context['menu_sidebar'] = Menu.objects.filter(
            menu_status__exact='1',
            menu_section__section_name__exact='Sidebar'
        )
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post/post_detail.html'

