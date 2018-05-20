---
title: "Dynamic DNS and OpenWRT"
date: "2015-02-06"
publishDate: "2015-02-06"
tags:
  - openwrt
  - network
  - linux
slug: "ddns-openwrt"
---

Access a home server from anywhere using **Dynamic DNS** (DDNS).

## Let's go!

My server sits behind a router assigned a **dynamic IP address** by the ISP. If I want to remotely connect to my server I can use a **DDNS service** to create a domain name that automatically updates the IP address whenever it changes and redirect traffic to the new location.

## 0. Select a DDNS service

I use the free DDNS service [duckdns.org](http://www.duckdns.org/) which permits the creation of up to 4 domains in the format `subdomain_foo.duckdns.org`. Make note of [duckdns.org/install](http://www.duckdns.org/install.jsp) (while logged in) for customized settings useful for configuring the router for DDNS.

## 1. Configure OpenWRT for notification

Different routers configure DDNS differently but the goal is the same: the ability to notify the DDNS service whenever the IP address assigned by the ISP is modified. I am using an [OpenWRT-powered router](http://www.circuidipity.com/supercharge-a-home-router-using-openwrt-pt2.html) and these are the steps to configure OpenWRT to use duckdns DDNS.

Login to the router and install DDNS packages ...

```bash
opkg update                                                                         
opkg install luci-app-ddns ddns-scripts                                             
```

Use the customized settings from [duckdns.org/install](http://www.duckdns.org/install.jsp) to configure `/etc/config/ddns` ...
      
```bash
config service          "duckdns"
option enabled          "1"
option service_name     "duckdns.org"
option domain           "subdomain_foo"
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
```

Start daemon ...

```bash
sh
. /usr/lib/ddns/dynamic_dns_functions.sh
start_daemon_for_all_ddns_sections "wan"
exit
```

Test ...

```bash
/usr/lib/ddns/dynamic_dns_updater.sh duckdns
```

In OpenWRT's `LuCI` interface navigate to `System->Startup` and enable DDNS to ensure the router continues to send IP address changes after reboot and hotplug events.
                                                                                    
Link: [OpenWRT DDNS client](http://wiki.openwrt.org/doc/howto/ddns.client)

## 2. Port forwarding

[Port forwarding](http://www.circuidipity.com/20141006.html) configures OpenWRT to forward traffic directed at one of the router's ports to the listening port on the server. **Example:** configure port `56789` on the router to [connect over SSH](http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html) to port `22` on the home server.

:penguin: *Part of the* [Linux Home Server](https://www.circuidipity.com/home-server/) *project*.

Happy hacking!
