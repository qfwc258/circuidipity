==================================================
Arch Linux installation with encrypted root + swap
==================================================

:date: 2015-03-26 21:00:00
:slug: arch-install-encrypt
:tags: arch, linux, chromebook

My notes for installing **Arch Linux** that follow a condensed path through the `Beginner's Guide <https://wiki.archlinux.org/index.php/Beginners%27_guide>`_ plus extra steps to configure LUKS-encrypted root + swap.

Let's go!
=========

**Target:** Acer ``C720-2848`` Chromebook (16GB SSD) with `Chrome OS removed and ready for full-featured Linux <http://www.circuidipity.com/c720-lubuntubook.html>`_.

0. Install media
================

`Download <https://www.archlinux.org/download/>`_ the combined 32+64bit installer and flash the image to a USB stick:

.. code-block:: bash

    $ sudo dd bs=4M if=archlinux*-dual.iso of=/dev/sdX

1. Net connection
=================

Connect the USB stick and boot the installer. Identify the name of the device net interfaces:

.. code-block:: bash

    # ip link

Chromebook wireless interface is ``wlp1s0``. Connect to an access point using ``netctl`` and its interactive ``wifi-menu`` utility:

.. code-block:: bash

    # wifi-menu

2. Wipe storage 
===============

Secure wipe storage before installation (16GB SSD took 22-23 minutes):

.. code-block:: bash

    # cryptsetup open --type plain /dev/sdX container
    # dd if=/dev/zero of=/dev/mapper/container

Upon completion close the container:

.. code-block:: bash

    # cryptsetup close /dev/mapper/container

Source: `Dm-crypt drive preparation <https://wiki.archlinux.org/index.php/Dm-crypt/Drive_preparation>`_

3. Partition
============

Detect storage devices:

.. code-block:: bash

    # lsblk

SSD identified as ``sda``. Use ``gpt`` to create a 4 partition layout:

* sda1 - 1M - BIOS boot partition (type: ``ef02``)
* sda2 - 300M - boot (unencrypted)
* sda3 - 1GB - swap (encrypted)
* sda4 - remaining space - root (encrypted)

Normally I create a separate partition for ``$HOME`` but on smaller storage devices I make a single encrypted ``root`` and a (required) unencrypted ``boot``:

.. code-block:: bash

    # gdisk /dev/sda
    o (new partition table)
    ...
    w

4. Encrypted root
=================

Using above partition layout:

.. code-block:: bash

    # cryptsetup -y -v luksFormat /dev/sda4
    # cryptsetup open /dev/sda4 cryptroot
    # mkfs.ext4 /dev/mapper/cryptroot
    # mount -t ext4 /dev/mapper/cryptroot /mnt

5. Boot
=======

Setup:

.. code-block:: bash

    # mkfs.ext4 /dev/sda2
    # mkdir /mnt/boot
    # mount -t ext4 /dev/sda2 /mnt/boot

6. Install
==========

Install the Arch base system:

.. code-block:: bash

    # pacstrap -i /mnt base base-devel

7. Fstab
========

Generate a base ``/etc/fstab`` and modify:

.. code-block:: bash

    # genfstab -U -p /mnt >> /mnt/etc/fstab
    # nano /mnt/etc/fstab

8. Chroot
=========

Chroot into the freshly-installed Arch base system to configure:

.. code-block:: bash

    # arch-chroot /mnt /bin/bash

9. Locale
=========

Configure a locale suitable for the region:

.. code-block:: bash

    # nano /etc/locale.gen
    ...
    en_CA.UTF-8 UTF-8
    ...
    # locale-gen
    # echo LANG=en_CA.UTF-8 > /etc/locale.conf
    # export LANG=en_CA.UTF-8

10. Time zone
=============

Configure local time:

.. code-block:: bash

    # ln -s /usr/share/zoneinfo/Canada/Eastern /etc/localtime

11. Hardware clock
==================

Set the hardware clock to UTC:

.. code-block:: bash

    # hwclock --systohc --utc

12. Hostname
============

Make a name for the new Arch installation:

.. code-block:: bash

    # echo myhostname > /etc/hostname

... and modify ``/etc/hosts``:

.. code-block:: bash

    #<ip-address> <hostname.domain.org> <hostname>
    127.0.0.1 localhost.localdomain localhost myhostname
    ::1   localhost.localdomain localhost myhostname

13. Network
===========

Chromebook wireless interface is an Atheros ``AR9462`` using the ``ath9k`` kernel module. It does not require separate firmware.

Install wireless tools:

.. code-block:: bash

    # pacman -S iw wpa_supplicant dialog

**Wait until after reboot** to configure interface with ``wifi-menu``.

14. Initial ramdisk
===================

Modify ``/etc/mkinitcpio.conf`` by adding an ``encrypt`` hook before ``filesystems``:

.. code-block:: bash

    HOOKS="... encrypt ... filesystems ..."

Re-generate the initramfs image:

.. code-block:: bash

    # mkinitcpio -p linux

15. Password
============

Set root password:

.. code-block:: bash

    # passwd

16. Bootloader
==============

Download GRUB:

.. code-block:: bash

    # pacman -S grub os-prober

Configure ``/etc/default/grub`` to handle encrypted root:

.. code-block:: bash

    GRUB_CMDLINE_LINUX="cryptdevice=/dev/sda4:cryptroot"

Install GRUB to storage device and auto-generate ``grub.cfg``:

.. code-block:: bash

    # grub-install --target=i386-pc --recheck /dev/sda
    # grub-mkconfig -o /boot/grub/grub.cfg

17. Prepare non-root encrypted partitions
=========================================

Add encrypted swap to ``/etc/crypttab``:

.. code-block:: bash

    cryptswap    /dev/sda3   /dev/urandom    swap,cipher=aes-cbc-essiv:sha256,size=256

... and modify ``/etc/fstab``:

.. code-block:: bash

    /dev/mapper/cryptswap    none    swap    sw      0 0

18. Unmount and reboot
======================

.. code-block:: bash

    # exit
    # umount /mnt/boot
    # umount /mnt
    # cryptsetup close /dev/mapper/cryptroot
    # reboot

Welcome to Arch. Happy hacking!
