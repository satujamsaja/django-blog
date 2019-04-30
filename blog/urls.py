from django.urls import path
from blog import views

# list urls
urlpatterns = [
  path('', views.PostIndexView.as_view(), name='post-index'),
  path('<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
  path('page/<int:pk>', views.PageDetailView.as_view(), name='page-detail'),
  path('category/<int:pk>', views.CategoryIndexView.as_view(), name='category-index'),
]
