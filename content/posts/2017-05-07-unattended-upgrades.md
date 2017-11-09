---
title: "Automatic security updates on Debian"
date: "2017-05-07"
publishDate: "2017-05-07"
tags:
  - debian
  - linux
slug: "unattended-upgrades"
aliases:
  - /unattended-upgrades.html
---

:penguin: [Home Server](http://www.circuidipity.com/home-server/) :: Fetch the latest fixes, install, and reboot (if necessary). Hands-free!

## Let's go!

Install ...

```bash
sudo apt install unattended-upgrades apt-listchanges
```

Configuration file for the unattended-upgrades package is `/etc/apt/apt.conf.d/50unattended-upgrades`. This section controls which packages are upgraded and security updates are uncommented and enabled by default ...

```bash
Unattended-Upgrade::Origins-Pattern {
    //
    [...]
    "origin=Debian,codename=${distro_codename},label=Debian-Security";
};
```

Uncomment the following line to have mail sent to root when Debian auto-installs packages ...

```bash
Unattended-Upgrade::Mail "root";
```

Confirm a working mail setup is in place. A package that provides `mailx` must be installed ...

```bash
dpkg -l | grep mailx
    ii  bsd-mailx                     8.1.2-0.20141216cvs-2      i386         simple mail user agent
```

On a laptop consider enabling the `MinimalSteps` option. This allows an upgrade to be interrupted upon shutdown (with a slight delay) ...

```bash
Unattended-Upgrade::MinimalSteps "true";
```

Some security updates can require the system to be rebooted. On a server I enable automatic reboot and set the reboot to occur at a specified time (instead of immediately) ...

```bash
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";
```

Activate unattended-upgrades by creating `/etc/apt/apt.conf.d/02periodic`. Sample file ...

```bash
// Control parameters for cron jobs by /etc/cron.daily/apt //

// Enable the update/upgrade script (0=disable)
APT::Periodic::Enable "1";

// Do "apt-get update" automatically every n-days (0=disable)
APT::Periodic::Update-Package-Lists "1";

// Run the "unattended-upgrade" security upgrade script every n-days (0=disabled)
// Requires the package "unattended-upgrades" and will write a log in /var/log/unattended-upgrades
APT::Periodic::Unattended-Upgrade "1";

// Do "apt-get autoclean" every n-days (0=disable)
APT::Periodic::AutocleanInterval "14";

// Send report mail to root ...
//  0:  no report             (or null string)
//  1:  progress report       (actually any string)
//  2:  + command outputs     (remove -qq, remove 2>/dev/null, add -d)
//  3:  + trace on
APT::Periodic::Verbose "2";
```

Confirm notifications will be sent to root ...

```bash
cat /etc/apt/listchanges.conf
    [apt]
    frontend=pager
    email_address=root
    confirm=0
    save_seen=/var/lib/apt/listchanges.db
    which=news
```

Upgrade information is also logged within the `/var/log/unattended-upgrades` directory.

Happy hacking!
