===============================
Debian Jessie on Raspberry Pi 2
===============================

:date: 2015-07-22 13:48:00
:slug: debian-jessie-raspberry-pi-2
:tags: debian, linux, raspberry pi
:modified: 2015-07-25 17:48:00

With the move to ARMv7 I am now capable of running the official ARM port of Debian (with Pi-friendly kernel+firmware) on my Raspberry Pi 2! 

Let's go!
=========

Debian developer Sjoerd Simons has created a `Jessie minimal image <http://sjoerd.luon.net/posts/2015/02/debian-jessie-on-rpi2/>`_ with an updated 3.18 Linux kernel and firmware suitable for Pi 2.

My setup:

* Raspberry Pi 2 Model B
* 5V 2A microUSB power adapter
* ethernet cable
* HDMI display + USB keyboard
* Debian ``jessie-rpi2-20150705``
* 32GB microSD card

0. Download
===========

Download the latest `image and GPG signature <https://images.collabora.co.uk/rpi2/>`_:

.. code-block:: bash

    $ wget https://images.collabora.co.uk/rpi2/jessie-rpi2-20150705.img.gz
    $ wget https://images.collabora.co.uk/rpi2/jessie-rpi2-20150705.img.bmap
    $ wget https://images.collabora.co.uk/rpi2/jessie-rpi2-20150705.img.gz.asc

`Verify the GPG signature <http://www.circuidipity.com/verify-pgp-signature-gnupg.html>`_.

1. Install to microSD
=====================

Unpack the image:

.. code-block:: bash

    $ gzip -d jessie-rpi2-20150202.img.gz

In lieu of the usual (slower) ``dd`` I use ``bmap-tools`` and ``jessie-rpi2-*.img.bmap`` to write the image to microSD:

.. code-block:: bash

    $ sudo apt-get install bmap-tools                                                    
    $ sudo bmaptool copy --bmap jessie-rpi2-20150705.img.bmap jessie-rpi2-20150705.img /dev/sdX

2. Boot and resize
==================

Login as ``root`` with password ``debian``.

Filesystem layout [1]_ on the microSD card:

.. code-block:: bash

    Filesystem      Size  Used Avail Use% Mounted on
    /dev/root       2.8G  555M  2.1G  21% /
    devtmpfs        459M     0  459M   0% /dev
    tmpfs           463M     0  463M   0% /dev/shm
    tmpfs           463M  312K  463M   1% /run
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           463M     0  463M   0% /sys/fs/cgroup
    /dev/mmcblk0p1  121M  9.7M  112M   9% /boot/firmware 

Install image inflates into a 2.8GB partition; using only a fraction of available capacity. I use ``fdisk`` to repartition the microSD to use all storage and ``resize2fs`` to `expand rootfs into its new accomodations <http://www.circuidipity.com/resize-rootfs-raspberry-pi.html>`_!

Alternative: `Run a Raspberry Pi from USB storage <http://www.circuidipity.com/raspberry-pi-usb-storage-v4.html>`_

3. Post-install
===============

Configure:

* a new root password: ``passwd``
* default locale: ``dpkg-reconfigure locales``
* timezone: ``dpkg-reconfigure tzdata``
* create 1GB swap file: ``dd if=/dev/zero of=/swap bs=1M count=1024 && mkswap /swap``
* enable swap file at boot: ``echo "/swap none swap sw 0 0" >> /etc/fstab``
* setup hardware random number generator: ``apt-get -y install rng-tools && echo "bcm2708-rng" >> /etc/modules``
* add new user: ``adduser USERNAME``
* hostname: modify ``/etc/hostname`` and ``/etc/hosts`` and reboot

4. Package management
=====================

Modify ``/etc/apt/sources.list``:

.. code-block:: bash

    deb http://httpredir.debian.org/debian jessie main contrib non-free
    #deb-src http://httpredir.debian.org/debian/ jessie main contrib non-free

    deb http://security.debian.org/ jessie/updates main contrib non-free
    #deb-src http://security.debian.org/ jessie/updates main contrib non-free

    deb http://httpredir.debian.org/debian/ jessie-updates main contrib non-free
    #deb-src http://httpredir.debian.org/debian/ jessie-updates main contrib non-free

    deb [trusted=yes] https://repositories.collabora.co.uk/debian/ jessie rpi2

Install image provides a ``flash-kernel`` package customized for the Pi. Use **apt-pinning** to `continue using this custom package <http://sjoerd.luon.net/posts/2015/02/debian-jessie-on-rpi2/#comment-64b33335e8d852179704fb5dc218aa1e>`_ vs updates from official Debian repositories. Create ``/etc/apt/preferences.d/flash-kernel`` with:

.. code-block:: bash

    Package: flash-kernel
    Pin: origin repositories.collabora.co.uk
    Pin-Priority: 900

Confirm ``flash-kernel`` is pinned:

.. code-block:: bash

    # apt-cache policy flash-kernel
    flash-kernel:
      Installed: 3.35.co1+b1
      Candidate: 3.35.co1+b1
      Package pin: 3.35.co1+b1
      Version table:
     *** 3.35.co1+b1 900
            500 https://repositories.collabora.co.uk/debian/ jessie/rpi2 armhf Packages
            100 /var/lib/dpkg/status
         3.35 900
            500 http://httpredir.debian.org/debian/ jessie/main armhf Packages

Now is a good time to upgrade:

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get dist-upgrade

5. Remote access
================

Generate new SSH keys on the Pi:

.. code-block:: bash

    # rm /etc/ssh/ssh_host_*key* && dpkg-reconfigure openssh-server

Secure remote access by `requiring clients to use SSH keys <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_.

Happy hacking!

Notes
-----

.. [1] ``/boot/config.txt`` has been moved to ``/boot/firmware/config.txt``.
