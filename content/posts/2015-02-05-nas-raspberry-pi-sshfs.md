---
title: "Network Attached Storage using a Raspberry Pi and SSHFS"
date: "2015-02-05"
publishDate: "2015-02-05"
tags:
  - raspberry pi
  - network
  - ssh
  - crypto
  - linux
slug: "nas-pi-sshfs"
---

Connect a Pi to external USB storage and create a cheap and cheerful NAS device via **SSH Filesystem** (SSHFS).

With a [Pi-attached 1TB hard drive](http://www.circuidipity.com/raspberry-pi-usb-storage-v4.html) hosting a properly configured [SSH server](http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html) nothing extra is required server-side. 

On the client... Install SSHFS and create a mountpoint for the remote filesystem ...

```bash
sudo apt-get install sshfs
mkdir ~/NAS                                                          
```

Mount the Pi-hosted remote filesystem (example: `ip_address:192.168.1.88`) to the client ...

```bash
sshfs -o idmap=user 192.168.1.88:/media/external_usb_storage ~/NAS
```

Contents of the remote hard drive now appear as local directories and files on the laptop. Data transfer between server and client is SSH-encrypted.

Use `fusermount` to detach from the remote storage ...

```bash
fusermount -u ~/NAS                       
```

Raspberry Pi + SSHFS is no speed demon but its very usable. On my laptop using a wireless LAN connection I am able to run Rhythmbox playing music and videos in VLC remotely hosted on the Pi.

:penguin: *Part of the* [Linux Home Server](https://www.circuidipity.com/home-server/) *project*.

Happy hacking!
