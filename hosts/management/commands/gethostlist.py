# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from inventaires.hosts.models import *

class Command(BaseCommand):
    args = ''
    help = 'import a host, arg must be a well formed file with a hostinv class'

    def handle(self, *args, **options):
        for h in Host.objects.all():
            out="%s;%s;%s" % (h,h.os.osname,h.client)
            print out.encode('utf-8')
