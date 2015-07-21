=============================
Resize rootfs on Raspberry Pi
=============================

:date: 2015-07-21 17:19:00
:slug: resize-rootfs-raspberry-pi
:tags: debian, linux, raspberry pi

Resize a mounted partition to take full advantage of the storage capacity of a microSD card.

Let's go!
=========

Debian developer Sjoerd Simons has created a `Jessie minimal image <http://sjoerd.luon.net/posts/2015/02/debian-jessie-on-rpi2/>`_ with an updated 3.18 Linux kernel and firmware suitable for Pi 2. I install the image file to a 32GB microSD card, insert card into my Pi and reboot, log in and inspect the filesystem layout:

.. code-block:: bash

    Filesystem      Size  Used Avail Use% Mounted on
    /dev/root       2.8G  555M  2.1G  21% /
    devtmpfs        459M     0  459M   0% /dev
    tmpfs           463M     0  463M   0% /dev/shm
    tmpfs           463M  312K  463M   1% /run
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           463M     0  463M   0% /sys/fs/cgroup
    /dev/mmcblk0p1  121M  9.7M  112M   9% /boot/firmware 

Install image inflates into a 2.8GB partition; using only a fraction of available capacity. I will use ``fdisk`` to repartition the microSD to use all storage and ``resize2fs`` to expand ``rootfs`` into its new accomodations!

0. Repartition
==============

Repartitioning the mounted filesytem using ``fdisk`` on the Pi involves:

* delete the current ``mmcblk0p2`` partition containing ``rootfs``
* create a new partition **beginning at the same sector as the old partition** that uses all remaining space
* ``mmcblk0p1`` - containing ``/boot/firmware`` - remains untouched

.. role:: warning

:warning:`WARNING!` Ensure the start sector remains identical (example: mine below is ``249856`` on the old and new versions of ``mmcblk0p2`` or there is a high probability the operation will fail and all data lost.

A sample run-through on my own microSD:

.. code-block:: bash

    # fdisk /dev/mmcblk0

    Welcome to fdisk (util-linux 2.25.2).
    Changes will remain in memory only, until you decide to write them.
    Be careful before using the write command.


    Command (m for help): p
    Disk /dev/mmcblk0: 29.7 GiB, 31914983424 bytes, 62333952 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0xc96ffe28

    Device         Boot  Start     End Sectors  Size Id Type
    /dev/mmcblk0p1        2048  249855  247808  121M  e W95 FAT16 (LBA)
    /dev/mmcblk0p2      249856 6291455 6041600  2.9G 83 Linux


    Command (m for help): d
    Partition number (1,2, default 2): 

    Partition 2 has been deleted.

    Command (m for help): n
    Partition type
       p   primary (1 primary, 0 extended, 3 free)
       e   extended (container for logical partitions)
    Select (default p): 

    Using default response p.
    Partition number (2-4, default 2): 
    First sector (249856-62333951, default 249856): 249856
    Last sector, +sectors or +size{K,M,G,T,P} (249856-62333951, default 62333951): 

    Created a new partition 2 of type 'Linux' and of size 29.6 GiB.

    Command (m for help): p
    Disk /dev/mmcblk0: 29.7 GiB, 31914983424 bytes, 62333952 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0xc96ffe28

    Device         Boot  Start      End  Sectors  Size Id Type
    /dev/mmcblk0p1        2048   249855   247808  121M  e W95 FAT16 (LBA)
    /dev/mmcblk0p2      249856 62333951 62084096 29.6G 83 Linux


    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Re-reading the partition table failed.: Device or resource busy

    The kernel still uses the old table. The new table will be used at the next reboot or after you run partprobe(8) or kpartx(8).

... aaaand reboot!

1. Resize
=========

Expand ``rootfs`` to use the new capacity:

.. code-block:: bash

    # resize2fs /dev/mmcblk0p2
    resize2fs 1.42.12 (29-Aug-2014)
    Filesystem at /dev/mmcblk0p2 is mounted on /; on-line resizing required
    old_desc_blocks = 1, new_desc_blocks = 2
    The filesystem on /dev/mmcblk0p2 is now 7760512 (4k) blocks long.

    # df -h
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/root        30G  561M   28G   2% /
    devtmpfs        459M     0  459M   0% /dev
    tmpfs           463M     0  463M   0% /dev/shm
    tmpfs           463M  312K  463M   1% /run
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           463M     0  463M   0% /sys/fs/cgroup
    /dev/mmcblk0p1  121M  9.7M  112M   9% /boot/firmware
    #

Source: https://raspberrypi.stackexchange.com/questions/499/how-can-i-resize-my-root-partition

Happy hacking!
