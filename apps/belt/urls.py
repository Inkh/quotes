from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success/(?P<id>\d+)$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^return$', views.account),
    url(r'^createquote$', views.createquote),
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite),
    url(r'^removefav/(?P<fav_id>\d+)$', views.removefav),
    url(r'^success/individual/(?P<user_id>\d+)$', views.individual)
    # url(r'^(?P<word>.+)$', views.nein)
]
