=============================================================
Run a Raspberry Pi 2 from external USB storage using Raspbian
=============================================================

:date: 2015-07-05 15:53:00
:slug: run-a-raspberry-pi-2-from-external-usb-storage-using-raspbian
:tags: raspberry pi, raspbian, debian, linux, network

`Raspberry Pi Home Server Hack #0 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ I am exploring the use of my Pi as **24/7 uptime home server** and one of the hacks I wish to add is using Pi as a cheap and cheerful `network attached storage (NAS) <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_ device. Hmmm... How about using that USB hard drive I connect for NAS and move over the Pi rootfs and run it from there as well?

Let's go!
=========

I imagine a 24/7 uptime Pi enjoys more storage and robust performance operating from hard drive storage vs a microSD card. [1]_ I put my plan in motion using:

* Raspberry Pi 2 Model B
* 5V 2A microUSB power adapter
* 8GB microSD card (for initial setup and ``boot`` partition) [2]_
* 1TB powered USB hard drive
* ethernet cable
* `raspbian-ua-netinst <https://github.com/debian-pi/raspbian-ua-netinst>`_ [3]_

Setup a minimal `Raspbian <http://www.circuidipity.com/tag-raspbian.html>`_ configuration using the latest packages drawn from `Debian <http://www.circuidipity.com/tag-debian.html>`_ ``jessie/stable``  with ``raspbian-ua-netinst``. The netinstaller runs unattended (no display/keyboard required) with the option of installing rootfs to external USB storage. Upon completion the Pi reboots with DHCP and OpenSSH for remote access.

0. Prepare the microSD
======================

MicroSD card is prepared on a host running Debian. `Download <https://github.com/debian-pi/raspbian-ua-netinst/releases/>`_ the latest ``raspbian-ua-netinst-vX.X.X.img.xz`` and flash image to the card (example ``sdX``):

.. code-block:: bash

    # apt-get install xz-utils
    # xzcat /path/to/raspbian-ua-netinst-<latest-version-number>.img.xz > /dev/sdX && sync

1. Customize the install
========================

`Default settings <https://github.com/debian-pi/raspbian-ua-netinst#installer-customization>`_ for the netinstaller are customized by creating ``installer-config.txt`` in the root directory of the newly-prepared microSD. Remove card, re-insert, mount ``sdX1``, add the config.

.. role:: warning

:warning:`WARNING!` Netinstaller reformats drive and installs rootfs to ``sda1``. Omit if you want a single partition that fills the entire drive (vs separate ``home`` partition I create later on). Either way... **all data will be wiped from the drive**. Make any backups you need to make.

Add only the settings to be changed from their defaults. Example that creates a 256MB ``boot`` on the microSD and 24GB ``root`` on the USB:

.. code-block:: bash

    packages=vim,tmux
    hostname=MyHostname
    bootsize=+256M
    rootsize=+24000M
    usbroot=1

A second ``post-install.txt`` shell script can also be created alongside ``installer-config.txt`` that will run after installation is complete but before the Pi reboots.

2. Install and configure
========================

I connect the 1TB hard drive to Pi, insert microSD, and power up. Netinstaller typically runs under 15 minutes to setup a base configuration before rebooting the Pi.

SSH into the newly-configured Pi (default ``login: root`` + ``password: raspbian``). Details of the install are logged in ``/var/log/raspbian-ua-netinst.log``.

Configure: [4]_

* a new root password: ``passwd``
* default locale: ``dpkg-reconfigure locales``
* timezone: ``dpkg-reconfigure tzdata``
* create 1GB swap file: ``dd if=/dev/zero of=/swap bs=1M count=1024 && mkswap /swap``
* enable swap file at boot: ``echo "/swap none swap sw 0 0" >> /etc/fstab``
* hardware random number generator: ``apt-get -y install rng-tools && echo "bcm2708-rng" >> /etc/modules``
* add new user: ``adduser USERNAME``

3. Upgrade
==========

Stable release of Raspbian (2015-07-03) is currently built on older Debian ``wheezy`` packages. Upgrade to the ``jessie/stable`` branch by first modifying ``/etc/apt/sources.list``:

.. code-block:: bash

    # cp /etc/apt/sources.list /etc/apt/sources.list.bak
    # echo "deb http://mirrordirector.raspbian.org/raspbian jessie main contrib non-free firmware rpi" > /etc/apt/sources.list
    # echo "deb http://archive.raspbian.org/raspbian jessie main" >> /etc/apt/sources.list

Update the package lists and upgrade:

.. code-block:: bash

    # apt-get update && apt-get -y dist-upgrade && apt-get -y autoremove

Reboot.

4. Partition external USB drive
===============================

