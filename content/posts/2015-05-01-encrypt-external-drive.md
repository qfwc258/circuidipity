---
title: "Configure an encrypted external USB hard drive in Linux"
date: "2015-05-01"
publishDate: "2015-05-01"
tags:
  - crypto
  - linux
slug: "encrypt-external-drive"
---

Using an external USB hard drive is part of my personal backup plan (the other part is backing up to a [home server](http://www.circuidipity.com/home-server.html)). I actually use 2 multi-terabyte drives. One drive is in my possession and the other drive I store offsite at a friend's home. Periodically I swap the drives and update the data.

## Let's go!

To guard against loss or theft its a good idea to encrypt the hard drive. I prepare the device using **Linux Unified Key Setup** (LUKS) and the `cryptsetup` utility.

**WARNING!** Make careful note of the drive and partition labels. The following steps **will destroy all data** currently stored on the drive.

## 0. Prepare

Download `cryptsetup` if not already installed. Connect the external drive, leave it **unmounted**, and make note of the device label (`sdb`, `sdc` ...) ...

```bash
lsblk
```

**Optional:** Overwrite the device with zeros for added security. This can take several hours depending on storage size. **Random number generation** is even more secure but takes much longer ...

```bash
sudo dd bs=4M if=/dev/zero of=/dev/sdX
```

## 1. Partition

Create a single partition using a favourite partitioning utility (`fdisk`, `gparted`...) that fills the entire drive. Encrypt the partition and assign a password ...

```bash
sudo cryptsetup luksFormat /dev/sdX1
sudo cryptsetup open /dev/sdX1 sdX1_crypt
```

## 2. Filesystem

Install a filesystem (example: `ext4`) [^1] and mount the partition to gain access to the storage ...

```bash
sudo mkfs.ext4 -E lazy_itable_init=0,lazy_journal_init=0 /dev/mapper/sdX1_crypt
sudo mount -t ext4 /dev/mapper/sdX1_crypt /mnt
```

Before disconnecting the drive the partition must be unmounted and the encrypted device must be closed ...

```bash
sudo umount /mnt
sudo cryptsetup close /dev/mapper/sdX1_crypt
```

## 3. Mountpoint

A file manager like `nautilus` will auto-mount and unmount encrypted partitions. For crafting a backup script it is useful to assign a **default mountpoint** to the encrypted partition... that is, whenever the USB drive is connected it will always be mounted to the same location.

Mount the encrypted drive. Retrieve the UUID string for the encrypted partition, and create a custom mountpoint (example: `/media/usb_crypt`) ...

```bash
ls /dev/disk/by-uuid/ | grep dm-  # outputs '<STRING> -> ../../dm-X'
sudo mkdir /media/usb_crypt
```

Unmount the drive and create an entry in `/etc/fstab` for the new custom mount point ...

```bash
UUID=<STRING>   /media/usb_crypt    ext4    rw.users,noauto,noatime    0   0
```

Next time the drive is auto-mounted it will be assigned to `/media/usb_crypt`.

Happy hacking!

#### Notes

[^1]: Writing `ext4` with options `lazy_itable_init=0,lazy_journal_init=0` initializes the inodes and journal at creation time vs a gradual process during mount times. If you wonder why your newly-formatted drive's activity LED is blinking away... install and run `iotop` and take note of `ext4lazyinit` and [Lazy Initialization](https://www.thomas-krenn.com/en/wiki/Ext4_Filesystem#Lazy_Initialization).
