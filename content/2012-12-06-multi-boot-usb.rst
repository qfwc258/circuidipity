=======================================================================
Transform a USB stick into a boot device packing multiple Linux distros
=======================================================================

:date: 2012-12-06 01:23:00
:tags: grub, shell, systemrescuecd, debian, lubuntu, ubuntu, linux
:slug: multi-boot-usb
:template: article-project
:modified: 2017-05-26 12:32:00

.. image:: images/grubs-300.png
    :align: right
    :alt: GRUBS
    :width: 300px
    :height: 363px

Transform removable USB storage into a dual-purpose device that is both a storage medium usable under Linux, Windows, and Mac OS and a GRUB boot device capable of loopback mounting Linux distro ISO files. [1]_

Depends: ``grub2``, ``bash``, ``sudo``, ``rsync``

Let's go!
=========

.. role:: warning

:warning:`WARNING!` In this HOWTO the USB device is identified as **sdx** and contains a single partition **sdx1**. Make careful note of the drive and partition labels on your system. The following steps will **destroy all data** currently stored on the device.

0. Format
---------

Create a ``FAT32`` partition on the **unmounted** USB device ...

.. code-block:: bash

    $ sudo mkfs.vfat -n MULTIBOOT /dev/sdx1

1. Boot and iso
---------------

Mount the USB device to MOUNTPOINT and create a ``boot`` folder for GRUB files and a ``iso`` folder to hold Linux distro images ...

.. code-block:: bash

    $ mkdir -p /media/MOUNTPOINT/boot/{grub,iso,debian}

2. GRUB
-------

Install GRUB to the **Master Boot Record (MBR)** of the USB device at MOUNTPOINT ...

.. code-block:: bash

    $ sudo grub-install --target=i386-pc --force --recheck --boot-directory=/media/MOUNTPOINT/boot /dev/sdx

3. Linux images
---------------

Download Linux distro image (ISO) files and place in the newly-created ``boot/iso`` folder on the USB device. I have installed ...

* **SystemRescueCd** - `Collection of Linux repair tools <http://www.system-rescue-cd.org/>`_
* **Debian Jessie Netinst+firmware** - `64bit <https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/8.7.1+nonfree/amd64/iso-cd/>`_ and `32bit <https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/8.7.1+nonfree/i386/iso-cd/>`_ installers
* **Lubuntu 16.04 Live Mode + Desktop Installer** - `64bit and 32bit <http://cdimage.ubuntu.com/lubuntu/releases/16.04.2/release/>`_ desktop images allow trying Lubuntu before installing
* **Ubuntu 16.04 LTS Mini-Installers** - `64bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/netboot/>`_ and `32bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-i386/current/images/netboot/>`_

3.1 Debian Netinst
++++++++++++++++++

Problem: This was a bit tricky to get working. Selecting ``firmware-8.7.1-ARCH-netinst.iso`` from the GRUB menu would get things started but the install would fail at the stage where the ISO needs to be located and mounted. Debian's netinst images do not include the **iso-scan** package , which is required for searching and loading ISO images.

Fix: Bypass the ``initrd.gz`` that is on the ISO images and use ones that *do* contain the iso-scan package, [2]_ which I retrieved from the **hd-media** installers ...

.. code-block:: bash

    $ mkdir /media/MOUNTPOINT/boot/debian/install.{amd,386}
    $ cd /media/MOUNTPOINT/boot/debian/install.amd
    $ wget http://ftp.debian.org/debian/dists/jessie/main/installer-amd64/current/images/hd-media/initrd.gz
    $ cd .. /install.386
    $ wget http://ftp.debian.org/debian/dists/jessie/main/installer-i386/current/images/hd-media/initrd.gz

4. GRUB configuration
---------------------

Create ``boot/grub/grub.cfg`` and write entries for the ISO files to be copied to the USB device. Note that each Linux distro is a bit different in the manner its booted by GRUB. This can require a bit of research. Example ... 

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
    
    menuentry "Lubuntu 16.04 - 64bit Live Mode + Desktop Installer" {
        set iso="/boot/iso/lubuntu-16.04.2-desktop-amd64.iso"
        loopback loop $iso
        linux (loop)/casper/vmlinuz.efi boot=casper iso-scan/filename=$iso noprompt noeject
        initrd (loop)/casper/initrd.lz
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

All done! Reboot. Configure the BIOS to accept removable USB storage as boot device. Reboot and GRUB displays a menu of the Linux distros installed on the USB device. Launch and enjoy!

When finished, simply reboot and return to using the USB device as a VFAT-formatted storage medium.

5. GRUBS Reanimated USB Boot Stick
----------------------------------

I created the `GRUBS shell script that prepares USB storage devices <https://github.com/vonbrownie/grubs>`_ using the above steps and uploaded it to GitHub.

Happy hacking!

Notes
+++++

.. [1] Image credit: Flickr user Peter via Creative Commons, retrieved from `InsideClimate News <https://insideclimatenews.org/species/birds/ad%C3%A9lie-penguin>`_.

.. [2] Helpful in figuring out the iso-scan package wrinkle: `Multi-boot stick update <http://126kr.com/article/6xzqwchvlv6>`_
