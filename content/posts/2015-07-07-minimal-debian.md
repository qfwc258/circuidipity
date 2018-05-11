---
title: "Minimal Debian"
date: "2018-05-11"
publishDate: "2015-07-07"
tags:
  - debian
  - linux
  - crypto
  - lvm
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

![Install](/img/screenshot/debianInstallLvm/001-stretch.png)

![Select language](/img/screenshot/debianInstallLvm/002.png)

![Select location](/img/screenshot/debianInstallLvm/003.png)

![Configure keyboard](/img/screenshot/debianInstallLvm/004.png)

![Hostname](/img/screenshot/debianInstallLvm/005.png)

![Domain](/img/screenshot/debianInstallLvm/006.png)

![Root password](/img/screenshot/debianInstallLvm/007.png)

![Verify password](/img/screenshot/debianInstallLvm/008.png)

![Full name](/img/screenshot/debianInstallLvm/009.png)

![Username](/img/screenshot/debianInstallLvm/010.png)

![User password](/img/screenshot/debianInstallLvm/011.png)

![Verify password](/img/screenshot/debianInstallLvm/012.png)

![Select time zone](/img/screenshot/debianInstallLvm/013.png)

## 2. Partitions

Sample layout:

* sda1 is a 512MB `boot` partition
* sda2 uses the remaining storage as a LUKS encrypted partition
* LVM is installed on the encrypted partition, and contains a volume group with the 3 logical volumes `root` + `swap` + `home`

![Partitioning method](/img/screenshot/debianInstallLvm/100.png)

![Partition disks](/img/screenshot/debianInstallLvm/101.png)

![Partition table](/img/screenshot/debianInstallLvm/102.png)

![Free space](/img/screenshot/debianInstallLvm/103.png)

![New partition](/img/screenshot/debianInstallLvm/104.png)

![Partition size](/img/screenshot/debianInstallLvm/105.png)

![Primary partition](/img/screenshot/debianInstallLvm/106.png)

![Beginning](/img/screenshot/debianInstallLvm/107.png)

Modify the default mount options ... [^5]

```bash
Mount point: /boot
Mount options: relatime
Bootable flag: on
```

![Boot](/img/screenshot/debianInstallLvm/108.png)

![Free space](/img/screenshot/debianInstallLvm/109.png)

![New partition](/img/screenshot/debianInstallLvm/104.png)

Assign the remaining storage to the encrypted partition ...

![Partition size](/img/screenshot/debianInstallLvm/110.png)

![Primary partition](/img/screenshot/debianInstallLvm/106.png)

Modify the default mount options ...

```bash
Use as: physical volume for encryption
Erase data: no
```

If the hard disk has not been securely wiped prior to installing Debian you may want to configure `Erase data: yes`. Note, however, depending on the size of the disk this operation can last several hours.

![Physical volume for encryption](/img/screenshot/debianInstallLvm/111.png)

![Configure encrypted volumes](/img/screenshot/debianInstallLvm/112.png)

![Write changes](/img/screenshot/debianInstallLvm/113.png)

![Create encrypted](/img/screenshot/debianInstallLvm/114.png)

![Devices to encrypt](/img/screenshot/debianInstallLvm/115.png)

![Finish](/img/screenshot/debianInstallLvm/116.png)

![Passphrase](/img/screenshot/debianInstallLvm/117.png)

![Verify passphrase](/img/screenshot/debianInstallLvm/118.png)

![Partition disks](/img/screenshot/debianInstallLvm/119.png)

Modify the default mount options ...

```bash
Use as: physical volume for LVM
```

![Physical volume for LVM](/img/screenshot/debianInstallLvm/120.png)

![Configure LVM](/img/screenshot/debianInstallLvm/121.png)

![Write changes](/img/screenshot/debianInstallLvm/122.png)

![Create volume group](/img/screenshot/debianInstallLvm/123.png)

![Vg name](/img/screenshot/debianInstallLvm/124.png)

![Device for vg](/img/screenshot/debianInstallLvm/125.png)

![Create lv](/img/screenshot/debianInstallLvm/126.png)

![Vg](/img/screenshot/debianInstallLvm/127.png)

![Lv root](/img/screenshot/debianInstallLvm/128.png)

![Lv root size](/img/screenshot/debianInstallLvm/129.png)

![Create lv](/img/screenshot/debianInstallLvm/130.png)

![Vg](/img/screenshot/debianInstallLvm/131.png)

![Lv swap](/img/screenshot/debianInstallLvm/132.png)

![Lv swap size](/img/screenshot/debianInstallLvm/133.png)

![Create lv](/img/screenshot/debianInstallLvm/134.png)

![Vg](/img/screenshot/debianInstallLvm/135.png)

![Lv home](/img/screenshot/debianInstallLvm/136.png)

Set aside some unused space for future requirements. LVM makes it easy to expand or create new filesystems as needed ...

![Lv home size](/img/screenshot/debianInstallLvm/137.png)

![Finish lvm](/img/screenshot/debianInstallLvm/138.png)

![Select lv root](/img/screenshot/debianInstallLvm/139.png)

Modify the default mount options ...

```bash
Use as: Ext4
Mount point: /
Mount options: relatime
```

![Lv root config](/img/screenshot/debianInstallLvm/140.png)

![Select lv swap](/img/screenshot/debianInstallLvm/141.png)

Modify the default mount options ...

```bash
Use as: swap area
```

![Lv swap config](/img/screenshot/debianInstallLvm/142.png)

![Select lv home](/img/screenshot/debianInstallLvm/143.png)

Modify the default mount options ... [^6]

```bash
Use as: Ext4
Mount point: /home
Mount options: relatime
Reserved blocks: 1%
```

