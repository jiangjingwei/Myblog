from django.conf.urls import url
from blog import views

urlpatterns = [
    # url(r'^(?P<username>\w+)/(?P<num>\d+)$', views.home_page, name='home_page'),
    # url(r'^(?P<user>\w+)/edit$', views.home_edit, name='home_edit'),
    url(r'^articleDetail/(?P<pk>\d+)/$', views.article_detail, name='articleDetail'),
    url(r'(?P<num>\d+)/$', views.home_page, name='page_num'),
    url(r'^category/(?P<cate_pk>\d+)/$', views.home_page, name='category'),
    url(r'^tag/(?P<tag_pk>\d+)/$', views.home_page, name='tag'),

]