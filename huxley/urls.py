from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

admin.autodiscover()

urlpatterns = patterns('huxley.core.views',
    url(r'^password/forgot', 'forgot_password', name='forgot_password'),
    url(r'^password/change', 'change_password', name='change_password'),
    url(r'^register', 'register', name='register'),
    url(r'^logout', 'logout_user', name='logout'),
    url(r'^login/user/(?P<uid>\d+)$', 'login_as_user', name='login_as_user'),
    url(r'^login', 'login_user', name='login'),
    url(r'^uniqueuser/', 'validate_unique_user', name='unique_user'),
    url(r'^$', 'index', name='index'),
)

urlpatterns += patterns('',
    url(r'^chair/', include('huxley.chairs.urls', app_name='chairs')),
    url(r'^advisor/', include('huxley.advisors.urls', app_name='advisors')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about'),
)