==============================================
Supercharge a home router using OpenWrt Part 2
==============================================

:date: 2015-02-08 18:16:00
:slug: supercharge-a-home-router-using-openwrt-pt2
:tags: networks, openwrt, linux

**Previous:** `TL-WR841N <http://www.circuidipity.com/pingparade4.html>`_

A **home router** is a much more capable device than its pre-installed software would lead you to believe. `OpenWrt <https://openwrt.org/>`_ is an embedded Linux distribution that converts cheap, energy-efficient, network-capable devices into much more useful hackable computers.

Getting its start hacking the original `Linksys WRT54G <https://en.wikipedia.org/wiki/Linksys_WRT54G_series#WRT54G>`_, OpenWrt and its volunteer developers now support a `wide and growing range of hardware <http://wiki.openwrt.org/toh/start>`_. The project hosts software packages that lay out a smorgasboard of extra possibilities: more network tools with more fine-grained controls, plus a range of server capabilities... manage printers, connect external USB drives for backup, host files/torrents/VOIP/VPNs.

I replaced the default firmware and now exploring an OpenWrt-supported `TP-Link TL-WDR3600 <http://wiki.openwrt.org/toh/tp-link/tl-wdr3600>`_ router:

* dual 2.4GHz 802.11bgn and 5GHz 802.11an wifi with detachable antennas
* 4 Port 10/100/1000 LAN
* 1 Port 10/100/1000 WAN
* 2 USB 2.0 Ports
* 64 MB Flash + 128MB RAM
* [my device has] firmware: 3.13.34 build 130909 rel. 53148n hardware **version: v1.5**

Let's go!
=========

0. Download install image
=========================

.. role:: warning

:warning:`WARNING!` OpenWrt builds different install images for different devices. Consult the `Table of Hardware <http://wiki.openwrt.org/toh/start>`_ to confirm that your router is supported and read the wiki entry for your particular device to identify the correct image. It is **easy to brick a device** (render inoperable) using an incorrect install image.

Latest version (2015-02-08) of OpenWrt is **v14.07 "Barrie Breaker"** and TL-WDR3600 is an **ar71xx** device. Download the appropriate install image:

[Link] `openwrt-ar71xx-generic-tl-wdr3600-v1-squashfs-factory.bin <https://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/openwrt-ar71xx-generic-tl-wdr3600-v1-squashfs-factory.bin>`_

1. Flash router
===============

Log into the TP-Link router web interface ``address=192.168.0.1`` ``user=admin`` ``password=admin`` navigate to the update page ``System Tools->Firmware Upgrade`` and select the downloaded ``openwrt-*-squashfs-factory.bin`` firmware image as the update package. Allow several minutes for the device to write the new OpenWrt firmware; when finished the device will reboot and accessible at new IP address ``192.168.1.1``.

2. First login
==============

`Use telnet (no password) to login for the first time <http://wiki.openwrt.org/doc/howto/firstlogin>`_ to the new OpenWrt installation. Use ``passwd`` to create a new root password. After changing the password telnet is disabled. Exit and re-login using SSH:

.. code-block:: bash

    $ ssh root@192.168.1.1

`Setup your internet connection <http://wiki.openwrt.org/doc/howto/internet.connection>`_ either by editing ``/etc/config/network`` or using OpenWrt's **Unified Configuration Interface (UCI)**. Using my DSL (pppoe) as an example:

.. code-block:: bash

    # uci set network.wan.proto=pppoe
    # uci set network.wan.username='yougotthisfromyour@isp.su'
    # uci set network.wan.password='yourpassword'
    # uci commit network
    # ifup wan

3. Web interface
================

OpenWrt can be further configured in the console or the `LuCI web interface <http://wiki.openwrt.org/doc/howto/luci.essentials>`_. LuCI is included by default in the WDR3600 image, otherwise it can be installed using the ``opkg`` package manager:

.. code-block:: bash

    # opkg update
    # opkg install luci

If installed manually LuCI will not be running:

.. code-block:: bash

    # /etc/init.d/uhttpd start    # start the web server
    # /etc/init.d/uhttpd enable   # auto-start at boot

LuCI's default web server **uhttpd** is configured in ``/etc/config/uhttpd`` and LuCI itself is configured in ``/etc/config/luci``.

.. image:: images/pingparade4-1.png
    :alt: LuCI login
    :width: 960px
    :height: 300px

4. Configuration
================

Secure access to the router using `SSH key authentication <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_. Create `static leases <http://www.circuidipity.com/20141001.html>`_ for hosts using DHCP and setup `port forwarding <http://www.circuidipity.com/20141006.html>`_ to reach devices behind the firewall from the world-at-large.

Its exciting what you can do with these consumer routers once you let it sink in that - with a few dollars and OpenWrt - you have an extremely configurable general purpose computer.

Happy hacking!
