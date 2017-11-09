---
title: "LVM and encrypted Logical Volumes"
date: "2017-05-13"
publishDate: "2017-05-13"
tags:
  - lvm
  - crypto
  - linux
slug: "lvm-crypt-lv"
aliases:
  - /lvm-crypt-lv.html
---

I have been playing with the **Logical Volume Manager** (LVM) on my recent Debian installs. Instead of creating a traditional partition layout on a hard drive, LVM adds a layer of abstraction over physical storage that allows the creation of "virtual" partitions. 

For my [netbook home server setup](http://www.circuidipity.com/laptop-home-server) I used the Debian installer's manual partitioning tools to assign a partition to LVM, create a **Volume Group** (VG) and **Logical Volumes** (LVs), with plenty of storage space to spare. [^1] After a successful first boot I configure an encrypted container for data storage that is manually mounted by a non-root user. I don't want an unattended server halting in the boot process waiting for a passphrase or any necessary boot mountpoints to reside on an encrypted partition.

## Let's go!

Scan my netbook for devices visible to LVM ... 

```bash
sudo lvmdiskscan
    /dev/vg/root              [      14.90 GiB]
    /dev/sda1                 [     487.00 MiB]
    /dev/vg/swap              [     952.00 MiB]
    /dev/sda2                 [     465.28 GiB] LVM physical volume
    /dev/mapper/vg-swap_crypt [     952.00 MiB]
    3 disks
    1 partition
    0 LVM physical volume whole disks
    1 LVM physical volume
```

Check for free space in the volume group ...

```bash
sudo vgdisplay
    [...]
    Free  PE / Size       115060 / 449.45 GiB
    [...]
```

## 0. Create

I create a 400GB `data` logical volume in the volume group ...

```bash
sudo lvcreate --size 400G vg --name data
```

Information about the LVs can be displayed with the `lvdisplay` command.

## 1. Encrypt

Configure LUKS encryption on the newly-created LV ...

```bash
sudo cryptsetup luksFormat /dev/vg/data
```

Open LV `data` under `vg-data_crypt`, format with a filesystem, and mount ... [^2]

```bash
sudo cryptsetup open /dev/vg/data vg-data_crypt
sudo mkfs.ext4 -m 1 /dev/mapper/vg-data_crypt
sudo mount /dev/mapper/vg-data_crypt /mnt
```

When finished, unmount the filesystem and close the encrypted LV ...

```bash
sudo umount /mnt
sudo cryptsetup close /dev/mapper/vg-data_crypt
```

## 2. Mountpoint

I create a dedicated mountpoint for the LV in `/media` ...

```bash
sudo mkdir /media/crypt_data
```

Modify `/etc/fstab` and allow mounting by a non-root user ...

```bash
/dev/mapper/vg-data_crypt /media/crypt_data        ext4    relatime,noauto,user       0       0
```

Open the LV and mount ...

```bash
sudo cryptsetup open /dev/vg/data vg-data_crypt
mount /media/crypt_data
```

Happy hacking!

#### Notes

[1]: For setting up LVM from the beginning and learning about its tools the LVM entries on [wiki.debian.org](https://wiki.debian.org/LVM) and [wiki.archlinux.org](https://wiki.archlinux.org/index.php/LVM) are very helpful!

[2]: Reserved blocks can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large non-root partitions extra space can be gained by reducing the default 5% reserve to 1% with option `-m <percent>`.

