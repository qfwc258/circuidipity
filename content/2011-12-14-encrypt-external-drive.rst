===================================================
Configure an encrypted external hard drive in Linux
===================================================

:tags: linux
:slug: encrypt-external-drive

Using an external USB-connected hard drive is part of my personal backup plan (the other part is backups to a `home server <linux-home-server.html>`_).

I actually use 2 one terabyte drives. One drive is in my possession and the other drive I store at a friend's home. Periodically I swap the drives and update the data via the *sneakernet*.

To guard against loss or theft its a good idea to *encrypt* the hard drive. I prepare the device using *Linux Unified Key Setup (LUKS)* and the ``cryptsetup`` utility.

.. warning::

    In this example the external hard drive is identified as *sdb* and contains a single partition *sdb1*. Make careful note of the drive and partition labels on **your system** as they can be very different. The following steps will **destroy all data** currently stored on the drive.

Download the cryptsetup package if not already installed. Connect the external drive, make note of drive labels (``sdb``, ``sdb1`` ...), and erase/overwrite the drive.

Filling the drive with zeros can take several hours depending on storage size. *Random number generation* is even more secure but takes much longer ...

.. code-block:: bash

    # dd if=/dev/zero of=/dev/sdb bs=1M

Create a single partition that fills the entire drive. Encrypt that newly-created partition and assign a password ...

.. code-block:: bash

    $ sudo cryptsetup luksFormat /dev/sdb1
    $ sudo cryptsetup luksOpen /dev/sdb1 sdb1_crypt

Install a filesystem (I use ``ext4``) and mount the partition to gain access to the storage ...

.. code-block:: bash

    $ sudo mkfs -t ext4 /dev/mapper/sdb1_crypt
    $ sudo mount /dev/mapper/sdb1_crypt /mnt

Before disconnecting the drive the partition must be unmounted and the encrypted device must be closed ...

.. code-block:: bash

    $ sudo umount /mnt
    $ sudo cryptsetup luksClose /dev/mapper/sdb1_crypt

A file manager like `Thunar <http://thunar.xfce.org/>`_ can automatically mount and unmount encrypted partitions. For scripting purposes its useful to assign a *default mount point* for the encrypted drive ... that is, whenever the drive is plugged into your system it will always be mounted in the same location.

Mount the encrypted drive, retrieve the LUKS string for the partition, and create a custom mount point (``/media/crypt`` in my example) ...

.. code-block:: bash

    $ ls /dev/mapper/luks*      # outputs '/dev/mapper/luks_crypto_STRING'
    $ sudo mkdir /media/crypt

Unmount the drive and create an entry in ``/etc/fstab`` for the new custom mount point ...

.. code-block:: bash

    /dev/mapper/luks_crypto_STRING  /media/crypt    auto    users,noauto,noatime    0   0

Next time the drive is auto-mounted it will be assigned to ``/media/crypt``.
