from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^login/', views.log_in, name='login'),
    url(r'^register/', views.register, name='register'),
]