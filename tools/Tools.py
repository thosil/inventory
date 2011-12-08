from hosts.models import *

def get_size(mount):
    size=used=0
    mountpoints=[]
    for fs in FS.objects.filter(mountpoint__iregex=mount):
        size += fs.size
        used += fs.size / 100 * fs.percent_used
        if fs.mountpoint not in mountpoints: mountpoints.append(fs.mountpoint)
    return (mountpoints,size/1024, used/1024)

