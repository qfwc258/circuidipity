====================================
OpenWrt surgery on more home routers
====================================

:date: 2015-02-08 18:16:00
:slug: supercharge-a-home-router-using-openwrt-pt2
:tags: openwrt, router, linux, network
:modified: 2015-07-16 15:05:00
           
Home routers are more capable than default firmware would lead you to believe. I replace that firmware with `OpenWrt <https://openwrt.org/>`_: an embedded Linux distribution that converts energy-efficient, network-capable devices into much more useful hackable computers.

Install and first login
=======================

`Supercharge a home router using OpenWrt <http://www.circuidipity.com/pingparade4.html>`_ on a **TP-Link TL-WR841N** (~$25CAN) I currently use as a `bridged repeater <http://www.circuidipity.com/openwrt-bridged-repeater.html>`_.

More routers
============

.. role:: warning

:warning:`WARNING!` OpenWrt builds different install images for different devices. Consult the `Table of Hardware <http://wiki.openwrt.org/toh/start>`_ to confirm that your router is supported and read the wiki entry for your particular device to identify the correct image. It is **easy to brick a device** (render inoperable) using an incorrect install image.

TP-Link TL-MR3420
-----------------

Specs:

* 802.11bgn with (2) detachable antennas
* 4 Port 10/100 LAN
* 1 Port WAN
* 1 USB 2.0 Port
* hardware version: 1.2
* running ``Chaos Calmer 15.05-rc2``: `openwrt-15.05-rc2-ar71xx-generic-tl-mr3420-v1-squashfs-factory.bin <https://downloads.openwrt.org/chaos_calmer/15.05-rc2/ar71xx/generic/openwrt-15.05-rc2-ar71xx-generic-tl-mr3420-v1-squashfs-factory.bin>`_

Router was acquired used and its default TP-Link firmware had been previously configured:

* Reset router to factory defaults ``System Tools->Factory Defaults`` and device reboots
* Access at address ``192.168.1.1`` with ``user: admin / password: admin``
* Use ``System Tools->Firmware Upgrade`` to upload the OpenWrt image and flash router
  
If the TP-Link uploader balks at the OpenWrt image filename (mine did) then rename the file to a TP-Link-compatible firmware name. Example:

.. code-block:: bash

    $ mv openwrt*squashfs-factory.bin mr3420v1_en_3_13_1_up\(121123\).bin
  
My intention is to use this router on a separate address range attached to my home LAN as a playground for network experiments.

TP-Link TL-WR1043ND
-------------------

Specs:

* 802.11bgn with (3) detachable antennas
* 4 Port 10/100/1000 LAN
* 1 Port WAN
* 1 USB 2.0 Port
* 8MB Flash + 32MB RAM
* hardware version: v1.8
* running ``Barrier Breaker v14.07``: `openwrt-ar71xx-generic-tl-wdr3600-v1-squashfs-factory.bin <https://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/openwrt-ar71xx-generic-tl-wdr3600-v1-squashfs-factory.bin>`_

This is my primary home router.

TP-Link TL-WDR3600
------------------

Specs:

* dual 2.4GHz 802.11bgn and 5GHz 802.11an with (2) detachable antennas
* 4 Port 10/100/1000 LAN
* 1 Port WAN
* 2 USB 2.0 Ports
* 64MB Flash + 128MB RAM
* hardware version: v1.5
* running ``Barrier Breaker v14.07``: `openwrt-ar71xx-generic-tl-wdr3600-v1-squashfs-factory.bin <https://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/openwrt-ar71xx-generic-tl-wdr3600-v1-squashfs-factory.bin>`_

I have setup this router model for family members and friends.

Happy hacking!
