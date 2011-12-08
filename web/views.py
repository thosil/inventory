# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from settings import INV_LOGLEVEL
import os

def index(request):
    return render_to_response('web/index.html',)

def logs(request):
    try:
        with open("/var/log/inventory/UpdateAll.log") as logfile:
            data = logfile.readlines()
        #out=[line.strip("\n").split(":") for line in data if line.split(" ")[0] in ("WARNING:","Warning:","DEBUG:","INFO:","ERROR:")]
        out=[line.strip("\n").split(":") for line in data if line.split(" ")[0] in INV_LOGLEVEL]
    except IOError:
        out=(("ERROR","can't open /var/log/inventory/UpdateAll.log"))
    return render_to_response('web/logs.html', ({'logs': out,}))

class ResolvForm(forms.Form):
  hostname = forms.CharField(max_length=40, label="Host or IP")

def resolv(request):
  if request.method == 'POST':
    form = ResolvForm(request.POST)
    if form.is_valid():
      hostname = form.cleaned_data['hostname']
      if hostname.replace(".","").replace("-","").isalnum():
        command = "host %s" % hostname
        results = [line.strip("\n") for line in os.popen(command).readlines()]
        return render_to_response('web/resolv.html', ({'form': form,'results':results,}))
      else:
        return render_to_response('web/resolv.html', ({'form': form,'errormsg':'invalid hostname or ip'}))
    else:
      return render_to_response('web/resolv.html', ({'form':form,}))
  else:
    form = ResolvForm()
    return render_to_response('web/resolv.html', ({'form':form,}))
