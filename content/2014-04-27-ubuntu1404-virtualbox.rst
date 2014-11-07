===========================
Ubuntu 14.04 and Virtualbox
===========================

:date: 2014-04-27 01:23:00
:tags: virtual environments, debian, ubuntu, linux
:slug: ubuntu1404-virtualbox

`Virtualbox <https://www.virtualbox.org/>`_ is virtualization software that allows a Linux user to HOST multiple GUEST operating systems as *virtual machines* (VMs). Its a cool tool for playing with different Linux distros and experimenting with configurations.

In this HOWTO I install Virtualbox on a Debian HOST and create an Ubuntu GUEST virtual machine.

0. Install VirtualBox on HOST
=============================

.. code-block:: bash

    $ sudo apt-get install build-essential dkms module-assistant linux-headers-$(uname -r)
    $ sudo apt-get install virtualbox virtualbox-dkms virtualbox-qt

Virtualbox kernel modules are built via **Dynamic Kernel Module Support** (`DKMS <http://en.wikipedia.org/wiki/Dynamic_Kernel_Module_Support>`_). After installing the virtualbox packages the ``vbox`` modules should be auto-built and -loaded: 

.. code-block:: bash

    $ lsmod | grep vbox
    vboxpci                19066  0 
    vboxnetadp             13155  0 
    vboxnetflt             23571  0 
    vboxdrv               190057  4 vboxnetflt,vboxnetadp,vboxpci

I add my USERNAME to the ``vboxusers`` group:

.. code-block:: bash

    $ sudo adduser YOUR_USERNAME vboxusers

1. Create the Ubuntu GUEST
==========================

The **Default Machine Folder** where VM images are stored is ``$HOME/Virtualbox VMs`` (this can be modified in ``File->Preferences->General``).

See the `User Manual <http://www.virtualbox.org/manual/UserManual.html>`_ for creating a GUEST virtual machine. I use the `Ubuntu mini.iso installer <http://archive.ubuntu.com/ubuntu/dists/trusty/main/installer-amd64/current/images/netboot/>`_ to create a new virtual machine with a minimal system configuration.

2. GUEST Additions
==================

**Guest Additions** provide extra features such as the ability to tweak display settings and add a shared folder that can accessed by both HOST and GUEST machines.

On the new Ubuntu GUEST run:

.. code-block:: bash

    $ sudo apt-get install build-essential module-assistant linux-headers-$(uname -r) dkms
    $ sudo apt-get install virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
    $ sudo m-a prepare
    $ sudo adduser YOUR_USERNAME vboxsf

If the virtualbox modules need to be rebuilt for any reason for the running kernel:

.. code-block:: bash

    $ uname -r | sudo xargs -n1 /usr/lib/dkms/dkms_autoinstaller start

Reboot Ubuntu GUEST and ``vbox`` drivers should now be loaded:

.. code:: bash

    $ lsmod | grep vbox
    vboxguest
    vboxsf
    vboxvideo

3. GUEST Configuration
======================

Tweak display settings by going to the Virtualbox ``Machine->Settings...->Display`` setting and move the slider to add more video memory and enable 3d acceleration.

.. image:: images/20121207-display.png
    :align: center
    :alt: Display Settings
    :width: 662px
    :height: 502px

With VirtualBox guest additions the display and resolution can be changed when running X:

.. code-block:: bash

    $ ps aux | grep VBox
    /usr/sbin/VBoxService
    /usr/bin/VBoxClient --clipboard
    /usr/bin/VBoxClient --display
    /usr/bin/VBoxClient --seamless

If GUEST does not use a graphical login manager to launch its desktop then modify ``$HOME/.xinitrc`` to start VBoxClient services:

.. code-block:: bash

    VBoxClient --clipboard &
    VBoxClient --display &
    VBoxClient --seamless &

Next create a shared folder on HOST. Make it accessible to GUEST by going to ``Machine->Settings...->Shared Folders`` and click ``Add Shared Folder`` and ``Auto-Mount``.

.. image:: images/20121207-shared-folders.png
    :align: center
    :alt: Shared Folder Settings
    :width: 662px
    :height: 502px

Happy hacking!
