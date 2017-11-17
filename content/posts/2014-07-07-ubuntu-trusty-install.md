---
title: "Minimal Ubuntu"
date: "2017-11-17"
publishDate: "2014-07-07"
tags:
  - ubuntu
  - linux
  - crypto
  - lvm
slug: "minimal-ubuntu"
---

<img style="float:right" src="/img/artful-aardvark-300.png" />

**Ubuntu 17.10 "Artful Aardvark"** is the latest release of the popular Linux operating system. I use Ubuntu's [minimal install image](https://help.ubuntu.com/community/Installation/MinimalCD) to create a **console-only base configuration** that can be customized for various tasks and alternate desktops.

## Let's go!

Below is a visual walk-through of a sample Ubuntu setup that makes use of an entire disk divided into 2 partitions: a `boot` partition, [^1] and an **encrypted** partition used by the **Logical Volume Manager** (LVM) to create "virtual partitions" (Logical Volumes). Installing LVM on top of the encrypted partition allows:

* creation of multiple LVs protected by a single passphrase entered at boot time
* dynamic resizing of filesystems (set aside unallocated space and make use of it as needed)
* snapshots of filesystems that can be used as backups or to restore a previous state [^2]

## 0. Prepare install media

Download the [64-bit artful minimal installer](http://archive.ubuntu.com/ubuntu/dists/artful/main/installer-amd64/current/images/netboot/mini.iso) ([32-bit](http://archive.ubuntu.com/ubuntu/dists/artful/main/installer-i386/current/images/netboot/mini.iso) for older machines) and burn to CD or [flash the image](https://help.ubuntu.com/community/Installation/FromUSBStick) to a USB stick. [^3] Using the minimal console installer vs. the graphical installer provides more options during setup.

Minimal installer (requires network connection) downloads all the latest packages during setup.

## 1. Launch

![Install](/img/screenshot/minimal-ubuntu/100.png)

![Select language](/img/screenshot/minimal-ubuntu/101.png)

![Selecl location](/img/screenshot/minimal-ubuntu/102.png)

![Configure keyboard](/img/screenshot/minimal-ubuntu/103.png)

![Keyboard](/img/screenshot/minimal-ubuntu/104.png)

I use the **Colemak** keyboard layout ...

![Keyboard](/img/screenshot/minimal-ubuntu/105.png)

A device with a single network interface is auto-detected and configured (otherwise the installer prompts to select an interface) ...

![Detecting network hardware](/img/screenshot/minimal-ubuntu/106.png)

![DHCP](/img/screenshot/minimal-ubuntu/107.png)

![Hostname](/img/screenshot/minimal-ubuntu/108.png)

![Mirror country](/img/screenshot/minimal-ubuntu/109.png)

![Mirror archive](/img/screenshot/minimal-ubuntu/110.png)

![Proxy](/img/screenshot/minimal-ubuntu/111.png)

Contents of the installer are now loaded into memory and the USB stick can safely be removed. [^4]

![Full name](/img/screenshot/minimal-ubuntu/112.png)

![Username](/img/screenshot/minimal-ubuntu/113.png)

![User password](/img/screenshot/minimal-ubuntu/114.png)

![Verify password](/img/screenshot/minimal-ubuntu/115.png)

![Encrypt home](/img/screenshot/minimal-ubuntu/116.png)

![Configure clock](/img/screenshot/minimal-ubuntu/117.png)

## 2. Partitions

Sample layout:

* sda1 is a 512MB `boot` partition
* sda2 uses the remaining storage as a LUKS encrypted partition
* LVM is installed on the encrypted partition, and contains a volume group with the 3 logical volumes: <nobr> `root` + `swap` + `home` </nobr>

![Partitioning method](/img/screenshot/minimal-ubuntu/200.png)

![Partition disks](/img/screenshot/minimal-ubuntu/201.png)

![Partition table](/img/screenshot/minimal-ubuntu/202.png)

![Free space](/img/screenshot/minimal-ubuntu/203.png)

![New partition](/img/screenshot/minimal-ubuntu/204.png)

![Partition size](/img/screenshot/minimal-ubuntu/205.png)

![Primary partition](/img/screenshot/minimal-ubuntu/206.png)

![Beginning](/img/screenshot/minimal-ubuntu/207.png)

![Mount point](/img/screenshot/minimal-ubuntu/208.png)

![Mount boot](/img/screenshot/minimal-ubuntu/209.png)

![Boot flag](/img/screenshot/minimal-ubuntu/210.png)

![Done with partition](/img/screenshot/minimal-ubuntu/211.png)

![Free space](/img/screenshot/minimal-ubuntu/212.png)

![New partition](/img/screenshot/minimal-ubuntu/213.png)

![Partition size](/img/screenshot/minimal-ubuntu/214.png)

![Primary partition](/img/screenshot/minimal-ubuntu/215.png)

![Use as](/img/screenshot/minimal-ubuntu/216.png)

![Encrypt volume](/img/screenshot/minimal-ubuntu/217.png)

If the hard disk has not been securely wiped prior to installing Ubuntu you may want to configure <nobr>`Erase data: yes`.</nobr> Note, however, that depending on the size of the disk this operation can last several hours ...

![Done with partition](/img/screenshot/minimal-ubuntu/218.png)

![Configure encrypt](/img/screenshot/minimal-ubuntu/219.png)

![Write changes](/img/screenshot/minimal-ubuntu/220.png)

![Create encrypt](/img/screenshot/minimal-ubuntu/221.png)

![Device to encrypt](/img/screenshot/minimal-ubuntu/222.png)

![Finish](/img/screenshot/minimal-ubuntu/223.png)

![Passphrase](/img/screenshot/minimal-ubuntu/224.png)

![Re-enter passphrase](/img/screenshot/minimal-ubuntu/225.png)

![Encrypt volume](/img/screenshot/minimal-ubuntu/226.png)

![Use as](/img/screenshot/minimal-ubuntu/227.png)

![LVM](/img/screenshot/minimal-ubuntu/228.png)
 
![Done setting up partition](/img/screenshot/minimal-ubuntu/229.png)

![Configure LVM](/img/screenshot/minimal-ubuntu/230.png)

![Write changes](/img/screenshot/minimal-ubuntu/231.png)

![Create volume group](/img/screenshot/minimal-ubuntu/232.png)

![Volume group name](/img/screenshot/minimal-ubuntu/233.png)

![Device for group](/img/screenshot/minimal-ubuntu/234.png)

![Create lv](/img/screenshot/minimal-ubuntu/235.png)

![Vg](/img/screenshot/minimal-ubuntu/236.png)

![Lv root](/img/screenshot/minimal-ubuntu/237.png)

![Lv size](/img/screenshot/minimal-ubuntu/238.png)

![Create lv](/img/screenshot/minimal-ubuntu/239.png)

![Vg](/img/screenshot/minimal-ubuntu/240.png)

![Lv swap](/img/screenshot/minimal-ubuntu/241.png)

![Lv size](/img/screenshot/minimal-ubuntu/242.png)

![Create lv](/img/screenshot/minimal-ubuntu/243.png)

![Vg](/img/screenshot/minimal-ubuntu/244.png)

![Lv home](/img/screenshot/minimal-ubuntu/245.png)

![Lv size](/img/screenshot/minimal-ubuntu/246.png)

![Finish](/img/screenshot/minimal-ubuntu/247.png)

![Partition](/img/screenshot/minimal-ubuntu/248.png)

![Use as](/img/screenshot/minimal-ubuntu/249.png)

![Ext4](/img/screenshot/minimal-ubuntu/250.png)

![Mount point](/img/screenshot/minimal-ubuntu/251.png)

![Home](/img/screenshot/minimal-ubuntu/252.png)

**Reserved blocks** can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large, **non-root** partitions extra space can be gained by reducing the `5%` default reserve set by Ubuntu to `1%` ...

![Reserved blocks](/img/screenshot/minimal-ubuntu/253.png)

![Percent reserved](/img/screenshot/minimal-ubuntu/254.png)

![Done with partition](/img/screenshot/minimal-ubuntu/255.png)

![Partition](/img/screenshot/minimal-ubuntu/256.png)

![Use as](/img/screenshot/minimal-ubuntu/257.png)

![Ext4](/img/screenshot/minimal-ubuntu/258.png)

![Mount point](/img/screenshot/minimal-ubuntu/259.png)

![Root](/img/screenshot/minimal-ubuntu/260.png)

![Done with partition](/img/screenshot/minimal-ubuntu/261.png)

![Partition](/img/screenshot/minimal-ubuntu/262.png)

![Use as](/img/screenshot/minimal-ubuntu/263.png)

![Swap](/img/screenshot/minimal-ubuntu/264.png)

![Done with partition](/img/screenshot/minimal-ubuntu/265.png)

![Finish](/img/screenshot/minimal-ubuntu/266.png)

![Write changes](/img/screenshot/minimal-ubuntu/267.png)

## 3. Install packages and finish up

![Install base](/img/screenshot/minimal-ubuntu/300.png)

![No automatic updates](/img/screenshot/minimal-ubuntu/301.png)

**Alternative:** For a [home server setup](https://www.circuidipity.com/laptop-home-server/) I like to select <nobr>`Install security updates automatically`</nobr> for a device often running unattended.

Un-select all tasks [^5] for a minimal install ...

![Software selection](/img/screenshot/minimal-ubuntu/302.png)

Core packages are downloaded and the installer makes its finishing touches ...

![GRUB](/img/screenshot/minimal-ubuntu/303.png)

![UTC](/img/screenshot/minimal-ubuntu/304.png)

![Finish install](/img/screenshot/minimal-ubuntu/305.png)

## 4. First boot

User is prompted for the passphrase to unlock the encrypted partition ...

![Enter encrypt passphrase](/img/screenshot/minimal-ubuntu/306.png)

![Login](/img/screenshot/minimal-ubuntu/307.png)

Login ... then run `timedatectl` to confirm system time+date is properly set.

## 5. GRUB

After running a minimal install on my laptop with LUKS encryption I ran into this issue: ["Black screen instead of password prompt for boot encryption"](https://bugs.launchpad.net/ubuntu/+source/cryptsetup/+bug/1375435).

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

Now it works!

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

Once a link is established install an (optional) network manager utility. Packages `network-manager` and `network-manager-gnome` provide the console `nmcli` and graphical `nm-applet` clients respectively. Comment out (deactivate) any entries in `interfaces` that will be managed by `network-manager`.

## 7. Secure access using SSH keys

Create cryptographic keys, install the OpenSSH server, and [configure remote access](https://www.circuidipity.com/ssh-keys/).

## 8. Where to go next ...

... is up to YOU. Yeehaw.

Happy hacking!

#### Notes

[^1]: Encrypted `root` requires an unencrypted `boot`.

[^2]: Very helpful! [LVM post on the Arch Wiki](https://wiki.archlinux.org/index.php/LVM).

[^3]: An alternative is adding the image to a [USB stick with multiple Linux installers](https://www.circuidipity.com/multi-boot-usb/).

[^4]: Recommended: Otherwise the partitioning tool may designate the USB device as primary (sda) storage and lead to broken partition layouts.

[^5]: The task selection menu can be run post-install using `sudo tasksel`.

[^6]: Multiple wireless static IP address setups can be created with `iface wlp1s0_NAME inet static` and [de]activated with `sudo if{up.down} wlp1s0=wlp1s0_NAME`.
