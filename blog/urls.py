from django.conf.urls import url
from blog import views

urlpatterns = [
    # url(r'^(?P<user>\w+)$', views.home_page, name='home_page'),
    # url(r'^(?P<user>\w+)/edit$', views.home_edit, name='home_edit'),
    url(r'^articleDetail/(?P<pk>\d+)/$', views.article_detail, name='articleDetail'),
]