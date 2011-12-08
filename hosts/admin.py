from inventaires.hosts.models import *

from django.contrib import admin

class DiskInline(admin.TabularInline):
    model = Disk
    extra = 1

class HostAdmin(admin.ModelAdmin):
    def upper_case(self,obj):
        return obj.hostname.upper()
    upper_case.short_description = 'Hostname'
    list_display = ['upper_case','os','cpu','gbmem','client','vlan']
    search_fields = ['hostname']
    list_filter = ['client','os','vlan', 'cpu']
    save_as = True
    inlines = [DiskInline]
    exclude = ('packages',)

class VlanAdmin(admin.ModelAdmin):
    list_display=['vlannumber','vlanname','network','netmask','gateway','dns1','dns2','ntp']
    search_fields = ['vlannumber','vlanname','network']
    list_filter = ['netmask']

class OSAdmin(admin.ModelAdmin):
    pass

class MembershipInline(admin.TabularInline):
    model = Group.members.through

class UserAdmin(admin.ModelAdmin):
    list_display = ['uid','username','gecos','shell','host']
    inlines = [MembershipInline]
    list_filter = ['shell','username']

class ExternalUserAdmin(admin.ModelAdmin):
    list_display = ['uid','username','gid','gecos','home','shell']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['groupname','host']
    inlines = [MembershipInline]
    exclude = ['members',]

admin.site.register(Host, HostAdmin)
admin.site.register(Client)
admin.site.register(OS, OSAdmin)
admin.site.register(Vlan, VlanAdmin)
#admin.site.register(Disk)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ExternalUser, ExternalUserAdmin)
