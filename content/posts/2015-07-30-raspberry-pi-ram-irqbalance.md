---
title: "Raspberry Pi RAM gobbled up by irqbalance"
date: "2015-07-30"
publishDate: "2015-07-30"
tags:
  - raspberry pi
  - linux
slug: "pi-ram-irqbalance"
---

**Problem:** After a few days uptime my Pi sees hundreds of MB gobbled up by the `irqbalance` daemon (which balances interrupts across multiple CPUs). Package version is `1.0.6-3` on Debian `jessie/armhf` and its a [known bug](https://bugs.launchpad.net/ubuntu/+source/irqbalance/+bug/1247107).

**[ Fix! ]** Restart `irqbalance` in nightly cron job, or compile and install a newer, patched version (my choice).

Remove buggy `irqbalance` ...

```bash
sudo systemctl stop irqbalance                                                       
sudo apt-get --purge remove irqbalance                                               
```

Install development tools on the Pi ...

```bash
sudo apt-get install build-essential autogen automake libtool pkg-config checkinstall
```

[Download source](https://github.com/Irqbalance/irqbalance) and unpack ...

```bash
wget https://github.com/Irqbalance/irqbalance/archive/v1.0.9.tar.gz && tar xvzf v1.0.9.tar.gz
```

**Checkinstall** is an easy way to make Debian packages for personal use. Compile and (check)install ...

```bash
cd irqbalance-1.0.9
/autogen.sh
./configure                                                                          
make                                                                                 
sudo checkinstall make install
```

Start new `irqbalance` ...

```bash
sudo /usr/local/sbin/irqbalance &
```

Optional: Configure the daemon for [systemd control and auto-start at boot](http://www.circuidipity.com/writing-systemd-service-files.html).

I have been running the daemon for a few days now and it stays around 0.6% memory usage vs **20%** (and growing) of the previous packaged version.

Happy hacking!
