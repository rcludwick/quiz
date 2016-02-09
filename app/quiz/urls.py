from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<quiz_id>\d+)/$', views.quiz, name='quiz'),
]
