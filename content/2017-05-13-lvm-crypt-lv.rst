=================================
LVM and encrypted Logical Volumes
=================================

:date: 2017-05-13 16:43:00
:slug: lvm-crypt-lv
:tags: lvm, crypto, linux

I have been playing with the **Logical Volume Manager** (LVM) on my recent Debian installs. Instead of creating a traditional partition layout on a hard drive, LVM adds a layer of abstraction over physical storage that allows the creation of "virtual" partitions. 

For my `netbook home server setup <http://www.circuidipity.com/laptop-home-server.html>`_ I used the Debian installer's manual partitioning tools to assign a partition to LVM, create a **Volume Group** (VG) and **Logical Volumes** (LVs), with plenty of storage space to spare. [1]_ After a successful first boot I configure an encrypted container for data storage that is manually mounted by a non-root user. I don't want an unattended server halting in the boot process waiting for a passphrase or any necessary boot mountpoints to reside on an encrypted partition.

Let's go!
=========

Scan my netbook for devices visible to LVM ... 

.. code-block:: bash

    # lvmdiskscan
    /dev/vg/root              [      14.90 GiB]
    /dev/sda1                 [     487.00 MiB]
    /dev/vg/swap              [     952.00 MiB]
    /dev/sda2                 [     465.28 GiB] LVM physical volume
    /dev/mapper/vg-swap_crypt [     952.00 MiB]
    3 disks
    1 partition
    0 LVM physical volume whole disks
    1 LVM physical volume

Check for free space in the volume group ...

.. code-block:: bash

    # vgdisplay
    [...]
    Free  PE / Size       115060 / 449.45 GiB
    [...]

0. Create
---------

I create a 400GB ``data`` logical volume in the volume group ...

.. code-block:: bash

    # lvcreate --size 400G vg --name data

Information about the LVs can be displayed with the ``lvdisplay`` command.

1. Encrypt
----------

Configure LUKS encryption on the newly-created LV ...

.. code-block:: bash

    # cryptsetup luksFormat /dev/vg/data
      
Open LV ``data`` under ``vg-data_crypt``, format with a filesystem, and mount ... [2]_

.. code-block:: bash

    # cryptsetup open /dev/vg/data vg-data_crypt
    # mkfs.ext4 -m 1 /dev/mapper/vg-data_crypt
    # mount /dev/mapper/vg-data_crypt /mnt

When finished, unmount the filesystem and close the encrypted LV ...

.. code-block:: bash

    # umount /mnt
    # cryptsetup close /dev/mapper/vg-data_crypt

2. Mountpoint
-------------

I create a dedicated mountpoint for the LV in ``/media`` ...

.. code-block:: bash

    # mkdir /media/crypt_data

Modify ``/etc/fstab`` and allow mounting by a non-root user ...

.. code-block:: bash

    /dev/mapper/vg-data_crypt /media/crypt_data        ext4    relatime,noauto,user       0       0
    
Open the LV and mount ...

.. code-block:: bash

    # cryptsetup open /dev/vg/data vg-data_crypt
    $ mount /media/crypt_data

Happy hacking!

Notes
+++++

.. [1] For setting up LVM from the beginning and learning about its tools the LVM entries on `wiki.debian.org <https://wiki.debian.org/LVM>`_ and `wiki.archlinux.org <https://wiki.archlinux.org/index.php/LVM>`_ are very helpful!

.. [2] Reserved blocks can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large non-root partitions extra space can be gained by reducing the default 5% reserve to 1% with option ``-m <percent>``.

