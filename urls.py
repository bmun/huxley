from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    url(r'^forgot/', 'core.views.forgot_password', name='forgotpassword'),
    url(r'^changepassword', 'core.views.change_password', name='changepassword'),
    url(r'^advisor/(?P<page>\w+)', 'advisors.views.dispatch', name='advisor'),
    url(r'^chair/(?P<page>\w+)', 'chairs.views.dispatch', name='chair'),
    url(r'^about', 'core.views.about', name='about'),
    url(r'^register', 'core.views.register', name='register'),
    url(r'^logout', 'core.views.logout_user', name='logout'),
    url(r'^login', 'core.views.login_user', name='login'),
    url(r'^uniqueuser/', 'core.views.validate_unique_user', name='uniqueuser'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'core.views.index', name='index'),
)
