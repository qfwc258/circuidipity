================================
Install Debian Squeeze GNU/Linux
================================

:date: 2010-06-03 01:23:00
:tags: debian, linux, install
:slug: install-debian-linux-squeeze

Happy news! On February 6, 2011 the word came down: "After 24 months of constant development, the Debian Project is proud to present its new `stable version 6.0 'Squeeze' <http://www.debian.org/News/2011/20110205a>`_".

Debian GNU/Linux is the one of the largest and longest-running all-volunteer free software projects in the world. One of the (many) things I like about Debian is how they balance the competing desires of *"ooohhh... shiny!"* vs *stability* in Linux by maintaining 3 different releases of the distribution: ``stable/squeeze``, ``testing/wheezy``, and ``unstable/sid``.

For a recent `home server setup <http://www.circuidipity.com/linux-home-server.html>`_ and laptop installation I chose ``stable``. Bleeding-edge packages are not required and these systems benefit from active security patches and bug fixes while avoiding any potentially disruptive changes in a very solid working environment.

``Unstable`` is the staging ground for changes which - if no serious bugs are unearthed - migrate in short order to ``testing``. Which in turn is destined to be "released when its ready" and become the next version of ``stable``. It is even possible to use `backports <http://backports.debian.org/>`_ plus - lightly and with caution - `apt-pinning <http://www.debian.org/doc/manuals/debian-reference/ch02.en.html#_tweaking_candidate_version>`_ to pull packages from different releases and create the perfect mix (as tailored by you) of stability and freshness.

Step 0 - Start
==============

I like to start with a *lightweight minimal* installation of Debian.

`Download <http://www.debian.org/distrib/>`_ one of the many versions of the Debian installation images. In this HOWTO example I select ``i386`` as my target architecture and I use the small ``businesscard.iso``: `Torrent <http://cdimage.debian.org/debian-cd/current/i386/bt-cd/debian-6.0.3-i386-businesscard.iso.torrent>`_ | `Direct download <http://cdimage.debian.org/debian-cd/current/i386/iso-cd/debian-6.0.3-i386-businesscard.iso>`_

Download the `MD5SUMS <http://cdimage.debian.org/debian-cd/current/i386/iso-cd/MD5SUMS>`_ file and confirm the Debian ``businesscard.iso`` is a "good" copy by running:

.. code-block:: bash

    $ md5sum debian-VERSION-i386-businesscard.iso; cat MD5SUMS | grep businesscard

Ensure the two strings of numbers match before proceeding.

Step 1 - Prepare USB stick
==========================

USB sticks are my Linux install media of choice because I have configured several devices that do not include an optical drive. Plug the USB stick into your Linux host machine and leave the stick **unmounted**. Run the ``dmesg`` command and note the USB device ID (``sdb``, ``sdc``, ...).

.. role:: warning

:warning:`WARNING!` Make sure to record the correct USB device ID. The following procedure **wipes out all data on the USB stick.** On my system the device shows up as ``sdb`` but it will possibly be different on **your** system.

Copy the iso to the USB stick:

.. code-block:: bash

    # cat debian-VERSION-i386-businesscard.iso > /dev/sdX 
    # sync

Step 2 - Install
================

BIOS and the Debian installer
-----------------------------

Plug the freshly prepared USB stick into the target box. Power up. Either the device is pre-configured in the BIOS to recognize a USB stick as the first choice for boot or hit the device hotkey to enter the boot menu. Select the USB stick and launch the Debian installer.

.. code-block:: bash

    Advanced Options -> Expert install

Mostly I stick with the default selections presented by the Debian installer .. with a few exceptions noted below.

Choose a mirror of the Debian archive
-------------------------------------

Debian's ``businesscard`` installer allows a choice of Debian versions - ``stable``, ``testing``, or ``unstable``:

.. code-block:: bash

    Debian version to install:
    squeeze - stable             

Partition disks
---------------

Creating encrypted partitions with **Erase date: yes** (default) overwrites the partition with random data and can take many hours depending on partition size.

Select the ``Manual`` option to partition the drive. I choose to encrypt my ``swap`` and ``home`` partitions. Space permitting - my chosen partition layout is:

