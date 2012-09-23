from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from leaguetrack.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^import/$', import_replay),
    url(r'^register/$', 'accounts.views.register'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='logout'),
    url(r'^summoner/(?P<region>[-\w]+)/(?P<summoner_name>[-\w]+)/$', view_summoner),
    url(r'^summoner/(?P<region>[-\w]+)/(?P<summoner_name>[-\w]+)/follow_toggle/$', follow_toggle_summoner),
    url(r'^metrics/(?P<region>[-\w]+)/(?P<summoner_name>[-\w]+)/$', view_metrics),
    url(r'^game/(?P<game_id>[-\w]+)/$', view_game),
    url(r'^$', home_page),
)
