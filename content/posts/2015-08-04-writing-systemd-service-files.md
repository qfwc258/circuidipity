---
title: "Writing systemd service files"
date: "2015-08-04"
publishDate: "2015-08-04"
tags:
  - linux
slug: "writing-systemd-service-files"
aliases:
  - /writing-systemd-service-files.html
---

Allow **systemd** and its `systemctl` command to start, stop, and report the status of a daemon by creating a **service file** in `/etc/systemd/system`.

**Example:** Setup the [irqbalance daemon I installed on my Raspberry Pi](http://www.circuidipity.com/raspberry-pi-ram-irqbalance) for systemd control by creating `/etc/systemd/system/irqbalance.service` ...

```bash
[Unit]      
Description=Daemon to distribute hardware interrupts across multi-CPUs      
                                                                                     
[Service]      
Type=forking      
# man systemd.service: "If set to forking... it is recommended to also use the   
# PIDFile= option, so that systemd can identify the main process of the daemon." 
PIDFile=/var/run/irqbalance.pid      
ExecStart=/usr/local/sbin/irqbalance --pid=/var/run/irqbalance.pid      
                                                                                     
[Install]      
WantedBy=multi-user.target
```

Set the new service to be auto-started at boot ...

```bash
sudo systemctl daemon-reload && sudo systemctl enable irqbalance.service
    Created symlink from /etc/systemd/system/multi-user.target.wants/irqbalance.service to /etc/systemd/system/irqbalance.service.
```

Launch daemon and inspect running service ...

```bash
sudo systemctl start irqbalance.service && sudo systemctl status irqbalance
```

Happy hacking!

Link: [Writing systemd unit files](https://wiki.archlinux.org/index.php/Systemd#Writing_unit_files)
