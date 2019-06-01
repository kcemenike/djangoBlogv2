"""djangoPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from blog.views import homepage, home, aboutUs, contactUs, login_page, register_page

from products.views import (
    ProductListView, 
    product_list_view, 
    ProductDetailView, 
    product_detail_view,
    ProductFeaturedListView,
    ProductFeaturedDetailView,
    ProductDetailSlugView,
    )

urlpatterns = [
    url(r'^$', home),
    # path(r"^$",home), # Why does this not work???
    url(r'^about/$', aboutUs), # you can either use url matching
    path("contact/", contactUs), # you can also use path matching
    path('admin/', admin.site.urls),
    path('blog/', homepage),
    path('login/', login_page),
    path('register/', register_page),

    url(r'^products/$', ProductListView.as_view()),
    path('products-fbv/', product_list_view),

    # url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
    url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),

    url(r'^featured/$', ProductFeaturedListView.as_view()),
    url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),

]


if settings.DEBUG: # This is so that if debug is on, static files won't be served
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# random string generator in python
from django.utils.text import slugify

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

import random, string
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))