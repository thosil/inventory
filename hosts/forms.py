from django import forms
from hosts.models import Client, Host, Vlan

class AddHostForm(forms.Form):
  hostname = forms.CharField(max_length=40, label="Hostname")
  client = forms.ModelChoiceField(queryset=Client.objects.all().order_by('clientname'), label="Client")

class DeleteHostForm(forms.Form):
  host = forms.ModelChoiceField(queryset=Host.objects.all().order_by('hostname'), label="Host to remove")

class VlanForm(forms.ModelForm):
  class Meta:
    model = Vlan

class ClientForm(forms.ModelForm):
  class Meta:
    model = Client

class HostForm(forms.ModelForm):
  class Meta:
    model = Host
    exclude = ('packages',)
