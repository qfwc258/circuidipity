---
title: "Minimal Ubuntu"
date: "2018-04-30"
publishDate: "2014-07-07"
tags:
  - ubuntu
  - linux
  - crypto
slug: "minimal-ubuntu"
---

<img style="float:right" src="/img/bionic-beaver-300.png" />

**Ubuntu 18.04 "Bionic Beaver"** is the latest **LTS release** (5 years support) of the popular Linux operating system. I use Ubuntu's [minimal install image](https://help.ubuntu.com/community/Installation/MinimalCD) to create a **console-only base configuration** that can be customized for various tasks and alternate desktops.

## Let's go!

Below is a visual walk-through of a sample Ubuntu setup that makes use of an entire disk divided into 3 partitions: a `root` partition, encrypted `swap`, and encrypted `home`. 

## 0. Prepare install media

Download the [64-bit minimal installer](http://archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/current/images/netboot/mini.iso) ([32-bit](http://archive.ubuntu.com/ubuntu/dists/bionic/main/installer-i386/current/images/netboot/mini.iso) for older machines) and burn to CD or [flash the image](https://help.ubuntu.com/community/Installation/FromUSBStick) to a USB stick. [^1] Using the minimal console installer vs. the graphical installer provides more options during setup.

Minimal installer (requires network connection) downloads all the latest packages during setup.

## 1. Launch

![Install](/img/screenshot/minimal-ubuntu-v2/100.png)

![Select language](/img/screenshot/minimal-ubuntu-v2/101.png)

![Select location](/img/screenshot/minimal-ubuntu-v2/102.png)

![Configure keyboard](/img/screenshot/minimal-ubuntu-v2/103.png)

![Keyboard](/img/screenshot/minimal-ubuntu-v2/104.png)

I use the **Colemak** keyboard layout ...

![Keyboard](/img/screenshot/minimal-ubuntu-v2/105.png)

A device with a single network interface is auto-detected and configured (otherwise the installer prompts to select an interface) ...

![DHCP](/img/screenshot/minimal-ubuntu-v2/106.png)

![Hostname](/img/screenshot/minimal-ubuntu-v2/107.png)

![Mirror country](/img/screenshot/minimal-ubuntu-v2/108.png)

![Mirror archive](/img/screenshot/minimal-ubuntu-v2/109.png)

![Proxy](/img/screenshot/minimal-ubuntu-v2/110.png)

Contents of the installer are now loaded into memory and the USB stick can safely be removed. [^2]

![Full name](/img/screenshot/minimal-ubuntu-v2/111.png)

![Username](/img/screenshot/minimal-ubuntu-v2/112.png)

![User password](/img/screenshot/minimal-ubuntu-v2/113.png)

![Verify password](/img/screenshot/minimal-ubuntu-v2/114.png)

![Configure clock](/img/screenshot/minimal-ubuntu-v2/115.png)

![Timezone](/img/screenshot/minimal-ubuntu-v2/116.png)

## 2. Partitions

Sample layout:

* sda1 is a 24GB `root` partition
* sda5 is a 2GB LUKS *random key* encrypted `swap` partition
* sda6 uses the remaining storage as a LUKS *passphrase* encrypted `home` partition

![Partitioning method](/img/screenshot/minimal-ubuntu-v2/200.png)

![Partition disks](/img/screenshot/minimal-ubuntu-v2/201.png)

![Partition table](/img/screenshot/minimal-ubuntu-v2/202.png)

![Free space](/img/screenshot/minimal-ubuntu-v2/203.png)

![New partition](/img/screenshot/minimal-ubuntu-v2/204.png)

![Partition size](/img/screenshot/minimal-ubuntu-v2/205.png)

![Primary partition](/img/screenshot/minimal-ubuntu-v2/206.png)

![Beginning](/img/screenshot/minimal-ubuntu-v2/207.png)

![Done with partition](/img/screenshot/minimal-ubuntu-v2/208.png)

![Free space](/img/screenshot/minimal-ubuntu-v2/209.png)

![New partition](/img/screenshot/minimal-ubuntu-v2/210.png)

![Partition size](/img/screenshot/minimal-ubuntu-v2/211.png)

![Logical partition](/img/screenshot/minimal-ubuntu-v2/212.png)

![Beginning](/img/screenshot/minimal-ubuntu-v2/213.png)

![Use as](/img/screenshot/minimal-ubuntu-v2/214.png)

![Encrypt volume](/img/screenshot/minimal-ubuntu-v2/215.png)

If the hard disk has not been securely wiped prior to installing Ubuntu you may want to configure <nobr>`Erase data: yes`.</nobr> Note, however, that depending on the size of the disk this operation can last several hours ...

![Encryption key](/img/screenshot/minimal-ubuntu-v2/216.png)

![Random key](/img/screenshot/minimal-ubuntu-v2/217.png)

![Done with partition](/img/screenshot/minimal-ubuntu-v2/218.png)

![Free space](/img/screenshot/minimal-ubuntu-v2/219.png)

![New partition](/img/screenshot/minimal-ubuntu-v2/220.png)

![Partition size](/img/screenshot/minimal-ubuntu-v2/221.png)

![Logical partition](/img/screenshot/minimal-ubuntu-v2/222.png)

![Use as](/img/screenshot/minimal-ubuntu-v2/223.png)

![Encrypt volume](/img/screenshot/minimal-ubuntu-v2/224.png)

![Encryption key](/img/screenshot/minimal-ubuntu-v2/225.png)

![Passphrase](/img/screenshot/minimal-ubuntu-v2/226.png)

![Done with partition](/img/screenshot/minimal-ubuntu-v2/227.png)

![Configure encrypt](/img/screenshot/minimal-ubuntu-v2/228.png)

![Write changes](/img/screenshot/minimal-ubuntu-v2/229.png)

![Create encrypt](/img/screenshot/minimal-ubuntu-v2/230.png)

![Device to encrypt](/img/screenshot/minimal-ubuntu-v2/231.png)

![Finish](/img/screenshot/minimal-ubuntu-v2/232.png)

![Passphrase](/img/screenshot/minimal-ubuntu-v2/233.png)

![Re-enter passphrase](/img/screenshot/minimal-ubuntu-v2/234.png)

![Encrypt volume swap](/img/screenshot/minimal-ubuntu-v2/235.png)

![Encrypt volume](/img/screenshot/minimal-ubuntu-v2/236.png)

![Mount point](/img/screenshot/minimal-ubuntu-v2/237.png)

![Home](/img/screenshot/minimal-ubuntu-v2/238.png)

**Reserved blocks** can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large, **non-root** partitions extra space can be gained by reducing the `5%` default reserve set by Ubuntu to `1%` ...

![Reserved blocks](/img/screenshot/minimal-ubuntu-v2/239.png)

![Percent reserved](/img/screenshot/minimal-ubuntu-v2/240.png)

![Done with partition](/img/screenshot/minimal-ubuntu-v2/241.png)

![Finish](/img/screenshot/minimal-ubuntu-v2/242.png)

![Write changes](/img/screenshot/minimal-ubuntu-v2/243.png)

![Partitions formatting](/img/screenshot/minimal-ubuntu-v2/244.png)

## 3. Install packages and finish up

![No automatic updates](/img/screenshot/minimal-ubuntu-v2/300.png)

**Alternative:** For a [home server setup](https://www.circuidipity.com/laptop-home-server/) I like to select <nobr>`Install security updates automatically`</nobr> for a device often running unattended.

Un-select all tasks [^3] for a minimal install ...

![Software selection](/img/screenshot/minimal-ubuntu-v2/301.png)

Core packages are downloaded and the installer makes its finishing touches ...

![Dowload and install](/img/screenshot/minimal-ubuntu-v2/302.png)

![GRUB](/img/screenshot/minimal-ubuntu-v2/303.png)

![UTC](/img/screenshot/minimal-ubuntu-v2/304.png)

![Finish install](/img/screenshot/minimal-ubuntu-v2/305.png)

## 4. First boot

User is prompted for the passphrase to unlock the encrypted partition ...

![Enter encrypt passphrase](/img/screenshot/minimal-ubuntu-v2/400.png)

![Login](/img/screenshot/minimal-ubuntu-v2/401.png)

Login ... then run `timedatectl` to confirm system time+date is properly set.

## 5. Kernel options

After running a minimal install on my laptop with LUKS encryption, the boot process would halt for ~30 seconds then generate this message ...

```bash
Gave up waiting for suspend/resume device
```

... followed by a prompt for the passphrase to unlock encrypted `home`, then continue to login.

**[ Fix! ]** System is looking for a swap device for suspend-to-disk/hibernate and fails to recognize my encrypted swap. I don't use hibernate, so I disable the task by adding kernel option `noresume`.

Modify `/etc/default/grub` ...

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet noresume"
```

... and update ...

```bash
$ sudo update-grub
```

Link: [boot delayed by 30sec waiting for suspend/resume device](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=860543#22)

## 6. Network

Check which network interfaces are detected and settings ...

```bash
$ ip a
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

More permanent configurations may be set in `/etc/default/interfaces`. Sample setup [^4] with a static IP address ...

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

Once a link is established install an (optional) network manager utility. Packages `network-manager` and `network-manager-gnome` provide the console `nmcli` and graphical `nm-applet` clients respectively. Comment out (deactivate) any entries in `interfaces` that will be managed by `network-manager`.

## 7. Secure access using SSH keys

Create cryptographic keys, install the OpenSSH server, and [configure remote access](https://www.circuidipity.com/ssh-keys/).

## 8. Where to go next ...

... is up to YOU. Yeehaw.

Happy hacking!

#### Notes

[^1]: An alternative is adding the image to a [USB stick with multiple Linux installers](https://www.circuidipity.com/multi-boot-usb/).

[^2]: Recommended: Otherwise the partitioning tool may designate the USB device as primary (sda) storage and lead to broken partition layouts.

[^3]: The task selection menu can be run post-install using `sudo tasksel`.

[^4]: Multiple wireless static IP address setups can be created with `iface wlp1s0_NAME inet static` and [de]activated with `sudo if{up.down} wlp1s0=wlp1s0_NAME`.
