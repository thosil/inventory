#!/usr/bin/env python

'''
# from a file named vlans.txt which contains lines like this:
#4    ETB-ISABEL_195.122.96.129/29     active
#5    NET-P2PB0-MGT_172.17.0.208/30    active
#6    NET-P2PB4-MGT_153.89.254.128/29  active
# output this:
#vlannumber;vlanname;network;netmask
#4;ETB-ISABEL;195.122.96.129;255.255.255.248
#5;NET-P2PB0-MGT;172.17.0.208;255.255.255.252
#6;NET-P2PB4-MGT;153.89.254.128;255.255.255.248

echo "vlannumber vlanname network netmaks" > clean_vlans.csv
awk '$2 ~/_.*\..*\..*\..*\//{
gsub("/|_"," ",$2)
print $1,$2
}' vlans.txt | awk '{
if($4 == '1') {$4="128.0.0.0"}
if($4 == '2') {$4="192.0.0.0"}
if($4 == '3') {$4="224.0.0.0"}
if($4 == '4') {$4="240.0.0.0"}
if($4 == '5') {$4="248.0.0.0"}
if($4 == '6') {$4="252.0.0.0"}
if($4 == '7') {$4="254.0.0.0"}
if($4 == '8') {$4="255.0.0.0"}
if($4 == '9') {$4="255.128.0.0"}
if($4 == '10') {$4="255.192.0.0"}
if($4 == '11') {$4="255.224.0.0"}
if($4 == '12') {$4="255.240.0.0"}
if($4 == '13') {$4="255.248.0.0"}
if($4 == '14') {$4="255.252.0.0"}
if($4 == '15') {$4="255.254.0.0"}
if($4 == '16') {$4="255.255.0.0"}
if($4 == '17') {$4="255.255.128.0"}
if($4 == '18') {$4="255.255.192.0"}
if($4 == '19') {$4="255.255.224.0"}
if($4 == '20') {$4="255.255.240.0"}
if($4 == '21') {$4="255.255.248.0"}
if($4 == '22') {$4="255.255.252.0"}
if($4 == '23') {$4="255.255.254.0"}
if($4 == '24') {$4="255.255.255.0"}
if($4 == '25') {$4="255.255.255.128"}
if($4 == '26') {$4="255.255.255.192"}
if($4 == '27') {$4="255.255.255.224"}
if($4 == '28') {$4="255.255.255.240"}
if($4 == '29') {$4="255.255.255.248"}
if($4 == '30') {$4="255.255.255.252"}
if($4 == '31') {$4="255.255.255.254"}
if($4 == '32') {$4="255.255.255.255"}
print $0
}' >> clean_vlans.csv
sed -i 's/\ /;/g' clean_vlans.csv
'''
import csv
import os
from django.core.management import setup_environ
import settings
setup_environ(settings)
from hosts.models import Vlan

netmaskreader = csv.DictReader(open('~/Desktop/clean_vlans.csv','rb'), delimiter=';')
netmasks=[]
for row in netmaskreader:
	vlan = Vlan(vlannumber = row['vlannumber'],
	            vlanname = row['vlanname'],
		    network = row['network'],
		    netmask = row['netmask'])
	try:
		vlan.validate_unique()
		vlan.save()
	except :
		print "can't save vlan %s" % vlan.vlannumber
'''
now in db:
+------------+-----------------+------+------+-----------------+-----+--------------------+--------+------+---------+
| vlannumber | network         | dns2 | dns1 | netmask         | id  | vlanname           | domain | ntp  | gateway |
+------------+-----------------+------+------+-----------------+-----+--------------------+--------+------+---------+
|          4 | 195.122.96.129  | NULL | NULL | 255.255.255.248 |   3 | ETB-ISABEL         | NULL   | NULL | NULL    |
|          5 | 172.17.0.208    | NULL | NULL | 255.255.255.252 |   4 | NET-P2PB0-MGT      | NULL   | NULL | NULL    |
|          6 | 153.89.254.128  | NULL | NULL | 255.255.255.248 |   5 | NET-P2PB4-MGT      | NULL   | NULL | NULL    |
'''
