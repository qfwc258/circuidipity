========================================
Run a Raspberry Pi from USB storage v4.0
========================================

:date: 2015-07-25 18:25:00
:slug: raspberry-pi-usb-storage-v4
:tags: raspberry pi, network, debian, linux

`PROJECT: Home Server #0 .: <http://www.circuidipity.com/home-server.html>`_ I am exploring the use of my Pi as **24/7 uptime home server**. Hard drives offer a more robust storage media than a Pi's default choice of microSD cards and that is what I decide to use. [1]_ I put my plan in motion using **Debian** and move ``rootfs`` from a microSD to a powered 1TB USB 3.5" hard drive with encrypted storage. 

Let's go!
=========

Current setup:

* Raspberry Pi 2 Model B
* 5V 2A microUSB power adapter
* ethernet cable
* HDMI display + USB keyboard (initial setup)
* USB hard drive with 3 partitions: ``root``, encrypted ``swap`` + ``storage``
* Debian ``jessie-rpi2-20150705``
* 4GB microSD card (initial setup and ``boot`` partition)

Previous versions:

* v3.0 - `Pi 2 Model B + Raspbian <http://www.circuidipity.com/run-a-raspberry-pi-2-from-external-usb-storage-using-raspbian.html>`_
* v2.0 - `Pi 2 Model B + Ubuntu <http://www.circuidipity.com/run-a-raspberry-pi-2-from-external-usb-storage.html>`_
* v1.0 - `Pi Model B + Raspbian <http://www.circuidipity.com/run-a-raspberry-pi-from-external-usb-storage.html>`_

0. Debian
---------

With the move to ARMv7 the Pi 2 is now capable of running the official Debian **armhf** port. Debian developer Sjoerd Simons has created a `Jessie minimal image <http://sjoerd.luon.net/posts/2015/02/debian-jessie-on-rpi2/>`_ with an updated 3.18 Linux kernel and firmware suitable for Pi 2.

Start here: `Install and configure Jessie on a microSD <http://www.circuidipity.com/debian-jessie-raspberry-pi-2.html>`_

1. Partition
------------

I connect the USB drive to Pi and confirm detection ...

.. code-block:: bash

    # lsblk
    NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sda           8:0    0 931.5G  0 disk 
    └─sda1        8:1    0 931.5G  0 part 
    mmcblk0     179:0    0   7.6G  0 disk 
    ├─mmcblk0p1 179:1    0   121M  0 part /boot/firmware
    └─mmcblk0p2 179:2    0   2.9G  0 part / 
   
Device is ``sda`` with a single ``sda1`` partition. Use ``fdisk`` to create 3 new partitions on the USB drive:

* sda1 - 20GB - future ``root``
* sda2 - 2GB - future encrypted ``swap``
* sda3 - remaining space - future encrypted ``storage``

Sample walk-through ...

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

    Device     Boot Start        End    Sectors   Size Id Type
    /dev/sda1        2048 1953525167 1953523120 931.5G 83 Linux


    Command (m for help): d
    Selected partition 1
    Partition 1 has been deleted.

    Command (m for help): n
    Partition type
        p   primary (0 primary, 0 extended, 4 free)
        e   extended (container for logical partitions)
    Select (default p): p
    Partition number (1-4, default 1): 
    First sector (2048-1953525167, default 2048): 
    Last sector, +sectors or +size{K,M,G,T,P} (2048-1953525167, default 1953525167): +20G

    Created a new partition 1 of type 'Linux' and of size 20 GiB.

    Command (m for help): n
    Partition type
        p   primary (1 primary, 0 extended, 3 free)
        e   extended (container for logical partitions)
    Select (default p): p
    Partition number (2-4, default 2): 
    First sector (41945088-1953525167, default 41945088): 
    Last sector, +sectors or +size{K,M,G,T,P} (41945088-1953525167, default 1953525167): +1G

    Created a new partition 2 of type 'Linux' and of size 1 GiB.

    Command (m for help): n
    Partition type
        p   primary (2 primary, 0 extended, 2 free)
        e   extended (container for logical partitions)
    Select (default p): p
    Partition number (3,4, default 3): 
    First sector (44042240-1953525167, default 44042240): 
    Last sector, +sectors or +size{K,M,G,T,P} (44042240-1953525167, default 1953525167): 

    Created a new partition 3 of type 'Linux' and of size 910.5 GiB.

    Command (m for help): p
    Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x00000000

    Device     Boot    Start        End    Sectors   Size Id Type
    /dev/sda1           2048   41945087   41943040    20G 83 Linux
    /dev/sda2       41945088   44042239    2097152     1G 83 Linux
    /dev/sda3       44042240 1953525167 1909482928 910.5G 83 Linux


    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.

    #

