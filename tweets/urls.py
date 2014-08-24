from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.blog.urls', namespace='blog')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)



urlpatterns += patterns('', (r'^static/(.*)$',
							'django.views.static.serve',
							{ 'document_root': settings.STATIC_ROOT }),)
