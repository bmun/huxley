from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

admin.autodiscover()

urlpatterns = patterns('huxley',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^password/forgot', 'core.views.forgot_password', name='forgot_password'),
    url(r'^password/change', 'core.views.change_password', name='change_password'),
    url(r'^advisor/(?P<page>\w+)', 'advisors.views.dispatch', name='advisor'),
    url(r'^chair/(?P<page>\w+)', 'chairs.views.dispatch', name='chair'),
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^register', 'core.views.register', name='register'),
    url(r'^logout', 'core.views.logout_user', name='logout'),
    url(r'^login/user/(?P<uid>\d+)$', 'core.views.login_as_user', name='login_as_user'),
    url(r'^login', 'core.views.login_user', name='login'),
    url(r'^uniqueuser/', 'core.views.validate_unique_user', name='unique_user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'core.views.index', name='index'),
)
