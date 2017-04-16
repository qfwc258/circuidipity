=======================================================================
Transform a USB stick into a boot device packing multiple Linux distros
=======================================================================

:date: 2012-12-06 01:23:00
:tags: grub, shell, linux
:slug: multi-boot-usb
:modified: 2017-04-16 17:53:00

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

    $ mkdir /media/MOUNTPOINT/{boot,iso}

2. GRUB
-------

Install GRUB to the **Master Boot Record (MBR)** of the USB device at MOUNTPOINT ...

.. code-block:: bash

    $ sudo grub-install --force --no-floppy --root-directory=/media/MOUNTPOINT /dev/sdX

3. Linux images
---------------

Download and copy Linux ISO images to the newly-created ``iso`` folder on the USB device. I have installed ...

* **SystemRescueCd** - `Collection of Linux repair tools <http://www.system-rescue-cd.org/>`_
* **Darik's Boot and Nuke (DBAN)** - `Secure deletion tool <http://www.dban.org/>`_ to wipe hard disks clean [1]_
* **Debian Jessie Mini-Installers** - Minimal (~25MB) `64bit <http://ftp.us.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/>`_ and `32bit <http://ftp.us.debian.org/debian/dists/stable/main/installer-i386/current/images/netboot/>`_ ``mini.iso`` installers
* **Ubuntu 16.04 LTS Mini-Installers** - `64bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/netboot/>`_ and `32bit mini.iso <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-i386/current/images/netboot/>`_
* **Memtest86+** - Diagnostic tool for `testing RAM <http://www.memtest.org/>`_

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

    menuentry "Darik's Boot and Nuke - Hard Disk Wipe" {
        set iso="/iso/dban-i586.iso"
        loopback loop $iso
        linux (loop)/DBAN.BZI nuke="dwipe"
    }

    menuentry "Debian Jessie - 64bit Mini-Installer" {
        set iso="/iso/debian-jessie-amd64-mini.iso"
        loopback loop $iso
        linux (loop)/linux
        initrd (loop)/initrd.gz
    }

    menuentry "Debian Jessie - 32bit Mini-Installer" {
        set iso="/iso/debian-jessie-i386-mini.iso"
        loopback loop $iso
        linux (loop)/linux
        initrd (loop)/initrd.gz
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

    menuentry "Memtest86+ - RAM Tester" {
        linux16 /boot/memtest86+-4.20.bin
    }

Save ``grub.cfg`` to the USB stick at ``/media/MOUNTPOINT/boot/grub``.

All done! Reboot, configure USB (set in BIOS) as boot device, save changes, reboot again, and GRUB will display the menu of Linux distro images. Remove the USB multi-boot device, reboot, and return to using your USB device as removable storage.

5. GRUBS Reanimated USB Boot Stick
----------------------------------

I created the `GRUBS shell script <https://github.com/vonbrownie/grubs>`_ that creates multi-boot Linux USB sticks using the above steps and placed it on GitHub.

Happy hacking!

Notes
-----

.. [1] When using DBAN remove the USB stick immediately when the boot messages begin to scroll past... otherwise it will scan for USB drives and later fail when selecting a hard drive to wipe.
