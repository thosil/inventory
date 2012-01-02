# Create your views here.
from django.template import Context, loader
from django.views.generic import UpdateView
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from inventaires.hosts.models import *
from inventaires.hosts.forms import *
from django.db.models import Count
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class paginator_bottom():
  def __init__(self, paginator, range_num = 10):
    #import pdb ; pdb.set_trace()
    # make some arithmetics to generate the range of pages to show for pagination
    # show ten pages by default but verify if the range is correct and if we have enough pages
    current_page_num = int(paginator.number)
    last_page_num = int(paginator.paginator.num_pages)
    # range_arithm is range -1 because we add range_arithm to the first
    # page of the list
    range_arithm = range_num - 1
    if last_page_num < range_arithm:
      incr = last_page_num - 1
    elif last_page_num == 1:
      incr = 0
    else:
      incr = range_arithm
    first_of_list = current_page_num - 4
    if first_of_list < 1:
      first_of_list = 1
    last_of_list = first_of_list + incr
    if last_of_list > last_page_num:
      last_of_list = last_page_num
      first_of_list = last_page_num - incr
    # Now we generate the range of pages to show
    self.list_range = range(first_of_list, last_of_list + 1)
    # Now we verify if we need to show the "first" and "last" link
    if self.list_range[-1] == last_page_num:
      self.show_last = False
    else:
      self.show_last = True
    if self.list_range[0] == 1:
      self.show_first = False
    else:
      self.show_first = True

def searchview(request, searchclass, searchvalue):
  if searchclass == 'hostname' : return get_host_by(request,'hostname', searchvalue)
  if searchclass == 'description' : return get_host_by(request,'description', searchvalue)
  if searchclass == 'package': return get_packages(request, searchvalue)
  if searchclass == 'hosttype': return get_host_by(request, 'type', searchvalue)
  if searchclass == 'ostype': return ostype(request, searchvalue)
  if searchclass == 'osversion': return osversion(request, searchvalue)
  if searchclass == 'osvendor': return osvendor(request, searchvalue)
  if searchclass == 'ip': return get_host_by(request, 'ip', searchvalue)
  if searchclass == 'user': return get_host_by(request, 'user', searchvalue)
  return render_to_response('debug.html', {'debug_data': (searchclass,searchvalue)})

def get_host_by(request, searchclass, searchvalue):
  try:
    if searchclass == 'hostname':
      if searchvalue == 'allhosts':
        hosts = Host.objects.order_by('hostname')
        h2 = "All hosts" 
      else:
        hosts = Host.objects.filter(hostname__icontains=searchvalue).order_by('hostname',)
        h2 = "Hosts with %s in hostname." % searchvalue
    elif searchclass == 'description':
      hosts = Host.objects.filter(description__icontains=searchvalue).order_by('hostname',)
      h2 = "Hosts with %s in descrption." % searchvalue
    elif searchclass == 'type':
      hosts = Host.objects.filter(type__icontains=searchvalue)
      h2 = "Hosts with type %s." % searchvalue
    elif searchclass == 'ip':
      hosts = Host.objects.filter(ip__icontains=searchvalue)
      h2 = "Hosts with ip %s." % searchvalue
    elif searchclass == 'user':
      hosts = Host.objects.filter(user__username__icontains=searchvalue)
      h2 = "Hosts with user %s." % searchvalue

    if hosts.count() == 1:
      return render_to_response('hosts/host_detail.html',({'object': hosts[0]}))
    else:
      paginator = Paginator(hosts, 200)
      try:
        current_page = request.GET.get('page')
        current_page_paginator = paginator.page(current_page)
      except:
        current_page_paginator = paginator.page(1)

      pagin_bottom = paginator_bottom(current_page_paginator)

      return render_to_response('hosts/host_list.html',({'current_page_paginator': current_page_paginator, 'pagin_bottom': pagin_bottom ,'h2': h2}))
  except:
    raise Http404

