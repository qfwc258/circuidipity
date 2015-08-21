========================================
Add encrypted USB storage to Chromebooks
========================================

:date: 2014-10-31 00:11:00
:slug: 20141031
:tags: luks, crypto, chromebook, debian, linux
:modified: 2015-08-21 16:14:00

I love my `Jessiebook <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_ and the speedy performance of a solid-state drive (SSD). However 16GB of storage does not offer much room. One popular option is to open up the device and swap in a bigger SSD.                                                                                    

An alternative is to reserve the internal SSD for the OS and use an external USB storage device for data. My plan is to keep the USB stick attached to the Chromebook to provide extra storage that can be disconnected and re-connected at will.

Let's go!
=========

I picked up a **SanDisk Ultra Fit 64GB USB 3.0**  which are really tiny devices that barely extrude from the USB port. To guard against loss or theft its a good idea to encrypt the USB stick. I prepare the device using **Linux Unified Key Setup** (LUKS) and the ``cryptsetup`` utility.

.. role:: warning

:warning:`WARNING!` Make careful note of the drive and partition labels. The following steps **will destroy all data** currently stored on the drive.

0. Prepare
==========

Download ``cryptsetup`` if not already installed. Connect the USB stick, leave it **unmounted**, and make note of the device label (``sdb``, ``sdc`` ...):

.. code-block:: bash

    $ lsblk

1. Partition
============

Create a single partition using ``fdisk`` or ``gparted`` that fills the entire drive. Encrypt the partition and assign a password:

.. code-block:: bash

    $ sudo cryptsetup luksFormat /dev/sdX1
    $ sudo cryptsetup luksOpen /dev/sdX1 sdX1_crypt

2. Filesystem
=============

Install a filesystem (example: ``ext4``) [1]_ and mount the partition to gain access to the storage:

.. code-block:: bash

    $ sudo mkfs.ext4 -m 1 -E lazy_itable_init=0,lazy_journal_init=0 /dev/mapper/sdX1_crypt
    $ sudo mount -t ext4 /dev/mapper/sdX1_crypt /mnt

Before disconnecting the drive the partition must be unmounted and the encrypted device must be closed:

.. code-block:: bash

    $ sudo umount /mnt
    $ sudo cryptsetup luksClose /dev/mapper/sdX1_crypt

3. Mountpoint
=============

Create a custom mountpoint (example ``/media/USB``):

.. code-block:: bash

    $ sudo mkdir /media/USB

Add entry in ``/etc/fstab`` for mountpoint:

.. code-block:: bash

    /dev/mapper/sdX1_crypt  /media/USB   ext4    rw,user,exec,noatime,noauto,data=ordered        0       0

4. Boot
=======

One wrinkle on the Chromebook is that attaching a USB stick makes the device always try to boot (and fail) from USB instead of internal storage. There appears to be no way to alter the default boot order in **SeaBIOS** except to rebuild the firmware. Plus I like that the USB boot option actually works! Simple workaround is just hit ``ESC`` key at startup to access boot menu and manually choose the SSD.

Happy hacking!

Notes
-----

.. [1] Writing ``ext4`` with options ``-m 1`` reduces reserved filesystem blocks from default 5% to 1% (grab extra space for non-root partitions) and ``lazy_itable_init=0,lazy_journal_init=0`` initializes the inodes and journal at creation time vs a gradual process during mount times. If you wonder why your newly-formatted drive's activity LED is blinking away... install and run ``iotop`` and take note of ``ext4lazyinit`` and `Lazy Initialization <https://www.thomas-krenn.com/en/wiki/Ext4_Filesystem#Lazy_Initialization>`_.
