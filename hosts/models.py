from django.db import models

class Host(models.Model):
    hostname = models.CharField(max_length=40, unique=True)
    description = models.TextField(null=True,blank=True)
    uptime = models.IntegerField(null=True,blank=True)
    client = models.ForeignKey('Client',null=True,blank=True)
    os = models.ForeignKey('OS')
    HOSTS_TYPES = (('Physical', 'Physical'),('Virtual', 'Virtual'))
    type = models.CharField(max_length=10,choices=HOSTS_TYPES,null=True,blank=True)
    cpu = models.IntegerField() # number of cores
    gbmem = models.DecimalField(max_digits=8,decimal_places=1)
    vlan = models.ForeignKey('Vlan',null=True,blank=True)
    ip = models.IPAddressField(unique=True) # admin ip (should be in dns)
    packages = models.ManyToManyField('Package', related_name='hosts')
    lastcheck = models.DateField(null=True,blank=True) # last inventory
    lastupdate = models.DateField(null=True,blank=True) # last os update
    datediff = models.IntegerField(null=True,blank=True) # seconds between this host and inventory server
    class Meta:
        ordering = ['hostname']
    def getent(self):
        for u in self.user_set.all():
            print u.getent()
    def __unicode__(self):
        return self.hostname

class HostGroup(models.Model):
    hostgroupname = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=50)
    members = models.ManyToManyField('Host', related_name='hostgroups', null=True, blank=True)
    class Meta:
        ordering = ['hostgroupname']
    def __unicode__(self):
        return self.hostgroupname


class Client(models.Model):
    clientname = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ['clientname']
    def __unicode__(self):
        return self.clientname

class OS(models.Model):
    osname = models.CharField(max_length=15)
    vendor = models.CharField(max_length=15)
    majorversion = models.CharField(max_length=15)
    minorversion = models.CharField(max_length=15)
    class Meta:
        ordering = ['vendor', 'majorversion', 'minorversion']
    def __unicode__(self):
        if (self.osname == 'Linux'):
            return self.vendor + " " + self.majorversion + "." + self.minorversion
        elif(self.osname == 'Solaris'):
            return self.osname + " " + self.majorversion + "u" + self.minorversion
        else:
            return self.osname + " " + self.majorversion + " " + self.minorversion

class Vlan(models.Model):
    vlannumber = models.IntegerField()
    vlanname = models.CharField(max_length=40)
    network = models.IPAddressField(unique=True)
    netmask = models.IPAddressField()
    gateway = models.IPAddressField(null=True, blank=True)
    dns1 = models.IPAddressField(null=True, blank=True)
    dns2 = models.IPAddressField(null=True, blank=True)
    domain = models.CharField(max_length=40,null=True, blank=True)
    ntp = models.CharField(max_length=40,null=True, blank=True)
    class Meta:
        ordering = ['vlannumber']
    def __unicode__(self):
        return str(self.vlannumber) + " - " + self.vlanname + ' - ' + self.network + " - " + self.netmask
    
class Disk(models.Model):
    diskname = models.CharField(max_length = 50)
    size = models.IntegerField()
    deviceid = models.CharField(max_length = 4, null=True, blank=True)
    host = models.ForeignKey('Host')
    def __unicode__(self):
        return self.diskname
    class Meta:
        ordering = ['host__hostname','diskname']

class Group(models.Model):
    groupname = models.CharField(max_length = 40)
    gid = models.IntegerField()
    host = models.ForeignKey('Host')
    members = models.ManyToManyField('User', related_name='groups')
    extmembers = models.ManyToManyField('ExternalUser', related_name='intgroups')
    class Meta:
        ordering = ['gid']
    def __unicode__(self):
        return self.groupname

class AbsUser(models.Model):
    username = models.CharField(max_length = 40, default="")
    uid = models.IntegerField()
    gid = models.IntegerField()
    gecos = models.CharField(max_length = 70, null=True, blank=True)
    home = models.CharField(max_length = 200, default="")
    shell = models.CharField(max_length = 70, default="")
    def getent(self):
        out =  "%s:x:%s:%s:%s:%s:%s" % (self.username, self.uid, self.gid, self.gecos, self.home, self.shell)
        return out.encode("latin1")
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.username

