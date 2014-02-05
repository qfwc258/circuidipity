=======================================================
Fix the backlight on laptops using Intel video chipsets
=======================================================

:tags: linux
:slug: intel-backlight

There are issues with some Intel video cards ``xserver-xorg-video-intel`` and ``KMS`` and the default ``2.6.32 kernel`` in Debian ``squeeze``.

On my Intel-equipped `Asus netbook <debian-linux-on-the-asus-eeepc-1001p.html>`_ booting from GRUB or starting an X session can result in a black screen and completely unresponsive system. A temporary fix is to edit the booting GRUB entry and add ``acpi=off`` to the kernel line.

A more permanent fix is to configure the backlight by editing ``GRUB_CMDLINE_LINUX_DEFAULT`` in ``/etc/default/grub`` ...

.. code-block:: bash

    GRUB_CMDLINE_LINUX_DEFAULT="quiet acpi_osi=Linux acpi_backlight=vendor"

Update the grub configuration by running ``sudo update-grub2`` and reboot.

Increase the brightness setting to maximum visibility. For example ... on my netbook</a> I run ...

.. code-block:: bash

    $ sudo echo 15 > /sys/class/backlight/eeepc/brightness
