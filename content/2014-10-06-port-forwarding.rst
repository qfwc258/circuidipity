===============
Port forwarding
===============

:date: 2014-10-06 14:58:00
:slug: 20141006
:tags: networks, openwrt, linux
:modified: 2015-02-10 20:05:00

**Port forwarding** enables `SSH access <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ to my `Raspberry Pi home server <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ from outside the home by forwarding traffic directed at a port on the router (reachable over the Internet by `dynamic DDNS <http://www.circuidipity.com/ddns-openwrt.html>`_) to the SSH port on the internal server behind a `NAT firewall <http://wiki.openwrt.org/doc/uci/firewall>`_.

`OpenWrt <http://www.circuidipity.com/supercharge-a-home-router-using-openwrt-pt2.html>`_ port forward configuration is done in ``/etc/config/firewall``. A sample entry that redirects port ``55555`` on the router to the SSH server listening on port ``22`` at ``192.168.1.88``:

.. code-block:: bash

    config 'redirect'
        option 'name' 'ssh'
        option 'src' 'wan'
        option 'proto' 'tcpudp'
        option 'src_dport' '55555'
        option 'dest_ip' '192.168.1.88'
        option 'dest_port' '22'
        option 'target' 'DNAT'
        option 'dest' 'lan'

Save and make the changes active by running:

.. code-block:: bash

    # /etc/init.d/firewall restart

Alternately, setup port forwarding in LuCI under ``Network->Firewall->Port Forwards``.

Example-in-action: To SSH login outside the home enter ``ssh -p 55555 my.external.ip.address`` and the connection will be forwarded to the Pi server.

Happy hacking!

Source: `OpenWrt Port Forwarding <http://wiki.openwrt.org/doc/howto/port.forwarding>`_
