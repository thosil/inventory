# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import netaddr
from inventaires.hosts.models import *
import settings
from datetime import datetime

class Command(BaseCommand):
  args = ''
  help = 'update vlans with ip of hosts, design to be used as a cron job'
  
  def handle(self, *args, **options):
    print 'INFO: %s: BEGIN vlan update' % datetime.now().ctime()
    errors=0
    try:
      UpdateVlans()
    except Exception as e:
      print "ERROR: ****** Oops, unhandled problem here ******"
      print e
      print "ERROR: ******************************************"
      errors +=1
    print 'INFO: %s: END vlanupdate with %s error(s)' % (datetime.now().ctime(),errors)

def UpdateVlans():
  # create a vlan dict { netaddr.IPNetwork : Vlan }
  vlans={}
  for v in Vlan.objects.all():
    try:
      vlans[netaddr.IPNetwork(v.network + "/" + v.netmask)] = v
    except netaddr.AddrFormatError:
      print "WARNING: vlan %s has no valid network/netmask: %s/%s" % (v.vlannumber, v.network,v.netmask)
  # check for each host if ip is in a vlan
  for h in Host.objects.all():
    #print "DEBUG: processing %s, %s" % (h,datetime.now().ctime())
    try:
      ip=netaddr.IPAddress(h.ip)
    except netaddr.AddrFormatError:
      print "WARNING: %s as no good ip: %s" % (h,h.ip)
      pass
    for network,vlan in vlans.iteritems():
      if netaddr.smallest_matching_cidr(ip,network):
        if h.vlan_id != vlan.id:
          h.vlan=vlan
          h.save()
          print "INFO: add %s to vlan %s" % (h,vlan)
        pass
