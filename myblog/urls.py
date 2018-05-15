"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from myblog import settings
from django.views.static import serve
from blog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.log_in, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^captcha/', views.get_captcha, name='captcha'),
    url(r'blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),

    # 配置media
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})

]
