# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from inventaires.hosts.models import *
import settings
from datetime import datetime
import traceback
import ldap

class Command(BaseCommand):
    args = ''
    help = 'import external users from config in settings.py (extuser_* vars)'

    def handle(self, *args, **options):
        print 'INFO: %s: External Users Import BEGIN' % datetime.now().ctime()
        errors=0
        try:
            ImportUpdate()
        except Exception as e:
            traceback.print_exc()
            print e
            print "ERROR: ******************************"
            print "ERROR: ***** Can't import users *****"
            print "ERROR: ******************************"
            errors +=1
        print 'INFO: %s: External Users Import END with %s error(s)' % (datetime.now().ctime(),errors)

def ImportUpdate():
    ''' open connection and get user list, create/delete/update them if necessary'''
    cnx = ldap.initialize(settings.extuser_ldapsrv)
    extusers = cnx.search_s( settings.extuser_basedn,
                             settings.extuser_scope,
			     settings.extuser_filter,
			     settings.extuser_attrs)
    # cleanup old users
    extuserset=set([user[1]['uidnumber'][0] for user in extusers])
    intextuserset = set([ str(user["uid"]) for user in ExternalUser.objects.all().values()])
    userstodelete = intextuserset - extuserset
    for olduser in userstodelete:
        ExternalUser.objects.get(uid=olduser).delete()
	print "DEBUG: delete user %s" % olduser
    # create / update new users
    for extluser in extusers:
	newusername = extluser[1]['uid'][0]
	newuid = extluser[1]['uidnumber'][0]
	newgid = extluser[1]['gidnumber'][0]
	newgecos = extluser[1]['gecos'][0].decode("latin1")
	newhome = extluser[1]['homedirectory'][0]
	newshell = extluser[1]['loginshell'][0]
	try:
	    oldextuser = ExternalUser.objects.get(uid=newuid, username=newusername)
	except ObjectDoesNotExist:
	    oldextuser = None
	newextuser,created = ExternalUser.objects.get_or_create(username=newusername,
				  uid=newuid,
				  gid=newgid,
				  gecos=newgecos,
				  home=newhome,
				  shell=newshell)
        if created == True and oldextuser != None:
	    oldextuser.delete()
	    print "DEBUG: update user: %s" % newextuser.getent()
	elif created == True and oldextuser == None:
	    print "DEBUG: create user: %s" % newextuser.getent()