def get_packages(request, searchvalue):
  try:
    if searchvalue == 'allpackages':
      packages_list = Package.objects.all().order_by('pkgname', '-version')
    else:
      packages_list = Package.objects.filter(pkgname__icontains=searchvalue)

    paginator = Paginator(packages_list, 200)
    try:
      current_page = request.GET.get('page')
      current_page_paginator = paginator.page(current_page)
    except:
      current_page_paginator = paginator.page(1)

    pagin_bottom = paginator_bottom(current_page_paginator)
          
    return render_to_response('hosts/package_list.html',({'current_page_paginator': current_page_paginator, 'pagin_bottom': pagin_bottom}))
  except:
    raise Http404

def ostype(request, os_type):
  try:
    oses = OS.objects.filter(osname__icontains=os_type).annotate(Count('host'))
    return render_to_response('hosts/os_type.html', ({'type': os_type, 'oses': oses,}))
  except OS.DoesNotExist:
    raise Http404

def osversion(request, searchvalue):
  try:
    oses = OS.objects.filter(majorversion__iexact=searchvalue).annotate(Count('host'))
    return render_to_response('hosts/os_type.html', ({'type': searchvalue, 'oses': oses,}))
  except OS.DoesNotExist:
    raise Http404

def osvendor(request, os_vendor):
  try:
    oses = OS.objects.filter(vendor__icontains=os_vendor).annotate(Count('host'))
    return render_to_response('hosts/os_type.html', ({'type': os_vendor, 'oses': oses,}))
  except OS.DoesNotExist:
    raise Http404

def addremovehost(request):
  addform    = AddHostForm()
  removeform = DeleteHostForm()
  return render_to_response('web/addremovehost.html',{'addform':addform,'removeform':removeform})

def addhost(request):
  if request.method == 'POST':
    form = AddHostForm(request.POST)
    if form.is_valid():
      newhost=form.cleaned_data['hostname']
      if newhost.isalnum() != True:
        return render_to_response('web/addremovehost.html',{'addform':form, 'removeform':DeleteHostForm(), 'errormsg': "'%s' is not a valid hostname" % newhost})
      if Host.objects.filter(hostname=newhost).count() > 0 :
        return render_to_response('web/addremovehost.html',{'addform':form, 'removeform':DeleteHostForm(), 'errormsg': "%s already exist in db" % newhost})
      command="/opt/inventory/scripts/AddHost %s" % newhost
      results = os.popen(command).readlines()
      try:
        newhostobject = Host.objects.get(hostname=newhost)
        client=form.cleaned_data['client']
        newhostobject.client = Client.objects.get(clientname=client)
        newhostobject.save()
        return HttpResponseRedirect('/hosts/search/hostname/%s/' % newhostobject.hostname)
      except Host.DoesNotExist:
        return render_to_response('web/addremovehost.html',{'addform':form, 'removeform':DeleteHostForm(), 'errormsg': "Can't add '%s' to database, check manualy." % newhost})
    else:
      return render_to_response('web/addremovehost.html',{'addform':form, 'removeform':DeleteHostForm()})
  else:
    return HttpResponseRedirect('/hosts/addremovehost/')

def removehost(request):
  if request.method == 'POST':
    form = DeleteHostForm(request.POST)
    if form.is_valid():
      oldhost=form.cleaned_data['host']
      try:
        oldhostobject = Host.objects.get(hostname=oldhost)
        oldhostobject.delete()
        return render_to_response('web/addremovehost.html',{'addform':AddHostForm(), 'removeform':form, 'infomsg': "Host '%s' as been deleted from database." % oldhost})
      except Host.DoesNotExist:
        return render_to_response('web/addremovehost.html',{'addform':AddHostForm(), 'removeform':form, 'errormsg': "Can't delete host '%s'." % oldhost})
    else:
      return render_to_response('web/addremovehost.html',{'addform':AddHostForm(), 'removeform':form})
  else:
    return HttpResponseRedirect('/hosts/addremovehost/')

class UpdateVlan(UpdateView):
  model=Vlan
  form_class=VlanForm
  success_url='/hosts/vlans/'

class UpdateClient(UpdateView):
  model=Client
  form_class=ClientForm
  success_url='/hosts/clients'

class UpdateHost(UpdateView):
  model=Host
  form_class=HostForm
  success_url='/hosts/hosts'
