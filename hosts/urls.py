from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, ListView, DetailView
from hosts.models import *
from hosts.views import *
from datetime import date,timedelta

# return an queryset of 'Host', if we ask for a list default is --> template/hosts/host_list.html
# return an queryset of 'Host', if we ask for a detail default is --> template/hosts/host_detail.html
def get_hosts():
    return {'queryset': Host.objects.all()}

# return an queryset of 'Client', if we ask for a list default is --> template/hosts/client_list.html
# return an queryset of 'Client', if we ask for a detail default is --> template/hosts/client_detail.html
def get_clients():
    return {'queryset': Client.objects.all().order_by('clientname')}

# return an queryset of 'Vlan', if we ask for a list default is --> template/hosts/vlan_list.html
# return an queryset of 'Vlan', if we ask for a detail default is --> template/hosts/vlan_detail.html
def get_vlans():
    return {'queryset': Vlan.objects.all()}

# return an queryset of 'OS', if we ask for a list default is --> template/hosts/os_list.html
# return an queryset of 'OS', if we ask for a detail default is --> template/hosts/os_detail.html
def get_oses():
    return {'queryset': OS.objects.all().order_by('osname', 'vendor', 'majorversion', 'minorversion')}

# return an queryset of 'Package', if we ask for a list default is --> template/hosts/package_list.html
# return an queryset of 'Package', if we ask for a detail default is --> template/hosts/package_detail.html
def get_pkgs():
    return { 'queryset' : Package.objects.all().order_by('pkgname', '-version') }


# Reporting:

# produce a list of servers without package ILMT-TAD4D-agent installed
# return an queryset of 'Host', we ask for a list default is --> template/hosts/host_list.html
def get_no_imlt():
    return { 
      'queryset' : Host.objects.exclude(packages__pkgname__contains="ILMT-TAD4D-agent"),
      'extra_context': {'title': 'Hosts without ILMT', 'h2': 'Hosts without ILMT'},
    }

# produce a list of servers where lastchek is greater than 7 days
# return an queryset of 'Host', we ask for a list default is --> template/hosts/host_list.html
def get_old_check():
    return {
      'queryset' : Host.objects.exclude(lastcheck__range=(date.today() - timedelta(7), date.today())),
      'extra_context': {'title': 'Old check', 'h2': 'Outdated inventories'},
    }

urlpatterns = patterns('hosts.views',
    (r'^$', direct_to_template, {'template': 'hosts/index.html'}),
    #(r'^hosts/$', 'hosts'),
    #(r'^hosts/(?P<sortby>\w+)/$', 'hosts'),
    (r'^hosts/host/(?P<object_id>\d+)/$', list_detail.object_detail, get_hosts()),
    (r'^hosts/host/update/(?P<pk>\d+)/$', UpdateHost.as_view()),
    (r'^search/(?P<searchclass>.*)/(?P<searchvalue>.*)/$', 'searchview'),
    (r'^reporting/oldinv/$', list_detail.object_list, get_old_check()),
    (r'^clients/$', list_detail.object_list, get_clients()),
    (r'^clients/client/(?P<object_id>\d+)/$', list_detail.object_detail, get_clients()),
    (r'^clients/client/update/(?P<pk>\d+)/$', UpdateClient.as_view()),
    (r'^vlans/$', ListView.as_view(model = Vlan)),
    (r'^vlans/vlan/(?P<pk>\d+)/$', DetailView.as_view(model=Vlan)),
    (r'^vlans/update/vlan/(?P<pk>\d+)/$', UpdateVlan.as_view()),
    (r'^oses/$', list_detail.object_list, get_oses()),
    (r'^oses/type/(?P<os_type>\w+)/$', 'ostype'),
    (r'^oses/vendor/(?P<os_vendor>\w+)/$', 'osvendor'),
    (r'^oses/os/(?P<object_id>\d+)/$', list_detail.object_detail, get_oses()),
    #(r'^packages/allpackages/$', 'get_all_packages'),
    (r'^packages/no_ilmt/$', list_detail.object_list, get_no_imlt()),
    (r'^packages/package/(?P<object_id>\d+)/$', list_detail.object_detail, get_pkgs()),
    (r'^addremovehost/$','addremovehost'),
    (r'^addhost/$','addhost'),
    (r'^removehost/$','removehost'),
)
#    (r'^vlans/$', list_detail.object_list, get_vlans()),
#    (r'^vlans/vlan/(?P<object_id>\d+)/$', list_detail.object_detail, get_vlans()),
