---
title: "Minimal Debian"
date: "2018-05-17"
publishDate: "2015-07-07"
tags:
  - debian
  - linux
  - crypto
  - lvm
  - projects
slug: "minimal-debian"
---

![Debian Vader](/img/debianVader.png)

**Debian 9 "Stretch"** is the latest stable release of the popular Linux operating system. I use Debian's [network installer image](https://www.debian.org/CD/netinst/) to create a **console-only base configuration** that can be customized for various tasks and [alternate desktops](http://www.circuidipity.com/i3-tiling-window-manager.html). [^1]

## Let's go!

[Debian GNU/Linux](http://www.debian.org) is an operating system created by volunteers of one of the largest and longest-running free software projects in the world. There are 3 **release branches**: stable (code-named *stretch*), testing (*buster*), and unstable (*sid*).

Below is a visual walk-through of a sample workstation setup that makes use of the entire disk divided into 2 partitions: a `boot` partition, [^2] and an **encrypted partition** used by the **Logical Volume Manager** (LVM) to create "virtual partitions" (Logical Volumes). Installing LVM on top of the encrypted partition allows:

* creation of multiple LVs protected by a single passphrase entered at boot time
* dynamic resizing of filesystems (set aside unallocated space and make use of it as needed)
* snapshots of filesystems that can be used as backups or to restore a previous state [^3]

## 0. Prepare install media

Download and verify the (unofficial with firmware) 64-bit `firmware-9.4.0-amd64-netinst.iso` ...

```bash
$ wget -c https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/iso-cd/firmware-9.4.0-amd64-netinst.iso
$ wget -c https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/iso-cd/SHA256SUMS
$ sha256sum -c SHA256SUMS
firmware-9.4.0-amd64-netinst.iso: OK
```

Write the installer to an **unmounted** USB storage device using `dd` as root. **BE VERY CAREFUL TO NOTE THE PROPER DEVICE. ALL DATA ON THE DEVICE WILL BE OVERWRITTEN.**

*Example:* On a Linux system, if a USB stick appears as `sde1`, then write the installer to the device using ...

```bash
$ sudo dd if=firmware-9.4.0-amd64-netinst.iso of=/dev/sde bs=4M && sudo sync
```

Minimal installer (requires network connection) downloads all the latest packages during setup. [^4]

## 1. Launch

![Install](/img/minimal-debian/001.png)

![Select language](/img/minimal-debian/002.png)

![Select location](/img/minimal-debian/003.png)

![Configure keyboard](/img/minimal-debian/004.png)

![Detecting link](/img/minimal-debian/005.png)

![DHCP](/img/minimal-debian/006.png)

![Hostname](/img/minimal-debian/007.png)

![Domain](/img/minimal-debian/008.png)

![Root password](/img/minimal-debian/009.png)

![Verify password](/img/minimal-debian/010.png)

![Full name](/img/minimal-debian/011.png)

![Username](/img/minimal-debian/012.png)

![User password](/img/minimal-debian/013.png)

![Verify password](/img/minimal-debian/014.png)

![Select time zone](/img/minimal-debian/015.png)

## 2. Partitions

Sample layout:

* sda1 is a 512MB `boot` partition
* sda2 uses remaining storage as a LUKS encrypted partition
* LVM installed on encrypted partition; contains volume group with 3 logical volumes: `root` + `swap` + `home`

![Partitioning method](/img/minimal-debian/100.png)

![Partition disks](/img/minimal-debian/101.png)

![Partition table](/img/minimal-debian/102.png)

![Free space](/img/minimal-debian/103.png)

![New partition](/img/minimal-debian/104.png)

![Partition size](/img/minimal-debian/105.png)

![Primary partition](/img/minimal-debian/106.png)

![Beginning](/img/minimal-debian/107.png)

Modify the default mount options ... 

```bash
Mount point: /boot
Bootable flag: on
```

![Mount point](/img/minimal-debian/108.png)

![Boot](/img/minimal-debian/109.png)

![Bootable flag](/img/minimal-debian/110.png)

![Done](/img/minimal-debian/111.png)

Assign the remaining storage to the encrypted partition ...

![Free space](/img/minimal-debian/200.png)

![New partition](/img/minimal-debian/201.png)

![Partition size](/img/minimal-debian/202.png)

![Primary partition](/img/minimal-debian/203.png)

Modify default mount options ...

```bash
Use as: physical volume for encryption
Erase data: no
```

If the hard disk has not been securely wiped prior to installing Debian you may want to configure `Erase data: yes`. Note, however, depending on the size of the disk this operation can last several hours.

![Use as](/img/minimal-debian/204.png)

![Physical volume for encryption](/img/minimal-debian/205.png)

![Erase data](/img/minimal-debian/206.png)

![Done](/img/minimal-debian/207.png)

![Configure encrypted volumes](/img/minimal-debian/208.png)

![Write changes](/img/minimal-debian/209.png)

![Create encrypted](/img/minimal-debian/210.png)

![Devices to encrypt](/img/minimal-debian/211.png)

![Finish](/img/minimal-debian/212.png)

![Passphrase](/img/minimal-debian/213.png)

![Verify passphrase](/img/minimal-debian/214.png)

Select encrypted volume and modify default mount options ...

```bash
Use as: physical volume for LVM
```

![Select](/img/minimal-debian/300.png)

![Use as](/img/minimal-debian/301.png)

![Physical volume for LVM](/img/minimal-debian/302.png)

![Done](/img/minimal-debian/303.png)

Create a LVM volume group with 3 logical volumes ...

![Configure LVM](/img/minimal-debian/304.png)

![Write changes](/img/minimal-debian/305.png)

![Create volume group](/img/minimal-debian/306.png)

![Vg name](/img/minimal-debian/307.png)

![Device for vg](/img/minimal-debian/308.png)

![Create lv](/img/minimal-debian/309.png)

![Vg](/img/minimal-debian/310.png)

![Lv root](/img/minimal-debian/311.png)

![Lv root size](/img/minimal-debian/312.png)

![Create lv](/img/minimal-debian/313.png)

![Vg](/img/minimal-debian/314.png)

![Lv swap](/img/minimal-debian/315.png)

![Lv swap size](/img/minimal-debian/316.png)

![Create lv](/img/minimal-debian/317.png)

![Vg](/img/minimal-debian/318.png)

![Lv home](/img/minimal-debian/319.png)

Set aside some unused space for future requirements. LVM makes it easy to expand or create new filesystems as needed ...

![Lv home size](/img/minimal-debian/320.png)

![Finish lvm](/img/minimal-debian/321.png)

Select LV root and modify default mount options ...

```bash
Use as: Ext4
Mount point: /
```

![Select lv root](/img/minimal-debian/400.png)

![Use as](/img/minimal-debian/401.png)

![Ext4](/img/minimal-debian/402.png)

![Mount point](/img/minimal-debian/403.png)

![Root](/img/minimal-debian/404.png)

![Done](/img/minimal-debian/405.png)

Select LV swap and modify default mount options ...

```bash
Use as: swap area
```

![Select lv swap](/img/minimal-debian/500.png)

![Use as](/img/minimal-debian/501.png)

![Swap](/img/minimal-debian/502.png)

![Done](/img/minimal-debian/503.png) 

Select LV home and modify default mount options ... [^5]

```bash
Use as: Ext4
Mount point: /home
Reserved blocks: 1%
```

![Select lv home](/img/minimal-debian/600.png)

![Use as](/img/minimal-debian/601.png)

![Ext4](/img/minimal-debian/602.png)

![Mount point](/img/minimal-debian/603.png)

![Home](/img/minimal-debian/604.png)

![Reserved blocks](/img/minimal-debian/605.png)

![Percent](/img/minimal-debian/606.png)

![Done](/img/minimal-debian/607.png)

Write changes to disk ...

![Finish partitioning](/img/minimal-debian/700.png)

![Write changes](/img/minimal-debian/701.png)

![Installing](/img/minimal-debian/702.png)

## 3. Install packages and finish up

![Scan](/img/minimal-debian/800.png)

![Archive mirror](/img/minimal-debian/801.png)

Use the Debian global mirrors service [deb.debian.org](https://wiki.debian.org/DebianGeoMirror) ...

![Mirror hostname](/img/minimal-debian/802.png)

![Mirror directory](/img/minimal-debian/803.png)

![Proxy](/img/minimal-debian/804.png)

![Pakage survey](/img/minimal-debian/805.png)

Select only `[*] standard system utilities` and leave the remaining tasks [^6] unmarked ...
    
![Software selection](/img/minimal-debian/806.png)

Packages are downloaded and the installer makes its finishing touches ...

![Install GRUB to MBR](/img/minimal-debian/807.png)

![GRUB device](/img/minimal-debian/808.png)

![Finish](/img/minimal-debian/809.png)

## 4. First boot

![GRUB menu](/img/minimal-debian/900.png)

User is prompted for the passphrase to unlock the encrypted partition ...

![Unlock passphrase](/img/minimal-debian/901.png)

![Login](/img/minimal-debian/902.png)

Login and run `timedatectl` to confirm system date+time is properly configured ...

```bash
timedatectl
```

## 5. Network

Check which network interfaces are detected and settings ...

```bash
ip a
```

**Wired** interfaces are usually auto-configured by default and assigned an IP address courtesy of DHCP.

To assign a **static** address, deactivate the wired interface and create a new entry in `/etc/network/interfaces`. [^7] Sample entry for `enp3s0` ...

```bash
# The primary network interface
auto enp3s0
iface enp3s0 inet static
address 192.168.1.88
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 8.8.8.8 8.8.4.4
```

Bring up|down interface with `if{up,down} enp3s0`.

Create a temporary **wireless** interface connection to WPA2 encrypted access points manually using `wpa_supplicant` + `wpa_passphrase` + `dhclinet`. Sample setup of `wlp1s0` (as root) ...

```bash
ip link set wlp1s0 up             ## bring up interface
iw dev wlp1s0 link                ## get link status
iw dev wlp1s0 scan | grep SSID    ## scan for access points
wpa_supplicant -i wlp1s0 -c<(wpa_passphrase "MY_SSID" "MY_PASSPHRASE")   ## connect to WPA/WPA2 ... add '-B' to background process
dhclient wlp1s0                   ## obtain IP address
```

More permanent configurations may be set in `interfaces`. Sample setup [^8] with a static IP address ...

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

Once a link is established install an (optional) network manager utility. Packages `network-manager` and `network-manager-gnome` provide the console `nmcli` and graphical `nm-applet` clients respectively . Comment out (deactivate) any entries in `interfaces` that will be managed by `network-manager`.

## 6. Upgrade

Install any upgrades ...

```bash
apt update; apt full-upgrade
```

## 7. Secure access using SSH keys

Create cryptographic keys, install the OpenSSH server, and [configure remote access](https://www.circuidipity.com/ssh-keys/).

## 8. Main, non-free, contrib, and backports

Debian uses three archives to distinguish between software packages based on their licenses. **Main** is enabled by default and includes everything that satisfies the conditions of the [Debian Free Software Guidelines](https://www.debian.org/social_contract#guidelines). **Non-free** contains packages that do not meet all the conditions of the DFSG but can be freely distributed, and **contrib** packages are open-source themselves but rely on software in non-free to work.

[Backports](https://backports.debian.org/) contains packages drawn from the testing (and sometimes unstable) archive and modified to work in the current stable release. All backports are disabled by default (to prevent unintended system upgrades) and are installed on a per PACKAGE basis by running ...

```bash
apt -t stretch-backports install PACKAGE
```

Modify `/etc/apt/sources.list` to add contrib, non-free, and backports ...

```bash
# Base repository
deb http://deb.debian.org/debian/ stretch main contrib non-free
deb-src http://deb.debian.org/debian/ stretch main contrib non-free

# Security updates
deb http://security.debian.org/debian-security stretch/updates main contrib non-free
deb-src http://security.debian.org/debian-security stretch/updates main contrib non-free

# Stable updates
deb http://deb.debian.org/debian stretch-updates main contrib non-free
deb-src http://deb.debian.org/debian stretch-updates main contrib non-free

# Stable backports
deb http://deb.debian.org/debian stretch-backports main contrib non-free
deb-src http://deb.debian.org/debian stretch-backports main contrib non-free
```

Any time `sources.list` is modified be sure to update the package database ...

```bash
apt update
```

## 9. Automatic security updates

Fetch and install the latest fixes courtesy of [unattended upgrades](http://www.circuidipity.com/unattended-upgrades.html). Useful feature for a [home server](https://www.circuidipity.com/home-server/); on the desktop I manage updates myself.

## 10. Sudo

Install `sudo` to temporarily provide your USER (example: `foo`) account with root privileges ...

```bash
apt install sudo
adduser foo sudo
```

To allow `foo` to shutdown or reboot the system, first create the file `/etc/sudoers.d/00-alias` containing ...

```bash
# Cmnd alias specification
Cmnd_Alias SHUTDOWN_CMDS = /sbin/poweroff, /sbin/reboot, /sbin/shutdown
```

Starting with Stretch, if you run as USER the command `dmesg` to read the contents of the kernel message buffer you will see ...

```bash
dmesg: read kernel buffer failed: Operation not permitted
```

Turns out it is a (security) [feature not a bug](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=842226#15)!

To allow `foo` to read the kernel log without being prompted for a password - and use our newly-created `Cmnd_Alias SHUTDOWN_CMDS` - create the file `/etc/sudoers.d/01-nopasswd` containg the `NOPASSWD` option ...

```bash
# Allow specified users to execute these commands without password
foo ALL=(ALL) NOPASSWD: SHUTDOWN_CMDS, /bin/dmesg
```

I add aliases for the commands in my `~/.bashrc` to auto-include `sudo` ...

```bash
alias dmesg='sudo dmesg'
alias poweroff='sudo /sbin/poweroff'
alias reboot='sudo /sbin/reboot'
alias shutdown='sudo /sbin/shutdown'
```

## 11. SSD

[Periodic TRIM](https://www.digitalocean.com/community/tutorials/how-to-configure-periodic-trim-for-ssd-storage-on-linux-servers) optimizes performance on SSD storage. Enable a weekly task that discards unused blocks on the drive ...

```bash
cp /usr/share/doc/util-linux/examples/fstrim.{service,timer} /etc/systemd/system/
systemctl enable fstrim.timer
```

## 12. Where to go next ...

... is up to YOU. A [home server](https://www.circuidipity.com/home-server/)? A workstation with your own [custom desktop](https://www.circuidipity.com/openbox/)?

Happy hacking!

#### Notes

[^1]: Image courtesy of [jschild](http://jschild.deviantart.com/art/Facebook-cover-debian-Darth-Vader-380351614).

[^2]: Note that encrypted `root` **requires** an unencrypted `boot`.

[^3]: Very helpful! [LVM post on the Arch Wiki](https://wiki.archlinux.org/index.php/LVM).

[^4]: An alternative is adding the image to a [USB stick with multiple Linux installers](https://www.circuidipity.com/multi-boot-usb/).

[^5]: Reserved blocks can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large **non-root partitions** extra space can be gained by reducing the default 5% reserve set aside by Debian to 1%.

[^6]: Task selection menu can be used post-install by running (as root) `tasksel`.

[^7]: Problem: setting the network interface to static address can result in `/etc/resolv.conf` being overwritten every few minutes with an IPv6 address that breaks DNS. The "fix" is to maually set `nameserver 8.8.8.8` in resolv.conf and install the `resolvconf` package. Note that `dns-nameservers` entries are ignored if resolvconf is not installed.

[^8]: Multiple wireless static IP address setups can be created with `iface wlp1s0_NAME inet static` and [de]activated with `if{up.down} wlp1s0=wlp1s0_NAME`.
