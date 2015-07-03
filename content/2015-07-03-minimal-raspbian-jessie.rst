=======================
Minimal Raspbian Jessie
=======================

:date: 2015-07-03 19:27:00
:slug: minimal-raspbian-jessie
:tags: raspbian, debian, linux, raspberry pi, networks

Setup a minimal `Raspbian <http://www.circuidipity.com/tag-raspbian.html>`_ configuration on the `Raspberry Pi <http://www.circuidipity.com/tag-raspberry-pi.html>`_ using `raspbian-ua-netinst <https://github.com/debian-pi/raspbian-ua-netinst>`_ (ideal start for a `home server <http://www.circuidipity.com/raspberry-pi-home-server.html>`_) with the latest packages from `Debian <http://www.circuidipity.com/tag-debian.html>`_ ``jessie/stable``. 

Let's go!
=========

The netinstaller runs unattended (no display/keyboard required) with the pre-configured option of installing rootfs to external USB storage. Upon completion the Pi reboots with DHCP and OpenSSH for remote access.

I put my plan in motion using:

* Raspberry Pi 2 Model B
* 5V 2A microUSB power adapter
* 8GB microSD card                                                                  
* ethernet cable
* raspbian-ua-netinst

0. Prepare the microSD
======================

MicroSD card is prepared on a host running Debian. `Download <https://github.com/debian-pi/raspbian-ua-netinst/releases/>`_ the latest ``raspbian-ua-netinst-vX.X.X.img.xz`` and flash the image to the card:

.. code-block:: bash

    # xzcat /path/to/raspbian-ua-netinst-<latest-version-number>.img.xz > /dev/sdX && sync

1. Customize the install (optional)
===================================

`Default settings <https://github.com/debian-pi/raspbian-ua-netinst#installer-customization>`_ for the netinstaller can be customized by creating ``installer-config.txt`` in the root directory of the newly-prepared microSD. Remove newly-formatted card, re-insert, mount ``sdX1``, add the config.

Add only the settings to be changed from their defaults (example):

.. code-block:: bash

    packages=vim,tmux
    hostname=MyHostname
    bootsize=+256M

A second ``post-install.txt`` shell script can also be created alongside ``installer-config.txt`` that will run after installation is complete but before the Pi reboots.

2. Install and configure
========================

Insert microSD in the Pi and power up. Netinstaller typically runs under 15 minutes [1]_ to setup a base configuration before rebooting the Pi.

SSH into the newly-configured Pi (default ``login: root`` + ``password: raspbian``). Details of the install are logged in ``/var/log/raspbian-ua-netinst.log``.

Configure [2]_:

* a new root password: ``passwd``
* default locale: ``dpkg-reconfigure locales``
* timezone: ``dpkg-reconfigure tzdata``
* create 1GB swap file: ``dd if=/dev/zero of=/swap bs=1M count=1024 && mkswap /swap``
* enable swap file at boot: ``echo "/swap none swap sw 0 0" >> /etc/fstab``
* enable hardware random number generator: ``apt-get -y install rng-tools && echo "bcm2708-rng" >> /etc/modules``
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

Happy hacking!

Notes
=====

.. [1] First attempt (unattended upgrade straight to ``jessie``) took 236min! Second attempt (no custom config) took 112min.

I poked around to see if there was something wonky with the microSD... first using ``badlocks`` (read-only test):

.. code-block:: bash

    # badblocks -vs /dev/sdb                                                   
    [...]                                                                           
    79434                                                                           
    79435                                                                           
    79436                                                                           
    79437                                                                           
    done                                                                            
    Pass completed, 6424 bad blocks found. (6424/0/0 errors)                        
                                                                                  
Second test was creating/writing an image to the card (see `"Testing a new SD card under Linux" <http://projects.nuschkys.net/2012/05/15/testing-a-new-sd-card-under-linux/>`_) but it bombed right away:

.. code-block:: bash

    # dd if=/dev/urandom of=test_sd.tmp bs=1024 count=8000000                       
    8000000+0 records in                                                            
    8000000+0 records out                                                           
    8192000000 bytes (8.2 GB) copied, 597.98 s, 13.7 MB/s                           
    # dd if=test_sd.tmp of=/dev/sdb bs=1024 count=8000000                      
    dd: error writing ‘/dev/sdb’: Input/output error                                
    73017+0 records in                                                              
    73016+0 records out                                                             
    74768384 bytes (75 MB) copied, 44.9678 s, 1.7 MB/s

Conclusion: *definitely* wonky. :-) Replace with a good microSD and install took 12min.

.. [2] I created a `post-install script <https://github.com/vonbrownie/linux-post-install/blob/master/scripts/raspbian-post-install.sh>`_ for configuring the base install and upgrading to ``jessie``.
