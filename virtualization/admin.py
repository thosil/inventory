from inventaires.virtualization.models import *
from django.contrib import admin

class VirtGroupAdmin(admin.ModelAdmin):
    pass

class HyperVisorAdmin(admin.ModelAdmin):
    pass

class FrameAdmin(admin.ModelAdmin):
    pass

class VMAdmin(admin.ModelAdmin):
    pass

admin.site.register(VirtGroup,VirtGroupAdmin)
admin.site.register(HyperVisor,HyperVisorAdmin)
admin.site.register(Frame,FrameAdmin)
admin.site.register(VM,VMAdmin)
