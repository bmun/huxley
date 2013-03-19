from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^password/forgot', 'huxley.core.views.forgot_password', name='forgot_password'),
    url(r'^password/change', 'huxley.core.views.change_password', name='change_password'),
    url(r'^advisor/(?P<page>\w+)', 'huxley.advisors.views.dispatch', name='advisor'),
    url(r'^chair/(?P<page>\w+)', 'huxley.chairs.views.dispatch', name='chair'),
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^register', 'huxley.core.views.register', name='register'),
    url(r'^logout', 'huxley.core.views.logout_user', name='logout'),
    url(r'^login/user/(?P<uid>\d+)$', 'huxley.core.views.login_as_user', name='login_as_user'),
    url(r'^login', 'huxley.core.views.login_user', name='login'),
    url(r'^uniqueuser/', 'huxley.core.views.validate_unique_user', name='uniqueuser'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'huxley.core.views.index', name='index'),
)
