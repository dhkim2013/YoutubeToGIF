from django.conf.urls import url

from gif import views

urlpatterns = [
    url(r'^$', views.ConvertGIF.as_view()),
]