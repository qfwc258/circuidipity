=====================================
Modify the default boot order in GRUB
=====================================

:date: 2014-08-31 01:23:00
:slug: 20140831
:tags: debian, linux, chromebook

My `Chromebook running Debian <http://www.circuidipity.com/c720-sidbook.html>`_ requires a less-than-recent kernel (3.13.10) that supports `compiling modules <https://github.com/vonbrownie/linux-post-install/blob/master/extra/c720_sidbook/scripts/c720-kernel-mods.sh>`_ for the laptop's touchpad. After installing a kernel retrieved from `snapshot.debian.org <http://snapshot.debian.org>`_ the GRUB boot manager auto-generates a menuentry for the new kernel but defaults to booting the most recent kernel available.

This is how I changed the GRUB boot order to default to my touchpad-friendly kernel.

Step 0 - Install a (less-than-current) Debian-packaged kernel
=============================================================

I am running Debian's *sid* (unstable) branch and the 3.13.X kernel is no longer available in the package manager. I download the kernel headers and image and install the packages using ``dpkg`` ...

.. code-block:: bash

    $ wget http://snapshot.debian.org/archive/debian/20140320T042639Z/pool/main/l/linux-tools/linux-kbuild-3.13_3.13.6-1_amd64.deb
    $ sudo dpkg -i linux-kbuild-3.13_3.13.6-1_amd64.deb
    $ wget http://snapshot.debian.org/archive/debian/20140416T101543Z/pool/main/l/linux/linux-headers-3.13-1-common_3.13.10-1_amd64.deb
    $ sudo dpkg -i linux-headers-3.13-1-common_3.13.10-1_amd64.deb
    $ wget http://snapshot.debian.org/archive/debian/20140416T101543Z/pool/main/l/linux/linux-headers-3.13-1-amd64_3.13.10-1_amd64.deb
    $ sudo dpkg -i linux-headers-3.13-1-amd64_3.13.10-1_amd64.deb
    $ wget http://snapshot.debian.org/archive/debian/20140416T101543Z/pool/main/l/linux/linux-image-3.13-1-amd64_3.13.10-1_amd64.deb
    $ sudo dpkg -i linux-image-3.13-1-amd64_3.13.10-1_amd64.deb

A menuentry for the new kernel is auto-generated in ``/boot/grub/grub.cfg``.

Step 1 - Retrieve the kernel menuentry
======================================

Inside ``grub.cfg`` there is an option for ``submenu 'Advanced options for Debian GNU/Linux'`` and beneath it multiple menuentries for installed kernels and boot options. Using my Chromebook's 3.13.10 kernel as an example the relevant entry is ...

.. code-block:: bash

    menuentry 'Debian GNU/Linux, with Linux 3.13-1-amd64'

This will be designated as the new default kernel to boot.

Step 2 - Set default kernel
===========================

Open ``/etc/default/grub`` in an editor and modify ``GRUB_DEFAULT=`` (set to '0' or most recent by default) to the new desired boot kernel. In the case of my Chromebook I include the submenu + menuentry in the modified setting ...

.. code-block:: bash

    GRUB_DEFAULT="Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 3.13-1-amd64"

Run ``sudo update-grub`` to generate a new config and reboot. At the GRUB splash screen the ``Advanced options for Debian GNU`` menu will be the new default and the designated kernel will load.

Happy hacking!
