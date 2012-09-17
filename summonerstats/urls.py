from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^import/$', 'leaguetrack.views.import_replay'),
    url(r'^register/$', 'accounts.views.register'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='logout'),
    url(r'^(?P<user_name>[-\w]+)/$', 'leaguetrack.views.profile'),
    url(r'^game/(?P<game_id>[-\w]+)/$', 'leaguetrack.views.view_game'),
    url(r'^$', 'leaguetrack.views.home_page'),
)
