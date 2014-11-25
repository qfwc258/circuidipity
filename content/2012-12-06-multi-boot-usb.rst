=======================================================================
Transform a USB stick into a boot device packing multiple Linux distros
=======================================================================

:date: 2012-12-06 01:23:00
:tags: gparted, ubuntu, dban, debian, linux, shell
:slug: multi-boot-usb
:modified: 2014-11-25 00:43:00

In 5 easy steps I transform a standard USB stick into a dual-purpose device that is both a storage medium usable under Linux, Windows, and Mac OS and a GRUB boot device packing multiple Linux distros.

.. role:: warning

:warning:`WARNING!` In this HOWTO the USB stick is identified as **sdX** and contains a single partition **sdX1**. Make careful note of the drive and partition labels on your system. The following steps will **destroy all data** currently stored on the device.

To boot Linux distro images using GRUB:
=======================================

0. Select device and create filesystem
--------------------------------------

Create a ``FAT32`` partition on the unmounted USB stick:

.. code-block:: bash

    $ sudo mkfs.vfat -n multiboot /dev/sdX1

1. Create boot and iso folders
------------------------------

The new ``FAT32`` partition is mounted and I create a ``boot`` folder for GRUB and a ``iso`` folder to hold my Linux distro images:

.. code-block:: bash

    $ cd MOUNTPOINT
    $ mkdir boot iso

2. Install GRUB
---------------

Install GRUB to the **Master Boot Record (MBR)** of the USB stick:

.. code-block:: bash

    $ sudo grub-install --force --no-floppy --boot-directory=MOUNTPOINT/boot /dev/sdX

3. Copy Linux images
--------------------

Download and copy Linux ISO images to the newly-created ``iso`` folder on the USB stick. For example I have installed on my own USB stick:

* **GParted Live CD** - `Graphical partition editor <http://gparted.sourceforge.net/livecd.php>`_ for hard drives
* **Darik's Boot and Nuke (DBAN)** - `Secure deletion tool <http://www.dban.org/>`_ to wipe hard disks clean [1]_
* **Debian Wheezy Mini-Installers** - Minimal (~25MB) `64bit <http://ftp.us.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/>`_ and `32bit <http://ftp.us.debian.org/debian/dists/stable/main/installer-i386/current/images/netboot/>`_ ``mini.iso`` installers
* **Ubuntu 14.04 LTS Mini-Installers** - `64bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/trusty/main/installer-amd64/current/images/netboot/>`_ and `32bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/trusty/main/installer-i386/current/images/netboot/>`_
* **Memtest86+** - Diagnostic tool for `testing RAM <http://www.memtest.org/>`_

4. Create grub.cfg
------------------

Create a ``grub.cfg`` with entries for the Linux images copied to the USB stick. Each distro is a little bit different in the manner its booted by GRUB. Using my own example above I have created:

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
    menuentry "GParted Live - Partition Editor" {
        set iso="/iso/gparted-live-0.20.0-2-i486.iso"
        loopback loop $iso
        linux (loop)/live/vmlinuz boot=live config union=aufs noswap noprompt ip=frommedia toram=filesystem.squashfs findiso=$iso
        initrd (loop)/live/initrd.img
    }

    menuentry "Darik's Boot and Nuke - Hard Disk Wipe" {
        set iso="/iso/dban-2.2.8_i586.iso"
        loopback loop $iso
        linux (loop)/DBAN.BZI nuke="dwipe"
    }

    menuentry "Debian Wheezy - 64bit Mini-Installer" {
        set iso="/iso/debian-wheezy-amd64-mini.iso"
        loopback loop $iso
        linux (loop)/linux
        initrd (loop)/initrd.gz
    }

    menuentry "Debian Wheezy - 32bit Mini-Installer" {
        set iso="/iso/debian-wheezy-i386-mini.iso"
        loopback loop $iso
        linux (loop)/linux
        initrd (loop)/initrd.gz
    }

    menuentry "Ubuntu 14.04 LTS - 64bit Mini-Installer" {
        set iso="/iso/ubuntu-14.04-amd64-mini.iso"
        loopback loop $iso
        linux (loop)/linux boot=casper iso-scan/filename=$iso noprompt noeject
        initrd (loop)/initrd.gz
    }

    menuentry "Ubuntu 14.04 LTS - 32bit Mini-Installer" {
        set iso="/iso/ubuntu-14.04-i386-mini.iso"
        loopback loop $iso
        linux (loop)/linux boot=casper iso-scan/filename=$iso noprompt noeject
        initrd (loop)/initrd.gz
    }

    menuentry "Ubuntu 14.04 LTS - 32bit Installer ('forcepae' for Pentium M)" {
        set iso="/iso/ubuntu-14.04-i386-mini.iso"
        loopback loop $iso
        linux (loop)/linux boot=casper iso-scan/filename=$iso noprompt noeject forcepae
        initrd (loop)/initrd.gz
    }

    menuentry "Memtest86+ - RAM Tester" {
        linux16 /boot/memtest86+-4.20.bin
    }

Save ``grub.cfg`` to the USB stick at ``MOUNTPOINT/boot/grub``.

All done! Reboot, select the USB stick (depending on BIOS settings) as boot device and GRUB will display a menu of the installed Linux distro images. Reboot again and return to using your USB stick as a regular storage device.

GRUBS Reanimated USB Boot Stick
-------------------------------

I made a Bash script called `GRUBS <https://github.com/vonbrownie/grubs>`_ that creates multi-boot Linux USB sticks using the above steps and placed it on `GitHub <https://github.com/vonbrownie/grubs>`_.

Happy hacking!

Notes
-----

.. [1] When using DBAN remove the USB stick immediately when the boot messages begin to scroll past... otherwise it will scan for USB drives and later fail when selecting a hard drive to wipe.