class ExternalUser(AbsUser):
    class Meta:
        ordering = ['username']

class User(AbsUser):
    host = models.ForeignKey('Host')
    class Meta:
        ordering = ['host','uid']

class Package(models.Model):
    pkgname = models.CharField(max_length = 100)
    version = models.CharField(max_length = 50)
    class Meta:
        ordering = ['pkgname','version']
    def __unicode__(self):
        return self.pkgname

class FStype (models.Model):
    fstype = models.CharField(max_length = 40)
    description = models.CharField(max_length = 40)
    class Meta:
        ordering = ['fstype']
    def __unicode__(self):
        return self.fstype

class FS(models.Model):
    device = models.CharField(max_length = 40)
    fstype = models.ForeignKey('FStype')
    size = models.DecimalField(max_digits=8,decimal_places=1)
    percent_used = models.IntegerField()
    mountpoint = models.CharField(max_length = 40)
    host = models.ForeignKey('Host')
    def get_size_gb(self):
        return "%.2f" % (self.size/1024)
    class Meta:
        ordering = ['host__hostname','mountpoint']
    def __unicode__(self):
        return self.mountpoint

class Interface (models.Model):
    INTERFACE_TYPES = (('NET','NET'),('FC','FC'))
    name = models.CharField(max_length=30) # eth0, etc
    type = models.CharField(max_length='10', choices=INTERFACE_TYPES)
    hwaddr = models.CharField(max_length=32) # mac, wwn
    ips = models.ManyToManyField('IP', related_name='interfaces', null=True, blank=True)
    host = models.ForeignKey('Host')
    linkstate = models.BooleanField() # True == Up, False == Down
    speed = models.CharField(max_length=32) # 'autoneg full-duplex 1GB' or '8GB'
    extra = models.CharField(max_length=50) # slaves if bonding or etherchannel
    class Meta:
        ordering = ['host', 'name']
    def __unicode__(self):
        return "%s_%s" % (self.host,self.name)

class IP (models.Model):
    ipaddr = models.CharField(max_length=40) # ip v4 ou v6
    netmask = models.CharField(max_length=40) # ip v4 ou v6
    class Meta:
        ordering = ['ipaddr']
    def __unicode__(self):
        return self.ipaddr

class Daemon (models.Model):
    name = models.CharField(max_length=40) # ntpd par ex
    #is_running = models.BooleanField() # True si il tourne effectivement
    hosts = models.ManyToManyField('Host',related_name='daemons', null=True, blank=True)
    class Meta:
        #ordering = ['is_running','name']
        ordering = ['name']
    def __unicode__(self):
        return self.name

class Netlink(models.Model):
    local_ip = models.CharField(max_length=40) # ip
    local_port = models.IntegerField() # port
    remote_ip = models.CharField(max_length=40) # ip
    remote_port = models.IntegerField() # port
    host = models.ForeignKey('Host',related_name='netlinks')
    def get_direction(self):
      '''TODO: implement direction detector'''
      return "<?>"
    class Meta:
        ordering = ['local_ip','local_port','remote_ip']
    def __unicode__(self):
        return "%s:%s %s %s:%s" % (local_ip,local_port,self.get_direction(),remote_ip,remote_port)

# not yet implemented in scritps
class AppCatalog(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=50)
    script = models.TextField()
    class Meta:
        ordering = ['name']
    def __unicode__(self):
        return self.name

class Application(models.Model):
    application = models.ForeignKey('AppCatalog')
    version = models.CharField(max_length = 50, null = True, blank = True)
    appdir = models.CharField(max_length = 50, null = True, blank = True)
    hosts = models.ManyToManyField('Host', related_name='applications', null=True, blank=True)
    class Meta:
        ordering = ['application', 'version']
    def __unicode__(self):
        return self.application.name
