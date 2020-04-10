"""
Simple Ryu Application to demonstrate OpenFlow switch blocking host
until it send a "magic" packet (UDP containing "xyzzy", eg, DNS)
(OpenFlow 1.3 only, simple single table example with only flooding)

For details see: http://www.naos.co.nz/talks/seize-control-with-ryu/

Written by Ewen McNeill <ewen@naos.co.nz>, 2014-09-09

Copyright (c) 2014 Naos Ltd
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from ryu.base               import app_manager
from ryu.controller         import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto            import ofproto_v1_3, ofproto_v1_3_parser, ether, inet
from ryu.lib.packet         import packet, ethernet, ipv4, tcp
import socket
import thread
import secrets


class FlowRider(app_manager.RyuApp):
  # Tell Ryu to only accept OpenFlow 1.3
  OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

  # Internal constants for ports, priority, etc
  MAGIC_COOKIE                 = bytearray(b"xyzzy")
  (PORT_H1, PORT_H2, PORT_H3)           = (1,2,3)
  (PRI_LOW, PRI_MID, PRI_HIGH) = (20, 30, 40)

  # Minimal __init__
  def __init__(self, *args, **kwargs):
    super(FlowRider, self).__init__(*args, **kwargs)

  # Helper to prepare format flow add messages
  def add_flow(self, dp, priority, match, actions):
    ofp    = dp.ofproto
    parser = dp.ofproto_parser

    inst = []
    if actions:
      inst = [parser.OFPInstructionActions(
                            ofp.OFPIT_APPLY_ACTIONS,
                            actions)]

    mod = parser.OFPFlowMod(datapath=dp, table_id=0,
                                priority=priority,
                                match=match, instructions=inst)
    dp.set_xid(mod)         # Preallocate transaction ID
    dp.send_msg(mod)

  # Helper to delete all flows (ie, reset to default)
  # (No filtering on delete, so deletes everything in table 0)
  def del_flows(self, dp):
    ofp    = dp.ofproto
    parser = dp.ofproto_parser

    wildcard_match = parser.OFPMatch()
    instructions   = []

    mod = parser.OFPFlowMod(datapath=dp, table_id=0,
                             command=ofp.OFPFC_DELETE,
                             out_port=ofp.OFPP_ANY,
                             out_group=ofp.OFPP_ANY,
                             match=wildcard_match,
                             instructions=instructions)

    dp.send_msg(mod)

  # Add flow to flood all arp packets, so ARP works
  def flood_all_arp(self, dp):
    ofp    = dp.ofproto
    parser = dp.ofproto_parser

    self.logger.info("Permitting ARP, by flooding")
    match   = parser.OFPMatch(eth_type = ether.ETH_TYPE_ARP)
    actions = [parser.OFPActionOutput(ofp.OFPP_FLOOD,
                                      ofp.OFPCML_NO_BUFFER)]
    self.add_flow(dp, FlowRider.PRI_MID,
                  match, actions)

  # Add override (high priority) to flood traffic from MAC
  def permit_traffic_from_mac(self, dp, src_mac):
    ofp    = dp.ofproto
    parser = dp.ofproto_parser

    self.logger.info("Permitting traffic from %s" % src_mac)
    match   = parser.OFPMatch(eth_src = src_mac)
    actions = [parser.OFPActionOutput(ofp.OFPP_FLOOD,
                                      ofp.OFPCML_NO_BUFFER)]
    self.add_flow(dp, FlowRider.PRI_MID,
                  match, actions)

  # Add (low priority) defaults that block traffic)
  def allow_traffic_by_default(self, dp):
    ofp    = dp.ofproto
    parser = dp.ofproto_parser

    self.logger.info("Clearing existing flows")
    self.del_flows(dp)

    self.logger.info("Allowing traffic from h1's port by default")
    match   = parser.OFPMatch(in_port = FlowRider.PORT_H1)
    actions = [parser.OFPActionOutput(ofp.OFPP_FLOOD,
                                      ofp.OFPCML_NO_BUFFER)]
    self.add_flow(dp, FlowRider.PRI_LOW,
                  match, actions)

    self.logger.info("Allowing traffic from h2's port by default")
    match   = parser.OFPMatch(in_port = FlowRider.PORT_H2)
    actions = [parser.OFPActionOutput(ofp.OFPP_FLOOD,
                                      ofp.OFPCML_NO_BUFFER)]
    self.add_flow(dp, FlowRider.PRI_LOW,
                  match, actions)

    self.logger.info("Allowing traffic from h3's port by default")
    match   = parser.OFPMatch(in_port = FlowRider.PORT_H3)
    actions = [parser.OFPActionOutput(ofp.OFPP_FLOOD,
                                      ofp.OFPCML_NO_BUFFER)]
    self.add_flow(dp, FlowRider.PRI_LOW,
                  match, actions)


  # Ask switch to send us UDP packets from host 1
  def add_notify_on_udp_from_host_1(self, dp):
    ofp    = dp.ofproto
    parser = dp.ofproto_parser

    self.logger.info("Request notify on UDP from h1")
    match   = parser.OFPMatch(in_port  = FlowRider.PORT_H1,
                              eth_type = ether.ETH_TYPE_IP,
                              ip_proto = inet.IPPROTO_UDP)
    actions = [parser.OFPActionOutput(ofp.OFPP_CONTROLLER,
                                      ofp.OFPCML_NO_BUFFER)]
    self.add_flow(dp, FlowRider.PRI_MID,
                  match, actions)



  def add_notify_on_tcp_from_host_1(self, dp):
    ofp    = dp.ofproto
    parser = dp.ofproto_parser
    self.logger.info("Request notify on TCP from h1")
    match  = parser.OFPMatch(in_port  = FlowRider.PORT_H1,
                               eth_type = ether.ETH_TYPE_IP,
                               ip_proto = inet.IPPROTO_TCP)
    actions = [parser.OFPActionOutput(ofp.OFPP_CONTROLLER,
                                       ofp.OFPCML_NO_BUFFER)]
    self.add_flow(dp, FlowRider.PRI_HIGH,
                   match, actions)

  # Ask switch to send us SYN packets from host 1
  #def add_notify_on_syn_from_host_1(self, dp):
#      ofp    = dp.ofproto_v1_3
#      parser = dp.ofproto_v1_3_parser

#      self.logger.info("Request notify on SYN packets from h1")
#      match   = parser.OFPMatch(in_port  = FlowRider.PORT_H1,
#      eth_type = ether.ETH_TYPE_IP,
#      ip_proto = inet.IPPROTO_TCP,
#      tcp_flags = tcp.TCP_SYN)
#      actions = [parser.OFPActionOutput(ofp.OFPP_CONTROLLER,
#      ofp.OFPCML_NO_BUFFER)]
#      self.add_flow(dp, FlowRider.PRI_MID,
#      match, actions)

  @set_ev_cls(ofp_event.EventOFPStateChange,
              MAIN_DISPATCHER)
  def new_connection(self, ev):
    dp = ev.datapath
    self.logger.info("Switch connected (id=%s)" % dp.id)
    self.allow_traffic_by_default(dp)
    self.flood_all_arp(dp)
    self.add_notify_on_udp_from_host_1(dp)
    self.add_notify_on_tcp_from_host_1(dp)

  @set_ev_cls(ofp_event.EventOFPPacketIn,
              MAIN_DISPATCHER)
  def handle_packet(self, ev):
    pkt = packet.Packet(ev.msg.data)
    eth = pkt.get_protocol(ethernet.ethernet)
    ipv4 = pkt.get_protocol(ipv4.ipv4)
    #self.logger.info("UDP received from %s" % pkt)
    #self.logger.info("UDP received from %s" % eth.src)
    self.logger.info("Connection attempt from from %s to %s" % ipv4.src, ipv4.dst)
    self.logger.info("TCP packet, sending out keys")
    #key = self.make_key()
    self.send_key('172.31.1.2')
    #self.send_key('172.31.1.1')
    self.permit_traffic_from_mac(ev.msg.datapath, eth.src)

   # Send key when triggered
  def send_key(self, HOST):
    PORT = 5000          # The port used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.logger.info("Connecting to the endpoint")
    s.connect((HOST, PORT))
    self.logger.info("Sending key information to %s" % HOST)
    #s.sendall(key)
    s.sendall(b'THIS IS THE PRE-SHARED KEY.')
    print('Key distribution done')
    s.close()

  def make_key(self):
    key = secrets.token_hex(128)
    return key
