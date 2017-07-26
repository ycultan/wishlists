from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_item$', views.add_item),
    url(r'^wish_item$', views.create),
    url(r'^wish_item/(?P<wish_id>\d+)$', views.wish_item),
    url(r'^add_wish/(?P<wish_id>\d+)$', views.add_wish),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove),
    url(r'^remove_self/(?P<wish_id>\d+)$', views.remove_self)
]