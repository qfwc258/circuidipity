===============================================
OpenWrt router as bridged repeater using relayd
===============================================

:date: 2015-06-26
:slug: openwrt-bridged-repeater
:tags: openwrt, linux, network

Extend the range of a wireless network using a cheap and cheerful router running `OpenWrt <http://www.circuidipity.com/tag-openwrt.html>`_ as a **bridged repeater**. All client devices use the same IP address range and are capable of communicating with each other.

Let's go!
=========

Wireless access points: **PrimaryAP** is a `TP-Link TL-WDR3600 <http://www.circuidipity.com/supercharge-a-home-router-using-openwrt-pt2.html>`_ with IP address ``192.168.1.1`` + wireless channel ``11`` and the **RepeaterAP** is a `TP-Link TL-WR841N <http://www.circuidipity.com/pingparade4.html>`_ (~$25CAN). Both devices are running OpenWrt.

`This thread <https://forum.openwrt.org/viewtopic.php?id=39077>`_ was a big help in cutting through the confusion and getting everything hopping! Basically there are 2 types of repeater scenarios to consider:

* *non-bridged* repeater - works on all radios... devices connected to the *RepeaterAP* see the *PrimaryAP* devices, *PrimaryAP* devices do not see *RepeaterAP* devices
* *bridged* repeater - works for most radios... everything sees everything

All configuration is done on the secondary router to setup device as a bridged repeater.

0. Install relayd
=================

Access the internet by connecting an ethernet cable from the secondary router's WAN port to the primary router. Login and install ``relayd``:

.. code-block:: bash

    # opkg update                                                                          
    # opkg install relayd                                                                  
    # /etc/init.d/relayd enable                                                            

1. Configure wireless
=====================

Sample ``/etc/config/wireless``:

.. code-block:: bash

    config wifi-device 'radio0'                                                        
        option type 'mac80211'                                                         
        option channel '11'     # Important! Match with the channel set on PrimaryAP                                                            
        option hwmode '11g'                                                            
        option path 'platform/ar934x_wmac'                                             
        option htmode 'HT20'                                                           
        option txpower '30'                                                            
        option country 'US'                                                            
                                                                                   
    config wifi-iface                                                                  
        option device 'radio0'                                                         
        option network 'wwan'                                                          
        option encryption 'psk2'                                                       
        option key '*********************'                                             
        option mode 'sta'                                                              
        option ssid 'PrimaryAP'                                                        
                                                                                   
    config wifi-iface                                                                  
        option device 'radio0'                                                         
        option network 'lan'                                                       
        option encryption 'psk2'                                                   
        option key '*****************'                                             
        option mode 'ap'                                                           
        option ssid 'RepeaterAP'

2. Configure network
====================

Sample ``/etc/config/network``:

.. code-block:: bash

    config interface 'loopback'                                                        
        option ifname 'lo'                                                             
        option proto 'static'                                                          
        option ipaddr '127.0.0.1'                                                      
        option netmask '255.0.0.0'                                                     
                                                                                   
    config interface 'lan'                                                             
        option ifname 'eth0'                                                           
        option force_link '1'                                                          
        option type 'bridge'                                                           
        option proto 'static'                                                          
        option ip6assign '60'                                                          
        option ipaddr '192.168.10.1'    # for relayd... requires 192.168.x.x address but not used by clients
        option gateway '192.168.1.1'    # ip address of PrimaryAP                      
        option netmask '255.255.255.0'                                                 
        option dns '192.168.1.1'                                                       
                                                                                   
    config interface 'wwan'                                                            
        option proto 'static'                                                          
        option ipaddr '192.168.1.254'                                                  
        option netmask '255.255.255.0'                                                 
        option gateway '192.168.1.1'                                                   
                                                                                   
    config interface 'stabridge'                                                       
        option proto 'relay'                                                           
        option network 'lan wwan'                                                      
        option ipaddr '192.168.1.254'   # static ip assigned from PrimaryAP address range         
                                                                                   
    config switch                                                                      
        option name 'switch0'                                                          
        option reset '1'                                                               
        option enable_vlan '1'                                                         
                                                                                   
    config switch_vlan                                                                 
        option device 'switch0'                                                        
        option vlan '1'                                                                
        option ports '0 1 2 3 4'
                                                               
3. Configure DHCP
=================

*PrimaryAP* will handle DHCP for the combined network. Sample ``/etc/config/dhcp``:

.. code-block:: bash

    config dhcp 'lan'                                                                  
        option interface 'lan'                                                         
        option start '100'                                                             
        option limit '150'                                                             
        option leasetime '12h'                                                         
        option ignore '1'                                                              
                                                                                   
    config dhcp 'wan'                                                                  
        option interface 'wan'                                                         
        option ignore '1'

4. Reboot
=========

*PrimaryAP* will handle firewall and dnsmasq for the combined network. Disable the services on *RepeaterAP* to avoid conflicts:

.. code-block:: bash

    # /etc/init.d/firewall stop                                                            
    # /etc/init.d/firewall disable                                                         
    # /etc/init.d/dnsmasq stop                                                             
    # /etc/init.d/dnsmasq disable                                                          
      
Reboot router:

.. code-block:: bash
                                                                               
    # reboot

OK! Connect to the new *RepeaterAP* and the device will be assigned an IP address on the *PrimaryAP*'s now-extended network. All rules and services on *PrimaryAP* will flow through to devices connected via *RepeaterAP*.

5. Helpful resources
====================

* My `wireless <https://github.com/vonbrownie/linux-post-install/blob/master/config/openwrt/bridged_repeater/etc/config/wireless>`_, `network <https://github.com/vonbrownie/linux-post-install/blob/master/config/openwrt/bridged_repeater/etc/config/network>`_, and `dhcp <https://github.com/vonbrownie/linux-post-install/blob/master/config/openwrt/bridged_repeater/etc/config/dhcp>`_ configs
* OpenWrt forum thread on `bridged and simple repeater configurations <https://forum.openwrt.org/viewtopic.php?id=39077>`_
* `Routed Client with relayd (Pseudobridge) <http://wiki.openwrt.org/doc/recipes/relayclient>`_

Happy hacking!
