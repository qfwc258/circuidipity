=======================
Dynamic DNS and OpenWRT
=======================

:date: 2015-02-06 00:02:00
:slug: ddns-openwrt
:tags: network, openwrt, linux
:modifed: 2015-02-08 18:08:00 

`Raspberry Pi Home Server Hack #5 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ Access a home server from anywhere using **Dynamic DNS** (DDNS).

Let's go!
=========

My Raspberry Pi server sits behind a router assigned a **dynamic IP address** by the ISP. If I want to connect to my Pi over the Internet from anywhere in the world I can use a **DDNS service** to create a domain name that automatically updates the IP address in the background whenever it changes and redirect traffic to the new location.

0. Select a DDNS service
========================

I chose the free DDNS service `duckdns.org <http://www.duckdns.org/>`_ which permits the creation of up to 4 domains in the format ``your_subdomain_choice.duckdns.org``. Example: Create the subdomain ``mypihomeserver`` and later - after configuring the router - when entering ``mypihomeserver.duckdns.org`` I will be redirected to the current IP address assigned to my home network.

Make note of `duckdns.org/install <http://www.duckdns.org/install.jsp>`_ (while logged in) for customized settings useful for configuring the router for DDNS.

1. Configure OpenWRT for notification
=====================================

Different routers configure DDNS differently but the goal is the same: the ability to notify the DDNS service whenever the IP address assigned by the ISP is modified. I am using an `OpenWRT-powered router <http://www.circuidipity.com/supercharge-a-home-router-using-openwrt-pt2.html>`_ and these are the steps to configure OpenWRT to use duckdns DDNS.

Install DDNS packages:

.. code-block:: bash

    # opkg update                                                                         
    # opkg install luci-app-ddns ddns-scripts                                             
                                                                                    
Use the customized settings from `duckdns.org/install <http://www.duckdns.org/install.jsp>`_ to configure ``/etc/config/ddns``:
      
.. code-block:: bash

    config service          "duckdns"
    option enabled          "1"
    option service_name     "duckdns.org"
    option domain           "mypihomeserver"
    option username         "NA"
    option password         "string_of_letters_and_digits"
    option ip_source        "network"
    option ip_network       "wan"
    option force_interval   "72"                                   
    option force_unit       "hours"                                
    option check_interval   "10"                                   
    option check_unit       "minutes"
    option update_url       "http://www.duckdns.org/update?domains=[DOMAIN]&token=[PASSWORD]&ip=[IP]"
    option use_syslog       "1"

Start daemon:

.. code-block:: bash

    # sh
    # . /usr/lib/ddns/dynamic_dns_functions.sh
    # start_daemon_for_all_ddns_sections "wan"
    # exit

Test:

.. code-block:: bash

    # /usr/lib/ddns/dynamic_dns_updater.sh duckdns

In OpenWRT's ``LuCI`` interface navigate to ``System->Startup`` and enable DDNS to ensure the router continues to send IP address changes after reboot and hotplug events.
                                                                                    
Source: `OpenWRT DDNS client <http://wiki.openwrt.org/doc/howto/ddns.client>`_

2. Port forwarding
==================

`Port forwarding <http://www.circuidipity.com/20141006.html>`_ configures OpenWRT to forward traffic directed at one of the router's ports to the listening port on the Pi home server. Example: configure ``port:55555`` on router to connect to the `SSH server <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ listening on ``port:22`` on Pi.

Happy hacking!
