==============================
Add USB storage to Chromebooks
==============================

:date: 2014-10-31 00:11:00
:slug: 20141031
:tags: chromebook, lubuntu, ubuntu, linux
:modified: 2015-01-29 11:56:00

I love my `Lubuntubook <http://www.circuidipity.com/c720-lubuntubook.html>`_ and the speedy performance of a solid-state drive (SSD). However 16GB of storage does not offer much room. One popular option is to `open up the device <http://www.circuidipity.com/c720-lubuntubook.html>`_ and swap in a bigger SSD.                                                                                    

An alternative is to reserve the internal SSD for the OS and use an external USB storage device for data. I picked up a `SanDisk Cruzer Fit 64GB USB 2.0 <http://www.amazon.com/SanDisk-Cruzer-Low-Profile-Drive-SDCZ33-064G-B35/dp/B00FJRS6QY>`_ which are really tiny devices that barely extrude from the USB port.

My plan is to keep the USB stick attached to the Chromebook (extra storage that can be disconnected and re-connected at will) and have Lubuntu auto-mount the device at boot.

Let's go!
=========

0. Filesystem
-------------

Device has a single partition that I re-format as ``ext4``:

.. code-block:: bash

    $ sudo mke2fs -t ext4 /dev/sdX1

1. UUID
-------

Retrieve the `Universally Unique Identifer <https://help.ubuntu.com/community/UsingUUID>`_ (UUID) of the USB stick's partition (example uses ``sdb1``):

.. code-block:: bash

    $ sudo blkid | grep sdb1
    /dev/sdb1: UUID="3e75240d-97b6-49cb-af21-fac25d574851" TYPE="ext4"

2. Auto-mount
-------------

Configure system to auto-mount USB stick at boot by creating a new mountpoint for the device:

.. code-block:: bash

    $ sudo mkdir /media/USB0

... and create a new entry in ``/etc/fstab``:

.. code-block:: bash

    UUID=3e75240d-97b6-49cb-af21-fac25d574851 /media/USB0 ext4 rw,exec,noatime,nobootwait 0 0

Note that ``nobootwait`` is an ``upstart``-specific option to the ``mountall`` command on `Ubuntu <http://www.circuidipity.com/tag-ubuntu.html>`_ and its derivatives. It enables boot to continue without manual intervention if the device is not found.

3. Boot
-------

One wrinkle on the Chromebook is that attaching a USB stick makes the laptop always try to boot (and fail) from USB instead of internal storage. There appears to be no way to alter the default boot order in **SeaBIOS** except to rebuild the firmware. Plus I like that the USB boot option actually works! Simple workaround is just hit ``ESC`` key at startup to access boot menu and manually choose the SSD.

Happy hacking!
