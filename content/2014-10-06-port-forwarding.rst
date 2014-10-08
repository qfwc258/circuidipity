===============
Port forwarding
===============

:date: 2014-10-06 14:58:00
:slug: 20141006
:tags: networks, openwrt, linux

**Port forwarding** enables `SSH access <http://www.circuidipity.com/pingparade2.html>`_ to my `home server <http://www.circuidipity.com/pingparade1.html>`_ from outside the home by forwarding traffic directed at a port on the router (reachable over the Internet by static IP) to the SSH port on the internal server behind a `NAT firewall <http://wiki.openwrt.org/doc/uci/firewall>`_.

`OpenWrt <http://www.circuidipity.com/pingparade4.html>`_ port forward configuration is done in ``/etc/config/firewall``. A sample entry that redirects port 55555 on the router to port 22 on the server...

.. code-block:: bash

    config 'redirect'
        option 'name' 'ssh'
        option 'src' 'wan'
        option 'proto' 'tcpudp'
        option 'src_dport' '55555'
        option 'dest_ip' '192.168.1.55'
        option 'dest_port' '22'
        option 'target' 'DNAT'
        option 'dest' 'lan'

Save and make the changes active by running ``/etc/init.d/firewall restart``.

Alternately, setup port forwarding in LuCI under ``Network->Firewall->Port Forwards``.

Source: `OpenWrt Port Forwarding <http://wiki.openwrt.org/doc/howto/port.forwarding>`_
