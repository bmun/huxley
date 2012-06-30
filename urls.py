from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^ajax/', 'cms.views.ajax_working'),
    url(r'^updateprefs/', 'cms.views.update_prefs'),
    url(r'^forgot/', 'cms.views.forgot_password'),
    url(r'^changepassword/', 'cms.views.change_password'),
    url(r'^advisor/(?P<page>\w+)/', 'cms.views.advisor'),
    url(r'^chair/(?P<page>\w+)/', 'cms.views.chair'),
    url(r'^about/', 'cms.views.about'),
    url(r'^updatewelcome/', 'cms.views.update_welcome'),
    url(r'^register/', 'cms.views.register'),
    url(r'^testupdateroster/', 'cms.views.test_update_roster'),
    url(r'^updateroster/', 'cms.views.update_roster'),
    url(r'^logout/', 'cms.views.logout_user'),
    url(r'^login/', 'cms.views.login_user'),
    url(r'^uniqueuser/', 'cms.views.validate_unique_user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cms.views.index'),
)
