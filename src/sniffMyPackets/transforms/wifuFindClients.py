#!/usr/bin/env python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from common.entities import SniffmypacketsEntity, monitorInterface, wifuClient
from canari.maltego.utils import debug, progress
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
    label='Sniff for WiFi Clients [U]',
    description='Listens for wifi probe responses on specified mon0 interface',
    uuids=[ 'sniffMyPackets.v2.sniffProbeResponses' ],
    inputs=[ ( 'sniffMyPackets', monitorInterface ) ],
    debug=True
)
def dotransform(request, response):
  
    clients = []
    interface = request.value
    
    def sniffProbe(p):
	  if p.haslayer(Dot11ProbeResp):
		ssid = p.getlayer(Dot11ProbeResp).info
		cmac = p.getlayer(Dot11).addr1
		bssid = p.getlayer(Dot11).addr2
		entity = ssid, cmac, bssid
		if entity not in clients:
		  clients.append(entity)
    
    sniff(iface=interface, prn=sniffProbe, count=500)
    for ssid, cmac, bssid in clients:
      e = wifuClient(cmac)
      e.clientBSSID = bssid
      e.monInt = interface
      e.clientSSID = ssid
      response += e
    return response