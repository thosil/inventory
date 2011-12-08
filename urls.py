from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from hosts.models import *
databrowse.site.register(Host)
databrowse.site.register(Client)
databrowse.site.register(OS)
databrowse.site.register(Package)
databrowse.site.register(User)
databrowse.site.register(Group)
databrowse.site.register(Vlan)
databrowse.site.register(Disk)
databrowse.site.register(HostGroup)

from django.conf import settings

urlpatterns = patterns('',
    (r'^$', include('web.urls')),
    (r'^hosts/', include('hosts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^db/(.*)', databrowse.site.root),
    (r'^logs/', 'web.views.logs'),
    (r'^lookup/$', 'web.views.resolv'),
)
