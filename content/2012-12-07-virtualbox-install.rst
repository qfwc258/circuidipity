=====================================
Virtualbox with Debian HOST and GUEST
=====================================

:tags: virtual environments, linux, debian
:slug: virtualbox-install

`Virtualbox <https://www.virtualbox.org/>`_ is virtualization software that allows a Linux user to HOST multiple GUEST OSs as *virtual machines* (VMs). Its an awesome piece of kit for playing with different Linux distros and experimenting with configurations without blowing up your main box.

In this HOWTO I install Virtualbox on a Debian HOST and create a Debian GUEST VM.

Step 0 - Install
================

.. code-block:: bash

    $ sudo apt-get install dkms linux-headers-amd64
    $ sudo apt-get install virtualbox virtualbox-dkms virtualbox-qt

Virtualbox kernel modules are built via *Dynamic Kernel Module Support* (`DKMS <http://en.wikipedia.org/wiki/Dynamic_Kernel_Module_Support>`_). After installing the virtualbox packages the ``vbox`` modules should be auto-built and -loaded ...

.. code-block:: bash

    $ lsmod | grep vbox
    vboxpci                19066  0 
    vboxnetadp             13155  0 
    vboxnetflt             23571  0 
    vboxdrv               190057  4 vboxnetflt,vboxnetadp,vboxpci

Add USERNAME to the ``vboxusers`` group ``sudo adduser USERNAME vboxusers``.

Step 1 - Create VM
==================

The *Default Machine Folder* where VM images are stored is ``$HOME/Virtualbox VMs`` (this can be modified in ``File->Preferences->General``).

See the `User Manual <http://www.virtualbox.org/manual/UserManual.html>`_ for creating a GUEST VM. I use the `Debian mini installer <http://ftp.nl.debian.org/debian/dists/testing/main/installer-amd64/current/images/netboot/mini.iso>`_ to create a new VM with a minimal system configuration. The installer auto-detects it is being configured as a VM and prompts for permission to install the ``virtualbox-ose-guest-x11`` package. Go ahead and install.

After the new Debian guest VM is sucessfully created I *clone* the image ``Machine->Clone ...`` - preserving the fresh install image 'as is' - and go off to do all my experiments on the clone. Saves having to repeat the installation all over again.

Step 2 - Guest VM Configuration
===============================

*Guest Additions* are designed to be installed inside a guest VM after the operating system has been installed. `This video <https://www.youtube.com/watch?v=Q84boOmiPW8>`_ was helpful for setting it up. Some cool extra features they bring to the party are the ability to tweak display settings and add a shared folder that can accessed by both HOST and GUEST machines.

.. note::

    There is much discussion online about installing the virtualbox *guest-additions iso* (available both from virtualbox.org and as a Debian package) and the `extensions pack <https://www.virtualbox.org/manual/ch01.html#intro-installing>`_ but I skipped it.

Startup your newly-created (clone) Debian guest VM and install ...

.. code-block:: bash

    $ sudo apt-get install dkms
    $ sudo apt-get install virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11

Add USERNAME to the ``vboxsf`` group.

Tweak display settings by going to the VM&#39;s ``Machine->Settings...->Display`` and move the slider to add more video memory and enable 3d acceleration.

.. image:: images/20121207-display.png
    :alt: Display Settings
    :align: center
    :width: 662px
    :height: 502px

With virtualbox guest additions installed the display and resolution can be changed when running X ...

.. code-block:: bash

    $ ps aux | grep VBox
    /usr/sbin/VBoxService
    /usr/bin/VBoxClient --clipboard
    /usr/bin/VBoxClient --display
    /usr/bin/VBoxClient --seamless

If the VM does not use a graphical login manager to launch its desktop then modify ``$HOME/.xinitrc`` to start VBoxClient services ...

.. code-block:: bash

    VBoxClient --clipboard &
    VBoxClient --display &
    VBoxClient --seamless &

Next create a shared folder on HOST. Make it accessible to GUEST by going to ``Machine->Settings...->Shared Folders`` and click ``Add Shared Folder`` and ``Auto-Mount``.

.. image:: images/20121207-shared-folders.png
    :alt: Shared Folder Settings
    :align: center
    :width: 662px
    :height: 502px

GUEST should see ``vbox`` running processes ...

.. code:: bash

    $ lsmod | grep vbox
    vboxguest
    vboxsf
    vboxvideo
