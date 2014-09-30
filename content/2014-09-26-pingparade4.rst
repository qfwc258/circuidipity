=========================
Ping Parade #4 -- Breaker
=========================

:date: 2014-09-26 21:10:00
:slug: pingparade4
:tags: networks, openwrt, linux
:template: article-project-pingparade

**Unlock the full potential of your home router using OpenWrt.**

.. image:: images/pingparade4-0.png
    :alt: OpenWRT
    :width: 960px
    :height: 500px

A **home router** is a much more capable device than its pre-installed software would lead you to believe. `OpenWrt <https://openwrt.org/>`_ is an embedded Linux distribution that converts cheap, energy-efficient, network-capable devices into much more useful hackable computers.

Getting its start hacking the original `Linksys WRT54G <https://en.wikipedia.org/wiki/Linksys_WRT54G_series#WRT54G>`_, OpenWrt and its volunteer developers now support a `wide and growing range of hardware <http://wiki.openwrt.org/toh/start>`_. The project hosts software packages that lay out a smorgasboard of extra possibilities: more network tools with more fine-grained controls, plus a range of server capabilities... manage printers, connect external USB drives for backup, host files/torrents/VOIP/VPNs.

I am currently using an OpenWrt-supported `TP-Link TL-WR841N <http://wiki.openwrt.org/toh/tp-link/tl-wr841nd>`_ wireless N router, an inexpensive ($20-25CDN) device with:

* 2 antennas (on the otherwise identical TL-WR841ND they are detachable)
* 4 Port 100/10 LAN
* 1 Port 100/10 WAN
* 4 MB Flash + 32MB RAM
* [my device has] firmware: 3.14.3 build 131011 rel. 55505n hardware **version: v8**

Not much flash storage for added packages but its a cheap and cheerful device to hack on. It has been running `Barrier Breaker <http://wiki.openwrt.org/doc/barrier.breaker>`_  - the release candidate of the next upcoming version of OpenWrt - with no problems for the last few months.

Below are the steps to replace the default router firmware with OpenWrt. I am using my TL-WR841N as an example. Good luck!

Step 0 - Download install image
===============================

.. warning::

    OpenWrt builds different install images for different devices. Consult the `Table of Hardware <http://wiki.openwrt.org/toh/start>`_ to confirm that your router is supported and read the wiki entry for your particular device to identify the correct image. It is **easy to brick a device** (render inoperable) using an incorrect install image.

TL-WR841N is an **ar71xx** device. Download the most recent devel VERSION (=14.07-rc3 as of 9-26):

[Sample link] http://downloads.openwrt.org/barrier_breaker/VERSION/ar71xx/generic/openwrt-ar71xx-generic-tl-wr841n-v8-squashfs-factory.bin

Step 1 - Flash router
=====================

Log into the TP-Link router web interface - address=192.168.0.1, user=admin, pass=admin - navigate to the update page and select the downloaded ``openwrt-*-squashfs-factory.bin`` firmware image as the update package. Allow several minutes for the device to write the new OpenWrt firmware; when finished the device will reboot and can be accessed at address=192.168.1.1.

Step 2 - First login
====================

`Use telnet (no password) to login for the first time <http://wiki.openwrt.org/doc/howto/firstlogin>`_ to the new OpenWrt installation. Use ``passwd`` to create a new root password. Once the password is properly configured telnet is disabled. Exit and re-login using ``ssh root@192.168.1.1`` and the new password.

`Setup your internet connection <http://wiki.openwrt.org/doc/howto/internet.connection>`_ either by editing ``/etc/config/network`` or using OpenWrt's *Unified Configuration Interface* (UCI). Using my DSL (pppoe) as an example...

.. code-block:: bash

    uci set network.wan.proto=pppoe
    uci set network.wan.username='yougotthisfromyour@isp.su'
    uci set network.wan.password='yourpassword'
    uci commit network
    ifup wan

Step 3 - Web interface
======================

OpenWrt can be further configured in the console or install the optional `LuCI web interface <http://wiki.openwrt.org/doc/howto/luci.essentials>`_ using the **opkg** package manager...

.. code-block:: bash

    opkg update
    opkg install luci

.. note::

    With only 4MB flash to play with there is less than 256K remaining in ``rootfs/overlay`` for more packages after installing LuCI.

After install LuCI is not running by default...

.. code-block:: bash

    /etc/init.d/uhttpd start    # start the web server
    /etc/init.d/uhttpd enable   # auto-start at boot

LuCI's default web server **uhttpd** is configured in ``/etc/config/uhttpd`` and LuCI itself is configured in ``/etc/config/luci``.

.. image:: images/pingparade4-1.png
    :alt: LuCI login
    :width: 960px
    :height: 300px

Step 4 - Configuration
======================

Secure access to the router using `SSH key authentication <http://www.circuidipity.com/pingparade2.html>`_. Create `static leases <http://www.circuidipity.com/20141001.html>`_ for hosts using DHCP.

Its exciting what you can do with these consumer routers once you let it sink in that - with a few dollars and OpenWrt - you have an extremely configurable general purpose computer.

Happy hacking!