.. code-block:: bash

    sda1 - 20GB - root partition - filesystem: ext4, noatime
    sda2 - 1GB - swap partition - filesystem: swap, Encryption key: Random key
    sda3 - remaining space - home partition - filesystem: ext4, noatime, reserved blocks: 1%, Encryption key: Passphrase

Placing ``root`` on a separate partition allows the flexibility of re-installing the operating system at a later date without overwriting ``home``.

Install the base system
-----------------------

No need to include every driver under the sun. Just let the system load what is needed:

.. code-block:: bash

    Drivers to include in the initrd:
    targeted: only include drivers needed for this system

Configure the package manager
-----------------------------

I choose to enable the ``non-free`` archive (useful if you require non-free firmware for devices such as wireless chipsets):

.. code-block:: bash

    Use non-free software?
    <Yes>

Software selection
------------------

A custom Debian machine starts as a *minimal* machine. *Un-select* all the software choices *except* for the standard system utilities:

.. code-block:: bash

    Choose software to install:
    [*] Standard system utilities

Finish installation
-------------------

Finish setting up a lightweight base installation. Reboot ...

Step 3 - Configure
==================

Fix time (if necessary)
-----------------------

.. code-block:: bash

    tzconfig    # select timezone
    date MMDDHHmmCCYY    # change the date and time to local settings 
    hwclock --utc    # set hardware clock to universal time
    hwclock --systohc    # set system time to hardware clock

Blacklist modules
-----------------

A system that makes use of encrypted hard drive partitions may notice the following error at boot - ``modprobe: fatal: error inserting padlock_sha ... no such device``.

