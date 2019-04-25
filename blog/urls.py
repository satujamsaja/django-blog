from django.urls import path
from blog import views

# list urls
urlpatterns = [
   path('<int:year>', views.post_year_archive, name='post_year'),
   path('<int:year>/<int:month>/', views.post_month_archive, name='post_month'),
   path('<int:year>/<int:month>/<int:id>', views.post_detail, name='post_detail'),
]

