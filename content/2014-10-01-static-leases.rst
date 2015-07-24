=============
Static leases
=============

:date: 2014-10-01 00:07:00
:slug: 20141001
:tags: openwrt, router, network, linux

My `netbook server <http://www.circuidipity.com/pingparade1.html>`_ stays put at home and uses a **fixed ip address**; however `Sidbook <http://www.circuidipity.com/c720-sidbook.html>`_ bounces between the LAN and the outside world. A router can use a **static lease** to assign a computer a fixed IP address based on their hardware (MAC) address. This allows Sidbook the flexibility of using DHCP both at home to retrieve a known and consistent IP address (useful for ssh access and running `backup scripts <https://github.com/vonbrownie/linux-home-bin/blob/master/backup-home-server>`_) and outside where an unknown range of IP addresses will be assigned at different locations and times.

To retrieve the hardware address on a Linux desktop using **Network Manager**, right-click on the network device icon and select *Connection Information*, or run the command ``ip -address`` in a console for more complete interface description.

For a router using `OpenWrt <http://www.circuidipity.com/pingparade4.html>`_, ssh into the device and create a static lease in ``/etc/config/dhcp``.

Sample entry:
 
.. code-block:: bash

    config host
            option name 'tyrell'
            option mac '01:2a:b3:4c:55:dd'
            option ip '192.168.1.55'

Alternately, use the `LuCI <http://www.circuidipity.com/pingparade4.html>`_ graphical config interface to create a static lease under ``Network->DHCP and DNS``.

Source: `DNS and DHCP configuration <http://wiki.openwrt.org/doc/uci/dhcp>`_

Happy hacking!
