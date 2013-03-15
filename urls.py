from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^forgot/', 'core.views.forgot_password', name='forgotpassword'),
    url(r'^changepassword', 'core.views.change_password', name='changepassword'),
    url(r'^advisor/(?P<page>\w+)', 'advisors.views.dispatch', name='advisor'),
    url(r'^chair/(?P<page>\w+)', 'chairs.views.dispatch', name='chair'),
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^register', 'core.views.register', name='register'),
    url(r'^logout', 'core.views.logout_user', name='logout'),
    url(r'^login/user/(?P<uid>\d+)$', 'core.views.login_as_user', name='login_as_user'),
    url(r'^login', 'core.views.login_user', name='login'),
    url(r'^uniqueuser/', 'core.views.validate_unique_user', name='uniqueuser'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'core.views.index', name='index'),
)
