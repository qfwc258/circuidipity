---
title: "Port forwarding"
date: "2014-10-06"
publishDate: "2014-10-06"
tags:
  - openwrt
  - network
  - linux
slug: "20141006"
aliases:
  - /20141006.html
---

**Port forwarding** enables [SSH access](http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html) to my [home server](http://www.circuidipity.com/home-server.html) from outside the home by forwarding traffic directed at a port on the router (reachable over the Internet by [dynamic DDNS](http://www.circuidipity.com/ddns-openwrt.html)) to the SSH port on the internal server behind a [NAT firewall](http://wiki.openwrt.org/doc/uci/firewall).

[OpenWrt](http://www.circuidipity.com/supercharge-a-home-router-using-openwrt-pt2.html) port forward configuration is done in `/etc/config/firewall`. A sample entry that redirects port `55555` on the router to the SSH server listening on port `22` at `192.168.1.88` ...

```bash
config 'redirect'
option 'name' 'ssh'
option 'src' 'wan'
option 'proto' 'tcpudp'
option 'src_dport' '55555'
option 'dest_ip' '192.168.1.88'
option 'dest_port' '22'
option 'target' 'DNAT'
option 'dest' 'lan'
```

Save and make the changes active by running ...

```bash
/etc/init.d/firewall restart
```

**Alternative:** setup port forwarding in LuCI under `Network->Firewall->Port Forwards`.

Example: SSH login outside the home enter `ssh -p 55555 my.external.ip.address` and the connection will be forwarded to the Pi server.

Link: [OpenWrt Port Forwarding](http://wiki.openwrt.org/doc/howto/port.forwarding)

Happy hacking!
