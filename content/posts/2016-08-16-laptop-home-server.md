---
title: "New life for an old laptop as a Linux home server"
date: "2018-01-11"
publishDate: "2016-08-16"
tags:
  - network
  - debian
  - linux
slug: "laptop-home-server"
---

:penguin: [Home Server](http://www.circuidipity.com/home-server/) :: **Netbooks** ... remember those small, (a few) Linux-powered laptops from several years ago? I dusted off my old **Asus 900HA** netbook and put it to work as a home server. Good times!

Running your own home server is a fun learning experience and offers several advantages.

Second-hand laptops -  retired in favour of more current and powerful machines - can still deliver plenty of *oomph* for running a personal server. Frugal with power and come equipped with their own built-in UPS (battery)!

Install a stable, well-tested Linux distribution and host services such as [network printing](http://www.circuidipity.com/network-printer-scanner) and [storage (NAS)](http://www.circuidipity.com/nas-raspberry-pi-sshfs), perform [backups](http://www.circuidipity.com/backup-over-lan), host [web services](http://www.circuidipity.com/php-nginx-postgresql) and much more. Start with a minimal base configuration of [Debian](http://www.circuidipity.com/minimal-debian) and gain access to tens of thousands of packages ready to install.

Privacy may be important to you. Hosting your own server running your own services gives more control over your data.

## Let's go!

**Hardware:** Asus 900HA netbook with 9" display, 1GB RAM, a 500GB hard drive (very easy replacement of original drive - just unscrew the netbook's bottom panel), built-in ethernet/wifi, webcam, and a host of ports (3xUSB2, VGA, sound, SD card slot). Neat and compact device!

## 0. Install Debian

My [screenshot tour](http://www.circuidipity.com/minimal-debian) of installing the Debian **stretch/stable** release. Debian's minimal **network+firmware install image** (32bit for the netbook) makes it easy to create a console-only base configuration that can be later customized for various tasks. 

I make a few modifications to my usual desktop install routine that are more appropriate for configuring a home server. I don't want an unattended server halting in the boot process waiting for a passphrase or any necessary boot mountpoints to reside on an encrypted partition. After a successful first boot I configure an encrypted container for data storage to be mounted manually.

Using the Debian installer I create 2 partitions on the netbook's 500GB internal storage ...

* sda1 is 16GB dedicated to `root`
* sda2 is 2GB used for `swap`

... with lots of space left free for the encrypted partition to be created post-install.

## 1. Static network address

Login to the new home server and check which network interfaces are detected and settings ...

```bash                                                            
ip a
```
                                                                                
**Wired** interfaces are usually auto-configured by default and assigned an IP address courtesy of DHCP.
                                                                                
To assign the server a **static** address (recommended), deactivate the wired interface and create a new entry in `/etc/network/interfaces`. [^1] Sample entry for `enp3s0` ...

                                                                                
```bash                                                            
# The primary network interface                                             
auto enp3s0
iface enp3s0 inet static                                                    
address 192.168.1.88                                                    
netmask 255.255.255.0                                                   
gateway 192.168.1.1                                                     
dns-nameservers 8.8.8.8                                            
```

Bring up|down interface with `sudo if{up,down} enp3s0`.

## 2. SSH

Install OpenSSH, create crypto keys, and [disable password logins](http://www.circuidipity.com/secure-remote-access-using-ssh-keys) to boost server security.

## 3. Automatic security updates

Fetch the [latest fixes, install, and reboot (if necessary)](http://www.circuidipity.com/unattended-upgrades). Hands-free!

## 4. Encrypted storage

I use the remaining disk space to create partition `sda3` (using `fdisk`). Configure LUKS encryption on the new partition ...

```
# cryptsetup luksFormat /dev/sda3
```

Open the encrypted partition under ``sda3_crypt``, format with the `ext4` filesystem, create a dedicated mountpoint, and mount ... [^2]

```
# cryptsetup open /dev/sda3 sda3_crypt
# mkfs.ext4 -m 1 /dev/mapper/sda3_crypt
# mkdir /media/sda3_crypt
# mount /dev/mapper/sda3_crypt /media/sda3_crypt
```

When finished, unmount the filesystem and close the encrypted partition ...

```
# umount /media/sda3_crypt
# cryptsetup close /dev/mapper/sda3_crypt
```

Modify ``/etc/fstab`` and allow mounting by a non-root user ...

```
/dev/mapper/sda3_crypt   /media/sda3_crypt     ext4    relatime,noauto,user    0   0
```

## 5. Power management on hard drive

Default settings on the netbook frequently park and spindown the drive, generating an audible "click" sound. Too aggressive power management can reduce lifespan of drive. I want "kinder, gentler" settings.
                                                                                   
Get information on drive ...                                                     

```bash                                                               
sudo hdparm -I /dev/sda                                                      
```

From `man hdparm` ...

`-B`                                                                             
    Get/set Advanced Power Management feature ... low value means aggressive power management and a high value means better performance. Possible settings range from values 1 through 127 (which permit spin-down), and values 128 through 254 (which do not permit spin-down) ... A value of 255 tells hdparm to disable APM altogether ...
                                                                                   
`-S`                                                                             
    Put the drive into idle (low-power) mode, and also set the standby (spindown) timeout for the drive ... A value of zero means "timeouts are disabled" ...
                                                                                   
On the netbook I run ...                                                         
                                                                                   
```bash                                                               
sudo hdparm -B 254 -S 0 /dev/sda                                             
    /dev/sda:                                                                        
    setting Advanced Power Management level to 0xfe (254)                            
    setting standby to 0 (off)                                                       
    APM_level      = 254                                                           
```

Create **udev rules** to setup at boot. Existing rule ...                         
                                                                                   
```bash                                                               
cat /lib/udev/rules.d/85-hdparm.rules                                          
    ACTION=="add", SUBSYSTEM=="block", KERNEL=="[sh]d[a-z]", RUN+="/lib/udev/hdparm"
```

... and make my own `/etc/udev/rules.d/85-hdparm.rules` (rules in `/etc/udev/rules.d` have the [highest priority](http://manpages.ubuntu.com/manpages/wily/man7/udev.7.html)) ...

```bash
ACTION=="add", SUBSYSTEM=="block", KERNEL=="sda", RUN+="/sbin/hdparm -B 254 -S 0 /dev/sda"
```

## 6. Backlight

Install the `vbetool` package to control the netbook's display backlight ...

```bash
sudo apt install vbetool
```

SSH into the server and turn off/on the backlight with the commands ...

```bash
sudo vbetool dpms off
sudo vbetool dpms on
```

## 7. Services

What to do next? [Some of the services I use ...](http://www.circuidipity.com/home-server)

Happy hacking!

#### Notes

[^1]: Problem: setting the network interface to static address can result in `/etc/resolv.conf` being overwritten every few minutes with an IPv6 address that breaks DNS. The "fix" is to maually set `nameserver 8.8.8.8` in resolv.conf and install the `resolvconf` package. Note that `dns-nameservers` entries are ignored if resolvconf is not installed.

[^2]: Reserved blocks can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large non-root partitions extra space can be gained by reducing the default 5% reserve set aside to 1% with option ``-m <percent>``.