Device is ``sda``. Use **fdisk** to create a new partition for ``home`` on the USB:

* sda1 - 24GB - ``root`` - created by ``raspbian-ua-netinst`` using ``installer-config.txt``
* sda2 - remaining space - ``home``

.. code-block:: bash
                                                                                
    # fdisk /dev/sda                                                                
                                                                                
    Welcome to fdisk (util-linux 2.25.2).                                           
    Changes will remain in memory only, until you decide to write them.             
    Be careful before using the write command.                                      
                                                                                
                                                                                
    Command (m for help): p                                                         
    Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors               
    Units: sectors of 1 * 512 = 512 bytes                                           
    Sector size (logical/physical): 512 bytes / 512 bytes                           
    I/O size (minimum/optimal): 512 bytes / 512 bytes                               
    Disklabel type: dos                                                             
    Disk identifier: 0x00000000                                                     
                                                                                
    Device     Boot Start      End  Sectors  Size Id Type                           
    /dev/sda1          63 46893734 46893672 22.4G 83 Linux                          
                                                                                
                                                                                
    Command (m for help): n                                                         
    Partition type                                                                  
        p   primary (1 primary, 0 extended, 3 free)                                  
        e   extended (container for logical partitions)                              
    Select (default p): p                                                           
    Partition number (2-4, default 2):                                              
    First sector (46893735-1953525167, default 46895104):                           
    Last sector, +sectors or +size{K,M,G,T,P} (46895104-1953525167, default 1953525167):
                                                                                
    Created a new partition 2 of type 'Linux' and of size 909.2 GiB.                
                                                                                
    Command (m for help): p                                                         
    Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors               
    Units: sectors of 1 * 512 = 512 bytes                                           
    Sector size (logical/physical): 512 bytes / 512 bytes                           
    I/O size (minimum/optimal): 512 bytes / 512 bytes                               
    Disklabel type: dos                                                             
    Disk identifier: 0x00000000                                                     
                                                                                
    Device     Boot    Start        End    Sectors   Size Id Type                   
    /dev/sda1             63   46893734   46893672  22.4G 83 Linux                  
    /dev/sda2       46895104 1953525167 1906630064 909.2G 83 Linux                  
                                                                                
                                                                                
    Command (m for help): w                                                         
    The partition table has been altered.                                           
    Calling ioctl() to re-read partition table.                                     
    Re-reading the partition table failed.: Device or resource busy                 
                                                                                
    The kernel still uses the old table. The new table will be used at the next reboot or after you run partprobe(8) or kpartx(8).
                                                                                
Reboot.

5. Move home
============

Format new partition using ``ext4`` filesystem:

.. code-block:: bash

    # mkfs.ext4 -E lazy_itable_init=0,lazy_journal_init=0 /dev/sda2                 
                                                                                
Mount partition and move over any contents in ``/home``:

.. code-block:: bash
                                              
    # mount -t ext4 /dev/sda2 /mnt && mv /home/* /mnt/ && sync && umount /mnt       
                                                                                
Configure ``fstab`` and mount new location of ``home``:

.. code-block:: bash                                 

    # echo "/dev/sda2 /home ext4 noatime 0 2" >> /etc/fstab && mount /home

6. Static address
=================

A Raspberry Pi that is going to stay home and run as a server can be configured to use a **static network address**. Sample ``/etc/network/interfaces`` modification that disables ``dhcp`` and sets ip address ``192.168.1.88`` and connects to a router (that handles DNS) at ``192.168.1.1``:

.. code-block:: bash

    #iface eth0 inet dhcp                                                       
    auto eth0                                                                   
    iface eth0 inet static                                                      
        address 192.168.1.88                                                    
        netmask 255.255.255.0                                                   
        gateway 192.168.1.1
        dns-nameservers 192.168.1.1

7. OpenSSH
==========

Secure access to remote servers `using SSH keys <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_.

Happy hacking!

Notes
-----

.. [1] `Discussion thread <http://www.raspberrypi.org/forums/viewtopic.php?f=29&t=44177>`_ about moving root to external USB storage.
.. [2] Pi 2 requires microSD card at boot so we continue using original ``/boot``.
.. [3] `Version 1 <http://www.circuidipity.com/run-a-raspberry-pi-from-external-usb-storage.html>`_ of HOWTO used Raspbian on a Raspberry Pi Model B. With the Pi 2 moving to ARMv7 I used a `minimal Ubuntu 14.04 <http://www.circuidipity.com/run-a-raspberry-pi-2-from-external-usb-storage.html>`_ installer for Version 2.
.. [4] I created a `post-install script <https://github.com/vonbrownie/linux-post-install/blob/master/scripts/raspbian-post-install.sh>`_ for configuring the base install and upgrading to ``jessie``.
