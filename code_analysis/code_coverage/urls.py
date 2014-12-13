from django.conf.urls import patterns, include, url
from code_coverage import views
from code_coverage.views import *

urlpatterns = patterns('english.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^downloader', DownloaderView.as_view(), name='downloader'),
    #url(r'selector/$', views.selectorReps, name='selectors'),
    url(r'^selector/(?P<repo_id>\d+)', SelectorView.as_view(), name='selector'),
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^register', RegisterView.as_view(), name='register'),
)
