from django.db import models

class VirtGroup(models.Model):
    groupname = models.CharField(max_length=40, unique=True)
    client = models.ForeignKey('hosts.Client',null=True,blank=True)
    hypervisor = models.ForeignKey('HyperVisor')
    def __unicode__(self):
        return self.groupname

class HyperVisor(models.Model):
    hvname = models.CharField(max_length=40, unique=True)
    vendor = models.CharField(max_length=15, null = True, blank = True)
    version = models.CharField(max_length=15, null = True, blank = True)
    vmmobility = models.BooleanField(default=True)
    def __unicode__(self):
        return self.vendor + " " + self.hvname + " " + self.version

class Frame(models.Model):
    hostname = models.CharField(max_length=40, unique=True)
    description = models.TextField(null=True,blank=True)
    virtgroup = models.ForeignKey('VirtGroup')
    cpu = models.IntegerField()
    gbmem = models.DecimalField(max_digits=8,decimal_places=1)
    def __unicode__(self):
        return self.hostname

class VM(models.Model):
    vmname = models.CharField(max_length=40, unique=True)
    vcpu = models.DecimalField(max_digits=8,decimal_places=1)
    gbmem = models.DecimalField(max_digits=8,decimal_places=1)
    parent = models.ForeignKey('Frame')
    host = models.OneToOneField('hosts.Host',null=True,blank=True)
    def __unicode__(self):
        return self.vmname
    def get_virtgroup(self):
        return parent.virtgroup
