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
    url(r'^updateprefs/', 'cms.views.update_prefs', name='updateprefs'),
    url(r'^forgot/', 'core.views.forgot_password', name='forgotpassword'),
    url(r'^changepassword', 'core.views.change_password', name='changepassword'),
    url(r'^advisor/(?P<page>\w+)', 'advisors.views.dispatch', name='advisor'),
    url(r'^chair/(?P<page>\w+)', 'chairs.views.dispatch', name='chair'),
    url(r'^about', 'core.views.about', name='about'),
    url(r'^updatewelcome', 'cms.views.update_welcome', name='updatewelcome'),
    url(r'^register', 'cms.views.register', name='register'),
    url(r'^updateroster/', 'cms.views.update_roster', name='updateroster'),
    url(r'^logout', 'core.views.logout_user', name='logout'),
    url(r'^login', 'core.views.login_user', name='login'),
    url(r'^uniqueuser/', 'cms.views.validate_unique_user', name='uniqueuser'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cms.views.index', name='index'),
)
