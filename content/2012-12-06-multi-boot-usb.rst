=======================================================================
Transform a USB stick into a boot device packing multiple Linux distros
=======================================================================

:date: 2012-12-06 01:23:00
:tags: grub, shell, systemrescuecd, debian, ubuntu, linux
:slug: multi-boot-usb
:modified: 2017-04-23 21:43:00

Transform a standard USB stick into a dual-purpose device that is both a storage medium usable under Linux, Windows, and Mac OS and a GRUB boot device packing multiple Linux distros.

Let's go!
=========

.. role:: warning

:warning:`WARNING!` In this HOWTO the USB device is identified as **sdX** and contains a single partition **sdX1**. Make careful note of the drive and partition labels on your system. The following steps will **destroy all data** currently stored on the device.

0. Format
---------

Create a ``FAT32`` partition on the **unmounted** USB device ...

.. code-block:: bash

    $ sudo mkfs.vfat -n MULTIBOOT /dev/sdX1

1. Boot and iso
---------------

Mount the USB device to MOUNTPOINT and create a ``boot`` folder for GRUB files and a ``iso`` folder to hold Linux distro images ...

.. code-block:: bash

    $ mkdir -p /media/MOUNTPOINT/boot/{grub,iso,debian}

2. GRUB
-------

Install GRUB to the **Master Boot Record (MBR)** of the USB device at MOUNTPOINT ...

.. code-block:: bash

    $ sudo grub-install --target=i386-pc --force --recheck --boot-directory=/media/MOUNTPOINT/boot /dev/sdX

3. Linux images
---------------

Download and copy Linux ISO images to the newly-created ``boot/iso`` folder on the USB device. I have installed ...

* **SystemRescueCd** - `Collection of Linux repair tools <http://www.system-rescue-cd.org/>`_
* **Debian Jessie Netinst+firmware** - `64bit <https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/8.7.1+nonfree/amd64/iso-cd/>`_ and `32bit <https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/8.7.1+nonfree/i386/iso-cd/>`_ installers
* **Ubuntu 16.04 LTS Mini-Installers** - `64bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/netboot/>`_ and `32bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-i386/current/images/netboot/>`_

3.1 Debian Netinst
++++++++++++++++++

Problem: This was a bit tricky to get working. Selecting ``firmware-8.7.1-ARCH-netinst.iso`` from the GRUB menu would get things started but the install would fail at the stage where the ISO needs to be located and mounted. Debian's netinst images do not include the **iso-scan** package , which is required for searching and loading ISO images.

Fix: Bypass the ``initrd.gz`` that is on the ISO images and use ones that *do* contain the iso-scan package, which I retrieved from the **hd-media** installers ...

.. code-block:: bash

    $ mkdir /media/MOUNTPOINT/boot/debian/install.{amd,386}
    $ cd /media/MOUNTPOINT/boot/debian/install.amd
    $ wget http://ftp.debian.org/debian/dists/jessie/main/installer-amd64/current/images/hd-media/initrd.gz
    $ cd .. /install.386
    $ wget http://ftp.debian.org/debian/dists/jessie/main/installer-i386/current/images/hd-media/initrd.gz

Helpful resource in figuring this out! `Multi-boot stick update <http://126kr.com/article/6xzqwchvlv6>`_

4. GRUB configuration
---------------------

Create ``grub.cfg`` with entries for the Linux images copied to the USB device. Each distro is a little bit different in the manner its booted by GRUB. Example ... 

.. code-block:: bash

    # Config for GNU GRand Unified Bootloader (GRUB)
    # /boot/grub/grub.cfg

    # Timeout for menu
    set timeout=30

    # Default boot entry
    set default=0

    # Menu Colours
    set menu_color_normal=white/black
    set menu_color_highlight=white/green

    # Path to the partition holding ISO images (using UUID)
    #set imgdevpath="/dev/disk/by-uuid/UUID_value"
    # ... or...
    # Path to the partition holding ISO images (using device labels)
    #set imgdevpath="/dev/disk/by-label/label_value"
    set imgdevpath="/dev/disk/by-label/MULTIBOOT"

    # Boot ISOs
    menuentry "SystemRescueCd std-64bit" {
        set iso="/iso/systemrescuecd-x86.iso"
        loopback loop $iso
        linux (loop)/isolinux/rescue64 isoloop=$iso
        initrd (loop)/isolinux/initram.igz
    }

    menuentry "SystemRescueCd std-32bit" {
        set iso="/iso/systemrescuecd-x86.iso"
        loopback loop $iso
        linux (loop)/isolinux/rescue32 isoloop=$iso
        initrd (loop)/isolinux/initram.igz
    }

    menuentry "Debian Jessie - 64bit Netinst+firmware" {
        set iso="/boot/iso/firmware-8.7.1-amd64-netinst.iso"
        loopback loop $iso
        linux (loop)/install.amd/vmlinuz iso-scan/ask_second_pass=true iso-scan/filename=$iso priority=low vga=788 --- quiet 
        initrd /boot/debian/install.amd/initrd.gz
    }

    menuentry "Debian Jessie - 32bit Netinst+firmware" {
        set iso="/boot/iso/firmware-8.7.1-i386-netinst.iso"
        loopback loop $iso
        linux (loop)/install.386/vmlinuz iso-scan/ask_second_pass=true iso-scan/filename=$iso priority=low vga=788 --- quiet 
        initrd /boot/debian/install.386/initrd.gz
    }

    menuentry "Ubuntu 16.04 LTS - 64bit Mini-Installer" {
        set iso="/iso/ubuntu-lts-amd64-mini.iso"
        loopback loop $iso
        linux (loop)/linux boot=casper iso-scan/filename=$iso noprompt noeject
        initrd (loop)/initrd.gz
    }

    menuentry "Ubuntu 16.04 LTS - 32bit Mini-Installer" {
        set iso="/iso/ubuntu-lts-i386-mini.iso"
        loopback loop $iso
        linux (loop)/linux boot=casper iso-scan/filename=$iso noprompt noeject
        initrd (loop)/initrd.gz
    }

    menuentry "Ubuntu 16.04 LTS - 32bit Installer ('forcepae' for Pentium M)" {
        set iso="/iso/ubuntu-lts-i386-mini.iso"
        loopback loop $iso
        linux (loop)/linux boot=casper iso-scan/filename=$iso noprompt noeject forcepae
        initrd (loop)/initrd.gz
    }

Save ``grub.cfg`` to the USB stick at ``boot/grub``.

All done! Reboot, configure USB (set in BIOS) as boot device, save changes, reboot again, and GRUB will display the menu of Linux distro images. Remove the USB multi-boot device, reboot, and return to using your USB device as removable storage.

5. GRUBS Reanimated USB Boot Stick
----------------------------------

I created the `GRUBS shell script <https://github.com/vonbrownie/grubs>`_ that creates multi-boot Linux USB sticks using the above steps and placed it on GitHub.

Happy hacking!
