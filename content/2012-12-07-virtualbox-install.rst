=====================
Debian and Virtualbox
=====================

:tags: virtual environments, linux, debian
:slug: virtualbox-install
:modified: 27 April 2014

`Virtualbox <https://www.virtualbox.org/>`_ is virtualization software that allows a Linux user to HOST multiple GUEST operating systems as *virtual machines* (VMs). Its a cool tool for playing with different Linux distros and experimenting with configurations.

In this HOWTO I install Virtualbox on a 64-bit Debian HOST and create a Debian GUEST virtual machine.

Step 0 - Install VirtualBox on HOST
===================================

.. code-block:: bash

    $ sudo apt-get install build-essential dkms module-assistant linux-headers-$(uname -r)
    $ sudo apt-get install virtualbox virtualbox-dkms virtualbox-qt

Virtualbox kernel modules are built via *Dynamic Kernel Module Support* (`DKMS <http://en.wikipedia.org/wiki/Dynamic_Kernel_Module_Support>`_). After installing the virtualbox packages the ``vbox`` modules should be auto-built and -loaded ...

.. code-block:: bash

    $ lsmod | grep vbox
    vboxpci                19066  0 
    vboxnetadp             13155  0 
    vboxnetflt             23571  0 
    vboxdrv               190057  4 vboxnetflt,vboxnetadp,vboxpci

I add my USERNAME to the ``vboxusers`` group...

.. code-block:: bash

    $ sudo adduser YOUR_USERNAME vboxusers

Step 1 - Create the Debian GUEST
================================

The *Default Machine Folder* where VM images are stored is ``$HOME/Virtualbox VMs`` (this can be modified in ``File->Preferences->General``).

See the `User Manual <http://www.virtualbox.org/manual/UserManual.html>`_ for creating a GUEST virtual machine. I use the `Debian mini.iso installer <http://ftp.us.debian.org/debian/dists/stable/main/installer-i386/current/images/netboot/>`_ to create a new virtual machine with a minimal system configuration. The installer auto-detects it is being configured as a virtualbox GUEST and installs the necessary ``virtualbox-guest-{dkms,utils,x11}`` packages.

Step 2 - GUEST Additions
========================

*Guest Additions* provide extra features such as the ability to tweak display settings and add a shared folder that can accessed by both HOST and GUEST machines.

I ran into a situation with my Debian 32-bit virtual machine where the installer created virtualbox kernel modules for ``linux-image-686-pae`` but not the ``486`` kernel I ended up using. Confirm that the current kernel has the necessary modules...

.. code-block:: bash

    $ modinfo /lib/modules/$(uname -r)/updates/dkms/vbox*

If they are missing like they were for me ... use DKMS to build them...

.. code-block:: bash

    $ sudo apt-get install build-essential dkms module-assistant linux-headers-$(uname -r)
    $ sudo m-a prepare
    $ sudo adduser YOUR_USERNAME vboxsf

If the virtualbox modules need to be rebuilt for any reason for the running kernel...

.. code-block:: bash

    $ uname -r | sudo xargs -n1 /usr/lib/dkms/dkms_autoinstaller start

Reboot Debian GUEST and ``vbox`` drivers should now be loaded...

.. code:: bash

    $ lsmod | grep vbox
    vboxguest
    vboxsf
    vboxvideo

Step 3 - GUEST Configuration
============================

Tweak display settings by going to the Virtualbox ``Machine->Settings...->Display`` setting and move the slider to add more video memory and enable 3d acceleration.

.. image:: images/20121207-display.png
    :alt: Display Settings
    :width: 662px
    :height: 502px

With VirtualBox guest additions the display and resolution can be changed when running X...

.. code-block:: bash

    $ ps aux | grep VBox
    /usr/sbin/VBoxService
    /usr/bin/VBoxClient --clipboard
    /usr/bin/VBoxClient --display
    /usr/bin/VBoxClient --seamless

If GUEST does not use a graphical login manager to launch its desktop then modify ``$HOME/.xinitrc`` to start VBoxClient services...

.. code-block:: bash

    VBoxClient --clipboard &
    VBoxClient --display &
    VBoxClient --seamless &

Next create a shared folder on HOST. Make it accessible to GUEST by going to ``Machine->Settings...->Shared Folders`` and click ``Add Shared Folder`` and ``Auto-Mount``.

.. image:: images/20121207-shared-folders.png
    :alt: Shared Folder Settings
    :width: 662px
    :height: 502px

Happy hacking!