![Lv home config](/img/screenshot/debianInstallLvm/144.png)

![Finish partitioning](/img/screenshot/debianInstallLvm/145.png)

![Write changes](/img/screenshot/debianInstallLvm/146.png)

## 3. Install packages and finish up

![Configure package manager](/img/screenshot/debianInstallLvm/200.png)

Use the Debian global mirrors service [deb.debian.org](https://wiki.debian.org/DebianGeoMirror) ...

![Mirror hostname](/img/screenshot/debianInstallLvm/201-1.png)

![Mirror directory](/img/screenshot/debianInstallLvm/202.png)

![Proxy](/img/screenshot/debianInstallLvm/203.png)

![Popularity contest](/img/screenshot/debianInstallLvm/204.png)

Select only `[*] standard system utilities` and leave the remaining tasks [^7] unmarked ...
    
![Software selection](/img/screenshot/debianInstallLvm/205.png)

Packages are downloaded and the installer makes its finishing touches ...

![Downloading](/img/screenshot/debianInstallLvm/206.png)

![Install GRUB to MBR](/img/screenshot/debianInstallLvm/207.png)

![GRUB device](/img/screenshot/debianInstallLvm/208.png)

![Finish](/img/screenshot/debianInstallLvm/209.png)

## 4. First boot

![GRUB menu](/img/screenshot/debianInstallLvm/300.png)

User is prompted for the passphrase to unlock the encrypted partition ...

![Unlock passphrase](/img/screenshot/debianInstallLvm/301-1.png)

![Login](/img/screenshot/debianInstallLvm/302-stretch.png)

Login and run `timedatectl` to confirm system date+time is properly configured.

## 5. GRUB

After running a minimal install on my Acer C720 Chromebook with encrypted swap + home partitions I ran into this issue: ["Black screen instead of password prompt for boot encryption"](https://bugs.launchpad.net/ubuntu/+source/cryptsetup/+bug/1375435).

I had to enter my passphrase blind and `ALT+F1` to console. When I tried removing the GRUB options `splash` and/or `quiet` I lost the ability to enter the passphrase at all and a hard reset was required.

**[ Fix! ]** Modify `/etc/default/grub` ...

```bash
## Force the kernel to boot in normal text mode with '=text'
GRUB_GFXPAYLOAD_LINUX=text
```

... and update ...

```bash
update-grub
```

Now it works! My chromebook is currently the only device I have run into this issue.

Link: [GNU gfxpayload](https://www.gnu.org/software/grub/manual/html_node/gfxpayload.html)

## 6. Network

Check which network interfaces are detected and settings ...

```bash
ip a
```

**Wired** interfaces are usually auto-configured by default and assigned an IP address courtesy of DHCP.

To assign a **static** address, deactivate the wired interface and create a new entry in `/etc/network/interfaces`. [^8] Sample entry for `enp3s0` ...

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

More permanent configurations may be set in `interfaces`. Sample setup [^9] with a static IP address ...

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

## 7. Upgrade

Install any upgrades ...

```bash
apt update; apt full-upgrade
```

## 8. Secure access using SSH keys

Create cryptographic keys, install the OpenSSH server, and [configure remote access](https://www.circuidipity.com/ssh-keys/).

## 9. Main, non-free, contrib, and backports

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

## 10. Automatic security updates

Fetch and install the latest fixes courtesy of [unattended upgrades](http://www.circuidipity.com/unattended-upgrades.html). Useful feature for a [home server](https://www.circuidipity.com/home-server/); on the desktop I manage updates myself.

## 11. Sudo

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

## 12. SSD

[Periodic TRIM](https://www.digitalocean.com/community/tutorials/how-to-configure-periodic-trim-for-ssd-storage-on-linux-servers) optimizes performance on SSD storage. Enable a weekly task that discards unused blocks on the drive ...

```bash
cp /usr/share/doc/util-linux/examples/fstrim.{service,timer} /etc/systemd/system/
systemctl enable fstrim.timer
```

## 13. Where to go next ...

... is up to YOU. I created a [post-install configuration shell script](https://github.com/vonbrownie/linux-post-install/tree/master/scripts/debian-stable-setup) that builds on a minimal install towards a more complete console setup, and can also install the [i3 tiling window manager](https://www.circuidipity.com/i3-tiling-window-manager/) plus a packages collection suitable for a workstation.

Happy hacking!

#### Notes

[^1]: Image courtesy of [jschild](http://jschild.deviantart.com/art/Facebook-cover-debian-Darth-Vader-380351614).

[^2]: Note that encrypted `root` **requires** an unencrypted `boot`.

[^3]: Very helpful! [LVM post on the Arch Wiki](https://wiki.archlinux.org/index.php/LVM).

[^4]: An alternative is adding the image to a [USB stick with multiple Linux installers](https://www.circuidipity.com/multi-boot-usb/).

[^5]: `Mount options: relatime` decreases write operations and boosts drive speed.

[^6]: Reserved blocks can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large **non-root partitions** extra space can be gained by reducing the default 5% reserve set aside by Debian to 1%.

[^7]: Task selection menu can be used post-install by running (as root) `tasksel`.

[^8]: Problem: setting the network interface to static address can result in `/etc/resolv.conf` being overwritten every few minutes with an IPv6 address that breaks DNS. The "fix" is to maually set `nameserver 8.8.8.8` in resolv.conf and install the `resolvconf` package. Note that `dns-nameservers` entries are ignored if resolvconf is not installed.

[^9]: Multiple wireless static IP address setups can be created with `iface wlp1s0_NAME inet static` and [de]activated with `if{up.down} wlp1s0=wlp1s0_NAME`.