It is harmless and the crypto-partitions mount as expected. But if you want to remove the error messages - and the affected system does not contain a VIA CPU - then *blacklist* the ``padlock_aes`` and ``padlock_sha`` modules by editing ``/etc/modprobe.d/blacklist.conf`` (let's also get rid of that "beep beep" pcspeaker as a bonus):

.. code-block:: bash

    # no beep, thanks
    blacklist pcspkr

    # no VIA CPU no padlock needed foo
    blacklist padlock_aes
    blacklist padlock_sha

Console tools
-------------

Install:

.. code-block:: bash

    # apt-get install anacron colordiff cowsay dosfstools firmware-linux gpm htop input-utils rsync sudo sysv-rc-conf vrms

Sudo
----

Allow a user to run commands with root-privileges using ``sudo``. Run the command ``visudo -s`` and configure:

.. code-block:: bash

    # Allow members of group sudo to execute any command
    %sudo   ALL=(ALL:ALL) ALL

    # User privilege specification
    root    ALL=(ALL:ALL) ALL
    # Allow user to run certain commands without prompting for a password
    yourusername     ALL=NOPASSWD: /sbin/cryptsetup, /sbin/halt, /sbin/ifconfig

Save changes and add your USERNAME to ``sudo`` group:

.. code-block:: bash

    # adduser USERNAME sudo

Wireless
--------

Wifi-equipped machines usually require additional firmware. My Thinkpad X201, for example, requires the `firmware-iwlwifi <http://packages.debian.org/squeeze/firmware-iwlwifi>`_ package:

.. code-block:: bash

    $ sudo apt-get install wireless-tools
    $ sudo apt-get install firmware-PACKAGENAME

Run ``ifconfig -a`` and confirm the wireless_interface is detected (usually identified as ``eth1`` or ``wlan0``). For manual setup of a wireless_interface (example: ``wlan0``) connecting to an access point with no encryption:

.. code-block:: bash

    $ ifconfig eth0 down
    $ iwconfig
    $ ifconfig wlan0 up
    $ iwlist wlan0 scan | less
    $ iwconfig wlan0 essid "ACCESSPOINT"
    $ iwconfig wlan0
    $ dhclient wlan0

Backports
---------

`Backports.debian.org <http://backports.debian.org/>`_ contains packages from Debian's ``testing`` and ``unstable`` releases that have been recompiled for ``stable``.

Add the archive to the package manager by generating an entry in ``/etc/apt/sources.list.d``:

.. code-block:: bash

    $ sudo echo 'deb http://backports.debian.org/debian-backports squeeze-backports main' > /etc/apt/sources.list.d/squeeze-backports.list
    $ sudo apt-get update

Files in ``sources.list.d`` must end with a ``*.list`` extension.

To verify which versions of a package are available and - for example - to install the version from backports:

.. code-block:: bash

    $ apt-cache policy PACKAGE
    $ sudo apt-get -t squeeze-backports install PACKAGE

Multimedia
----------

Add `marillat's debian-multimedia archive <http://debian-multimedia.org/>`_. Download and install the archive encryption key:

.. code-block:: bash

    $ wget -c http://www.debian-multimedia.org/pool/main/d/debian-multimedia-keyring/debian-multimedia-keyring_2010.12.26_all.deb
    $ sudo dpkg -i debian-multimedia-keyring_2010.12.26_all.deb

Generate an entry in ``/etc/apt/sources.list.d``:

.. code-block:: bash

    $ sudo echo 'deb http://www.debian-multimedia.org/ squeeze main non-free' > /etc/apt/sources.list.d/debian-multimedia.list
    $ sudo apt-get update

Apt-file
--------

``Apt-file`` is a useful Debian package search tool:

.. code-block:: bash

    $ sudo apt-get install apt-file
    $ sudo apt-file update  

Re-run ``apt-file update`` whenever a new package archive is added to ``sources.list`` or ``sources.list.d``.

Kernel
------

If you are running Debian's ``i386`` target architecture on a machine with 4GB+ of memory download the ``pae kernel`` to make use of all that installed RAM:

.. code-block:: bash

    $ sudo apt-get remove linux-image-2.6-686
    $ sudo apt-get -t squeeze-backports install linux-image-686-pae

... and reboot.

Sound
-----

.. code-block:: bash

    $ aptitude show alsa-utils
    $ alsamixer 
    $ aplay /usr/share/sounds/alsa/Front_Center.wav
    $ alsactl store

Xorg
----

Discover your machine's video card:

.. code-block:: bash

    $ lspci -v | grep "VGA compatible controller"

*Using an open-source video driver*

.. code-block:: bash

    $ sudo apt-get install xorg

There are known issues with some Intel video cards - ``xserver-xorg-video-intel`` - and `KMS <http://wiki.debian.org/KernelModesetting>`_ and the default ``2.6.32 kernel`` in Debian ``stable``.

On my Intel-equipped `netbook <http://www.circuidipity.com/debian-linux-on-the-asus-eeepc-1001p.html>`_ netbook booting from GRUB or starting an X session can result in a black screen. A temporary fix is to edit the booting GRUB entry and add ``acpi=off`` to the kernel line.

A more permanent fix is to configure the *backlight* setting in ``/etc/default/grub``.

*Using the proprietary Nvidia driver*

See `Getting Nvidia and Xorg to play nice <http://www.circuidipity.com/getting-nvidia-and-xorg-to-play-nice.html>`_ ... though I think this information might be out-dated. I no longer use an NVIDIA-equipped machine.

Step 4 - Desktop
================

Select a window manager or a full-blown desktop environment such as XFCE, GNOME or KDE. There are a `few to choose from <http://www.gilesorr.com/wm/table.html>`_ ...

I like `XFCE <http://www.xfce.org/>`_. For a desktop environment complete with file manager, themes, graphical package and network managers:

.. code-block:: bash

    $ sudo apt-get install xfce4 gdm gksu libnotify-bin thunar ffmpegthumbnailer catfish synaptic update-notifier xscreensaver
    $ sudo apt-get install gtk2-engines gtk2-engines-murrine gnome-colors shiki-colors qt4-qtconfig
    $ sudo apt-get install ttf-mscorefonts-installer ttf-bitstream-vera ttf-liberation xfonts-terminus   
    $ sudo apt-get install network-manager network-manager-gnome

Applications
------------

My `applications checklist <http://www.circuidipity.com/applications-checklist-for-my-debian-linux-installs.html>`_.
