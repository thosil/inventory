# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from inventaires.hosts.models import *
import settings
from datetime import datetime
import pymssql
import traceback


class Command(BaseCommand):
    args = ''
    help = 'update hosts with some infos from cmdb'

    def handle(self, *args, **options):
        print 'INFO: %s: Update from CMDB BEGIN' % datetime.now().ctime()
        errors=0
        try:
            ImportUpdate()
        except Exception as e:
            traceback.print_exc()
            print e
            print "ERROR: ******************************"
            print "ERROR: ***** Can't import infos *****"
            print "ERROR: ******************************"
            errors +=1
        print 'INFO: %s: Update from CMDB END with %s error(s)' % (datetime.now().ctime(),errors)

def ImportUpdate():
  ''' open connection'''
  try:
    conn = pymssql.connect(host=setting.INV_CMDB_HOST, user=settings.INV_CMDB_USER, password=settings.INV_CMDB_PASS, database=settings_INV_CMDB_DB, charset='CP1252')
    cur = conn.cursor()
  except:
    print "can't open database"
    return False

  '''execute query (here get hostname/description/company/env_type '''
  query='''SELECT t1.logical_name, t1.description, t1.company, t1.env_type
           FROM sc.device2m1 t1, sc.serverm1 t2
           WHERE
           t2.OS_NAME IN ('Linux', 'Solaris','AIX') AND
           t1.istatus IN ('Frozen','Operational','Under construction') AND
           t1.type IN ('lserver', 'pserver') AND
           t1.logical_name=t2.logical_name;'''
  cur.execute(query)
  for row in cur:
    try:
      # logical name (f 0) == hostname
      host = Host.objects.get(hostname__iexact=row[0])
      # descrition (f 1)
      host.description = unicode(row[1])
      # get or create client (company f 2)
      myclient, created = Client.objects.get_or_create(clientname=row[2])
      if created:
        print "INFO: %s is a new client!" % myclient
      host.client = myclient
      del(created)
      # get or create hostgroup (env_type f 3)
      if row[3] != None:
        myhostgroup,created = HostGroup.objects.get_or_create(hostgroupname=row[3])
        current_env = host.hostgroups.get(hostgroupname__regex='''^.\..*$''')
        if current_env != myhostgroup:
          host.hostgroups.remove(current_env)
          host.hostgroups.add(myhostgroup)
      host.save()
    except Host.DoesNotExist:
      # TODO: implement exclude list?
      print "DEBUG: can't find %s - %s. in inventory" % tuple(row[:2])
