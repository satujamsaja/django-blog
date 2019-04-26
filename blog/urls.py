from django.urls import path
from blog import views

# list urls
urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('<int:pk>', views.DetailView.as_view(), name='detail')
]
