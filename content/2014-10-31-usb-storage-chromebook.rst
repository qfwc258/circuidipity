==============================
Add USB storage to Chromebooks
==============================

:date: 2014-10-31 00:11:00
:slug: 20141031
:tags: chromebook, lubuntu, ubuntu, linux

I love my `Lubuntubook <http://www.circuidipity.com/c720-lubuntubook.html>`_ and the speedy performance of a solid-state drive (SSD). However 16GB of storage does not offer much room to shuffle data around. One popular option is to `open up the device <http://www.circuidipity.com/c720-lubuntubook.html>`_ and swap in a bigger SSD.                                                                                    

An alternative is to reserve the internal SSD for the OS and use an external USB storage device for data. I picked up a `SanDisk Cruzer Fit 64GB USB 2.0 <http://www.amazon.com/SanDisk-Cruzer-Low-Profile-Drive-SDCZ33-064G-B35/dp/B00FJRS6QY>`_ which are really tiny devices that barely extrude from the USB port.

My plan is to keep the USB stick attached to the Chromebook (extra storage that can be disconnected and re-connected at will) and have Lubuntu auto-mount the device at boot. Steps to get it working:

0. Partition and format
-----------------------

Wipe any SanDisk stuff off the device by creating a new partition table with a single partition using a partitioning utility (such as **fdisk**). I chose to format the partition as **FAT32** for the widest range of compatibility using **mkfs**:

.. code-block:: bash

    $ sudo mkfs.vfat /dev/sd[device_label]1

1. Auto-mount
-------------

Configure the system to auto-mount the USB stick at boot by creating a new mount point for the device:

.. code-block:: bash

    $ sudo mkdir /media/usb-extra

... and create a new entry in ``/etc/fstab``:

.. code-block:: bash                                                               
                                                                                   
    UUID=7168-E0A7  /media/usb-extra    vfat   rw,user,noatime,uid=1000,gid=1000,shortname=mixed,dmask=0077,fmask=0133,utf8=1,flush,nobootwait  0   0

Experiment with the settings. Note that ``nobootwait`` is an ``upstart``-specific option to the ``mountall`` command on `Ubuntu <http://www.circuidipity.com/tag-ubuntu.html>`_ and its derivatives. It enables boot to continue without manual intervention if the device is not found.

2. Boot
-------

One wrinkle on the **Acer C720 Chromebook** is that an attached USB storage device makes the laptop always try to boot from USB (and fail) instead of internal storage. There appears to be no way to alter the default boot order in **SeaBIOS** except to rebuild the firmware. Plus I **like** that USB booting actually works on this device! The simple workaround is just hit **ESC** at startup to access the boot menu and manually choose the SSD.

Happy hacking!
