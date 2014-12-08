from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from bars.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api$', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'bars.views.home', name='home'),
    url(r'^repo/$', RepoList.as_view(), name='repo-list'),
    url(r'^branch/$', BranchList.as_view(), name='branch-list'),
    url(r'^commit/$', CommitList.as_view(), name='commit-list'),
    url(r'^raw/$', RawList.as_view(), name='raw-list'),
    url(r'^repo/(?P<pk>\d+)/$', RepoDetail.as_view(), name='repo-detail'),
    url(r'^branch/(?P<pk>\d+)/$', BranchDetail.as_view(), name='branch-detail'),
    url(r'^commit/(?P<pk>\d+)/$', CommitDetail.as_view(), name='commit-detail'),
    url(r'^raw/(?P<pk>\d+)/$', RawDetail.as_view(), name='raw-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns,  allowed=['json', 'html'])