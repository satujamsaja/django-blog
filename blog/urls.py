from django.urls import path
from blog import views

# list urls
urlpatterns = [
  path('', views.PostIndexView.as_view(), name='post-index'),
  path('<int:pk>', views.PostDetailView.as_view(), name='post-detail')
]
