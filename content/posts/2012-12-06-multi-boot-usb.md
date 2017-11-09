---
title: "Transform a USB stick into a boot device packing multiple Linux distros"
date: "2017-07-16"
publishDate: "2012-12-06"
tags:
  - grub
  - shell
  - linux
slug: "multi-boot-usb"
aliases:
  - /multi-boot-usb.html
---

<img style="float:right" src="/img/grubs-300.png" />

Transform removable USB storage into a dual-purpose device that is both a storage medium usable under Linux, Windows, and Mac OS and a GRUB boot device capable of loopback mounting Linux distro ISO files. [^1]

## Let's go!

**WARNING!** In this HOWTO the USB device is identified as **sdx** and contains a single partition **sdx1**. Make careful note of the drive and partition labels on your system. The following steps will **destroy all data** currently stored on the device.

## 0. Format

Create a `FAT32` partition on the **unmounted** USB device ...

```bash
sudo mkfs.vfat -n MULTIBOOT /dev/sdx1
```

## 1. Boot and iso

Mount the USB device to MOUNTPOINT and create a `boot` folder for GRUB files and a `iso` folder to hold Linux distro images ...

```bash
mkdir -p /media/MOUNTPOINT/boot/{grub,iso,debian}
```

## 2. GRUB

Install GRUB to the **Master Boot Record (MBR)** of the USB device at MOUNTPOINT ...

```bash
sudo grub-install --target=i386-pc --force --recheck --boot-directory=/media/MOUNTPOINT/boot /dev/sdx
```

## 3. Linux images

Download Linux distro image (ISO) files and place in the newly-created `boot/iso` folder on the USB device. I have installed ...

* **SystemRescueCd** - Collection of [Linux repair tools](http://www.system-rescue-cd.org/)
* **Debian Stretch Netinst+firmware** - [64bit](https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/iso-cd/) and [32bit](https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current/i386/iso-cd/) installers
* **BunsenLabs** - Lightweight distro based on Debian stable release; [64bit, 32bit, and NonPAE installers](https://kelaino.bunsenlabs.org/ddl/)
* **Lubuntu 16.04 Live Mode + Desktop Installer** - [64bit and 32bit](http://cdimage.ubuntu.com/lubuntu/releases/16.04.2/release/) desktop images allow trying Lubuntu before installing
* **Ubuntu 16.04 LTS Mini-Installers** - [64bit mini.iso](http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/netboot/) and [32bit mini.iso](http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-i386/current/images/netboot/)

### 3.1 Debian Netinst

Problem: This was a bit tricky to get working. Selecting `firmware-9.0.0-ARCH-netinst.iso` from the GRUB menu would get things started but the install would fail at the stage where the ISO needs to be located and mounted. Debian's netinst images do not include the **iso-scan** package , which is required for searching and loading ISO images.

**[ Fix! ]** Bypass the `initrd.gz` that is on the ISO images and use ones that *do* contain the iso-scan package, [^2] which I retrieved from the **hd-media** installers ...

```bash
mkdir /media/MOUNTPOINT/boot/debian/install.{amd,386}
cd /media/MOUNTPOINT/boot/debian/install.amd
wget http://ftp.debian.org/debian/dists/stable/main/installer-amd64/current/images/hd-media/initrd.gz
cd .. /install.386
wget http://ftp.debian.org/debian/dists/stable/main/installer-i386/current/images/hd-media/initrd.gz
```

## 4. GRUB configuration

Create `boot/grub/grub.cfg` and write entries for the ISO files to be copied to the USB device. Note that each Linux distro is a bit different in the manner its booted by GRUB and may require a bit of research. This post on boot entries for a [number of distributions](https://wiki.archlinux.org/index.php/Multiboot_USB_drive#Boot_entries_for_other_distributions) on the Arch Linux Wiki might prove helpful.

Link: My own [grub.cfg.sample](https://github.com/vonbrownie/grubs/blob/master/boot/grub/grub.cfg.sample).

## 5. Run

All done! Reboot. Configure the BIOS to accept removable USB storage as boot device. Reboot and GRUB displays a menu of the Linux distros installed on the USB device. Launch and enjoy!

When finished, simply reboot and return to using the USB device as a VFAT-formatted storage medium.

## 6. GRUBS Reanimated USB Boot Stick

I created the [GRUBS shell script](https://github.com/vonbrownie/grubs) that prepares USB storage devices using the above steps and uploaded it to GitHub.

Happy hacking!

#### Notes

[^1]: Image credit: Flickr user Peter via Creative Commons, retrieved from [InsideClimate News](https://insideclimatenews.org/species/birds/ad%C3%A9lie-penguin).

[^2]: Helpful in figuring out the iso-scan package wrinkle: [Multi-boot stick update](http://126kr.com/article/6xzqwchvlv6)