2. Root
-------

Format the future ``rootfs`` partition using filesystem ``ext4`` and mount ...

.. code-block:: bash

    # mke2fs -t ext4 -L rootfs /dev/sda1
    # mount -t ext4 /dev/sda1 /mnt

Modify options in ``/boot/firmware/cmdline.txt`` to point the bootloader to ``root`` filesystem on the USB device ...

.. code-block:: bash

    Original:                                                                      
    dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootwait net.ifnames=1
 
    Modified:
    dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1 root=/dev/sda1 rootwait rootdelay=5

Comment out ``mmcblk0p2`` and point to the new ``root`` partition in ``/etc/fstab`` ...

.. code-block:: bash

    #/dev/mmcblk0p2  / ext4 relatime,errors=remount-ro,discard 0 1
    /dev/sda1 / ext4 relatime,errors=remount-ro 0 1
    /dev/mmcblk0p1 /boot/firmware vfat defaults 0 2

Use ``rsync`` to duplicate contents of ``root`` on the microSD [2]_ to the ``rootfs`` partition on the USB hard drive ...

.. code-block:: bash

    # apt-get -y install rsync
    # rsync --exclude=firmware/* -axv / /mnt

3. LUKS encryption
------------------

Root is unencrypted to allow **unattended boots** of the server (otherwise the Pi would hang waiting for a passphrase that never arrives). A LUKS-encrypted ``swap`` is added with a **randomly-generated key** and post-boot I log in and mount a LUKS-encrypted ``storage`` partition using a passphrase.

3.1 Storage
+++++++++++

Encrypt the partition, assign a passphrase, and format using filesystem ``ext4`` ...

.. code-block:: bash

    # apt-get -y install cryptsetup
    # cryptsetup luksFormat /dev/sda3
    # cryptsetup luksOpen /dev/sda3 sda3_crypt
    # mkfs.ext4 -L storage /dev/mapper/sda3_crypt

Create a mountpoint and mount the partition ...

.. code-block:: bash

    # mkdir /media/sda3_crypt && mount -t ext4 /dev/mapper/sda3_crypt /media/sda3_crypt/

Unmounting ...

.. code-block:: bash

    # umount /media/sda3_crypt && cryptsetup luksClose /dev/mapper/sda3_crypt

3.2 Swap
++++++++

Configure the secure wiping of the swap partition, auto-generation of a new random key, and swap activation at boot ...

.. code-block:: bash

    # echo "sda2_crypt /dev/sda2 /dev/urandom cipher=aes-xts-plain64,size=256,swap" >> /etc/crypttab
    # echo "/dev/mapper/sda2_crypt none swap sw 0 0" >> /etc/fstab

4. Reboot
---------

Aaaand reboot!

.. code-block:: bash

    # reboot
    
Log in and check the new filesystem layout ...

.. code-block:: bash

    $ df -h
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/root        20G  646M   18G   4% /
    devtmpfs        459M     0  459M   0% /dev
    tmpfs           463M     0  463M   0% /dev/shm
    tmpfs           463M  340K  463M   1% /run
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           463M     0  463M   0% /sys/fs/cgroup
    /dev/mmcblk0p1  121M  9.7M  112M   9% /boot/firmware

5. Static Address
-----------------

Assign a Pi home server a **static network address**. Sample ``/etc/network/interfaces`` that disables ``dhcp``, sets ip address ``192.168.1.88``, and connects to a router (managing DNS) at ``192.168.1.1`` ...

.. code-block:: bash

    auto eth0                                                                   
    iface eth0 inet static                                                      
        address 192.168.1.88                                                    
        netmask 255.255.255.0                                                   
        gateway 192.168.1.1
        dns-nameservers 192.168.1.1

Happy hacking!

Notes
+++++

.. [1] `Discussion thread (raspberrypi.org/forums) <http://www.raspberrypi.org/forums/viewtopic.php?f=29&t=44177>`_ about moving root to external USB storage.

.. [2] Raspberry Pi requires an SD card to boot and the bootloader expects certain config files to reside on a ``vfat`` formatted partition. This particular Debian ``jessie-rpi2-DATE.img`` installs the necessary files in ``mmcblk0p1`` and mounts this partition to ``/boot/firmware``. You can inspect the image partition layout, contents, and make modifications before installing to a microSD: `How can I mount a Raspberry Pi linux distro image? <https://raspberrypi.stackexchange.com/questions/13137/how-can-i-mount-a-raspberry-pi-linux-distro-image>`_
