---
title: "Minimal Ubuntu"
date: "2016-08-14"
publishDate: "2014-07-07"
tags:
  - ubuntu
  - linux
  - crypto
slug: "ubuntu-trusty-install"
aliases:
  - /ubuntu-trusty-install.html
---

<img style="float:right" src="/img/screenshot/ubuntuInstall/xerus.png" />

**Ubuntu 16.04 "Xenial Xerus"** is the latest **Long Term Support (LTS)** release of the popular Linux operating system. I use Ubuntu's [minimal install image](https://help.ubuntu.com/community/Installation/MinimalCD) to create a **console-only base configuration** that can be customized for various tasks and [alternate desktops](http://www.circuidipity.com/i3-tiling-window-manager.html).

## Let's go!

Below is a visual walk-through of a sample Ubuntu setup that makes use of an entire storage device divided into 3 partitions: an unencrypted `root` partition, and encrypted `swap` + `home`. 

## 0. Prepare install media

Download the [64-bit xenial minimal installer](http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/netboot/mini.iso) ([32-bit](http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-i386/current/images/netboot/mini.iso) for older machines) and burn to CD or [flash the image](https://help.ubuntu.com/community/Installation/FromUSBStick) to a USB stick. [^1] Using the minimal console installer vs. the graphical installer provides more options during setup. [^2]

Minimal installer (requires network connection) downloads all the latest packages during setup.

## 1. Launch
---------

![Install](/img/screenshot/ubuntuInstall/100.png)

![Select language](/img/screenshot/ubuntuInstall/101.png)

![Selecl location](/img/screenshot/ubuntuInstall/102.png)

![Configure keyboard](/img/screenshot/ubuntuInstall/103.png)

![Keyboard](/img/screenshot/ubuntuInstall/104.png)

![Keyboard](/img/screenshot/ubuntuInstall/105.png)

![Hostname](/img/screenshot/ubuntuInstall/106.png)

![Mirror country](/img/screenshot/ubuntuInstall/107.png)

![Mirror archive](/img/screenshot/ubuntuInstall/108.png)

![Proxy](/img/screenshot/ubuntuInstall/109.png)

Contents of the installer are now loaded into memory and the USB stick can safely be removed. [^3]

![Full name](/img/screenshot/ubuntuInstall/110.png)

![Username](/img/screenshot/ubuntuInstall/111.png)

![User password](/img/screenshot/ubuntuInstall/112.png)

![Verify password](/img/screenshot/ubuntuInstall/113.png)

![Encrypt home](/img/screenshot/ubuntuInstall/114.png)

![Configure clock](/img/screenshot/ubuntuInstall/115.png)

![Select time zone](/img/screenshot/ubuntuInstall/116.png)

## 2. Partitions

In the example below I create 3 partitions [^4] on the disk:

* sda1 is a 24GB `root` partition 
* sda2 is a 2GB LUKS encrypted `swap` partition using a **random key**
* sda3 uses the remaining space as a LUKS encrypted `home` partition using a **passphrase**

![Partitioning method](/img/screenshot/ubuntuInstall/200.png)

![Partition disks](/img/screenshot/ubuntuInstall/201.png)

![Partition table](/img/screenshot/ubuntuInstall/202.png)

![Free space](/img/screenshot/ubuntuInstall/203.png)

![New partition](/img/screenshot/ubuntuInstall/204.png)

![Partition size](/img/screenshot/ubuntuInstall/205.png)

![Primary partition](/img/screenshot/ubuntuInstall/206.png)

![Beginning](/img/screenshot/ubuntuInstall/207.png)

Setting `Mount options: relatime` decreases write operations and boosts drive speed ...

![Mount options](/img/screenshot/ubuntuInstall/208.png)

![Mount relatime](/img/screenshot/ubuntuInstall/209.png)

![Done with partition](/img/screenshot/ubuntuInstall/210.png)

![Free space](/img/screenshot/ubuntuInstall/211.png)

![New partition](/img/screenshot/ubuntuInstall/204.png)

![Partition size](/img/screenshot/ubuntuInstall/213.png)

![Primary partition](/img/screenshot/ubuntuInstall/206.png)

![Beginning](/img/screenshot/ubuntuInstall/207.png)
    
![Use as](/img/screenshot/ubuntuInstall/215.png)

![Encrypt volume](/img/screenshot/ubuntuInstall/216.png)

![Encrypt key](/img/screenshot/ubuntuInstall/217.png)

![Random key](/img/screenshot/ubuntuInstall/218.png)

If the hard disk has not been securely wiped prior to installing Ubuntu you may want to configure `Erase data: yes`. Note, however, that depending on the size of the disk this operation can last several hours ...

![Done with partition](/img/screenshot/ubuntuInstall/219.png)

![Free space](/img/screenshot/ubuntuInstall/220.png)

![New partition](/img/screenshot/ubuntuInstall/204.png)

![Partition size](/img/screenshot/ubuntuInstall/222.png)

![Primary partition](/img/screenshot/ubuntuInstall/206.png)

![Use as](/img/screenshot/ubuntuInstall/224.png)

![Encrypt volume](/img/screenshot/ubuntuInstall/216.png)

![Encrypt key](/img/screenshot/ubuntuInstall/216-1.png)

![Passphrase](/img/screenshot/ubuntuInstall/216-2.png)

![Done with partition](/img/screenshot/ubuntuInstall/226.png)
 
![Configure encrypted volumes](/img/screenshot/ubuntuInstall/227.png)

![Write changes](/img/screenshot/ubuntuInstall/228.png)

![Create encrypted volumes](/img/screenshot/ubuntuInstall/229.png)

![Devices to encrypt](/img/screenshot/ubuntuInstall/230.png)

![Finish](/img/screenshot/ubuntuInstall/231.png)

![Encrypt passphrase](/img/screenshot/ubuntuInstall/232.png)

![Verify passphrase](/img/screenshot/ubuntuInstall/233.png)

![Configure encrypt volume](/img/screenshot/ubuntuInstall/234.png)

![Mount point](/img/screenshot/ubuntuInstall/235.png)

![Mount home](/img/screenshot/ubuntuInstall/236.png)

![Mount options](/img/screenshot/ubuntuInstall/237.png)

![Mount relatime](/img/screenshot/ubuntuInstall/209.png)

**Reserved blocks** can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large, **non-root partitions** extra space can be gained by reducing the `5%` default reserve set by Ubuntu to `1%` ...

![Reserved blocks](/img/screenshot/ubuntuInstall/239.png)

![Percent reserved](/img/screenshot/ubuntuInstall/240.png)

![Done with partition](/img/screenshot/ubuntuInstall/241.png)

![Finish](/img/screenshot/ubuntuInstall/242.png)

![Write changes](/img/screenshot/ubuntuInstall/243.png)

## 3. Install packages and finish up

![No automatic updates](/img/screenshot/ubuntuInstall/300.png)

**Alternative:** For a [home server setup](http://www.circuidipity.com/laptop-home-server.html) I like to select `Install security updates automatically` for a device often running unattended ...

![Install security updates](/img/screenshot/ubuntuInstall/300-1.png)

Select `[*] standard system utilities` and leave the remaining tasks unmarked if you wish to start with a minimal, console-only base configuration ready for further customization ... [^5]

![Software selection](/img/screenshot/ubuntuInstall/301.png)

**Alternative:** Or - again, for a home server - select the few extras included in `[*] Basic Ubuntu server` ...

![Software selection](/img/screenshot/ubuntuInstall/301-1.png)

Packages are downloaded and the installer makes its finishing touches ...

![GRUB](/img/screenshot/ubuntuInstall/302.png)

![UTC](/img/screenshot/ubuntuInstall/303.png)

![Finish install](/img/screenshot/ubuntuInstall/304.png)

## 4. First boot

System will display a passphrase prompt to unlock encrypted `home` partition ...

![Enter encrypt passphrase](/img/screenshot/ubuntuInstall/305.png)

![Login](/img/screenshot/ubuntuInstall/306.png)

Login ... then run `timedatectl` to confirm system time+date is properly set.

## 5. GRUB

After running a minimal install on my laptop with encrypted `swap` + `home` partitions I ran into this issue: ["Black screen instead of password prompt for boot encryption"](https://bugs.launchpad.net/ubuntu/+source/cryptsetup/+bug/1375435).

I had to enter my passphrase blind and `ALT+F1` to console. When I tried removing the GRUB options `splash` and/or `quiet` I lost the ability to enter the passphrase at all and a hard reset was required.

**[ Fix! ]** Modify `/etc/default/grub` ...

```bash
# Force the kernel to boot in normal text mode with '=text'                     
GRUB_GFXPAYLOAD_LINUX=text
```

... and update ...

```bash
sudo update-grub
```

Now it works! My chromebook is the only device I have run into this issue.

Link: [GNU gfxpayload](https://www.gnu.org/software/grub/manual/html_node/gfxpayload.html)

## 6. Network

Check which network interfaces are detected and settings ...

```bash
ip a
```

**Wired** interfaces are usually auto-configured by default and assigned an IP address courtesy of DHCP.

To assign a **static** address, deactivate the wired interface and create a new entry in `/etc/network/interfaces`. Sample entry for `enp3s0` ...

```bash
# The primary network interface
auto enp3s0
#iface enp3s0 inet dhcp
iface enp3s0 inet static
address 192.168.1.88
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 192.168.1.1
```

Bring up|down interface with `sudo if{up,down} enp3s0`.

Create a temporary **wireless** interface connection to WPA2 encrypted access points manually using `wpa_supplicant` + `wpa_passphrase` + `dhclinet`. Sample setup of `wlp1s0` ...

```bash
sudo ip link set wlp1s0 up            # bring up interface
iw dev wlp1s0 link                    # get link status
sudo iw dev wlp1s0 scan | grep SSID   # scan for access points
sudo -i                               # simulate a root login shell (for wpa_supplicant)
wpa_supplicant -B -i wlp1s0 -c<(wpa_passphrase "MY_SSID" "MY_PASSPHRASE")   # connect to WPA/WPA2 ... '-B' sends the process to the background
exit
sudo dhclient wlp1s0                  # obtain IP address
```

More permanent configurations may be set in `/etc/default/interfaces`. Sample setup [^6] with a static IP address ...

```bash
iface wlp1s0 inet static
address 192.168.1.77
netmask 255.255.255.0
gateway 192.168.1.1                                                              
wpa-ssid MY_SSID
wpa-psk MY_PASSPHRASE
dns-nameservers 8.8.8.8 8.8.4.4                                                  
```

Alternative setup using DHCP ...

```bash               
allow-hotplug wlp1s0
iface wlp1s0 inet dhcp
wpa-ssid MY_SSID
wpa-psk MY_PASSPHRASE                                       
dns-nameservers 8.8.8.8 8.8.4.4
```

Once a link is established an optional network manager utility may be installed. Package `network-manager-gnome` provides the console `nmcli` and graphical `nm-applet` clients ...

```bash
sudo apt install network-manager-gnome 
```

Comment out (deactivate) any entries in `/etc/network/interfaces` that will be managed by `network-manager`.

## 7. Where to go next ...

... is up to YOU. Yeehaw.

Happy hacking!

#### Notes

[^1]: An alternative is adding the image to a [USB stick with multiple Linux installers](http://www.circuidipity.com/multi-boot-usb.html).

[^2]: Specifically, the console installer provides a **random key** option for the encrypted swap partition.

[^3]: Recommended: Otherwise the partitioning tool may designate the USB device as primary (sda) storage and lead to broken partition layouts.

[^4]: For storage devices >=128GB I create separate `root` + `swap` + `home` partitions. Smaller devices get `boot` + `swap` + `root` partitions. Note encrypted `root` **requires** an unencrypted `boot`.

[^5]: The task selection menu can be run post-install using `sudo tasksel`.

[^6]: Multiple wireless static IP address setups can be created with `iface wlp1s0_NAME inet static` and [de]activated with `sudo if{up.down} wlp1s0=wlp1s0_NAME`.
