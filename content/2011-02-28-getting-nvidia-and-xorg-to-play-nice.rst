====================================
Getting Nvidia and xorg to play nice
====================================

:date: 2011-02-28 01:23:00
:tags: graphics, debian, linux
:slug: getting-nvidia-and-xorg-to-play-nice

Configure a Nvidia graphics card for use in Debian.

*Nvidia* provides a driver on their website that can be downloaded and installed directly on a Linux system. But it is not a recommended course of action for a Debian user.

A better way is to use an open-source driver (2-D graphics) ... and if 3-D is the name of your game the *best* way is either downloading the Debian pre-built Nvidia package or create one using ``module-assistant``. Going down the package route permits the Nvidia driver to be properly tracked and managed by the awesome Debian package tools.

Step 0 - Start
==============

Shutdown the X server if currently running ... either by exiting the current X session and returning to the console or - if running a graphical login manager such as ``gdm`` or ``kdm`` - exiting to the login screen and hitting CTRL+ALT+F1 to jump back to a console.

Stop the running X session ... ``sudo /etc/init.d/gdm stop``.

Determine which Nvidia graphics card is installed
-------------------------------------------------

.. code-block:: bash

    $ lspci -v | grep "VGA compatible controller: nvidia"

On the motherboard of my primary workstation I have an embedded Nvidia chipset with dual VGA + DVI ports:

.. code-block:: bash

    $ lspci -v | grep "VGA compatible controller: nvidia"
    00:05.0 VGA compatible controller: nVidia Corporation C51PV [GeForce 6150] (rev a2) (prog-if 00 [VGA controller])

Step 1 - Install driver
=======================

Using the open-source nouveau driver
------------------------------------

For 2-D graphics the ``vesa`` or ``nv`` or ``nouveau`` drivers will suffice (3-D graphics require the proprietary driver).

To install the <strong>nouveau</strong> driver ...

.. code-block:: bash

    $ sudo apt-get install xorg xserver-xorg-video-vesa xserver-xorg-video-nouveau xbindkeys mesa-utils

That's it. X should pick it up automatically. See below to confirm that the correct driver is loaded or switch to another open-source driver (``vesa`` can be a good fallback if things go awry).

Using the proprietary Nvidia driver
-----------------------------------

Few different ways this can go ...

* use Debian pre-built package
  
* run module-assistant to build and install our own package (*my choice*)

* perform a manual build for either a custom or Debian-packaged kernel

These ``nvidia-{kernel,glx}`` packages only support GeForce 6xxx and higher GPUs. Check out the *nvidia legacy* packages for older cards and the list of `legacy drivers <http://www.nvidia.com/object/IO_32667.html>`_ .

Pre-built
---------

If running the default kernel in Debian ``squeeze`` or ``wheezy`` ... there is a Debian package available of a pre-built Nvidia module (`supported chipsets <http://us.download.nvidia.com/XFree86/Linux-x86/195.36.24/README/supportedchips.html>`_) ...

.. code-block:: bash

    $ sudo apt-get install xorg xserver-xorg-video-vesa xserver-xorg-video-nouveau xbindkeys mesa-utils
    $ sudo apt-get install nvidia-kernel-$(uname -r)
    $ sudo apt-get install nvidia-glx

See below for configuring X to use the proprietary Nvidia driver vs an open-source driver.

module-assistant
----------------

.. code-block::  bash

    $ sudo apt-get install xorg xbindkeys mesa-utils module-assistant nvidia-kernel-common build-essential
    $ sudo m-a prepare
    $ sudo m-a clean nvidia-kernel-source
    $ m-a get nvidia-kernel-source
    $ sudo m-a build nvidia-kernel-source
    $ sudo m-a install nvidia-kernel-source
    $ sudo apt-get install nvidia-glx

See below for configuring X to use the proprietary Nvidia driver vs an open-source driver.

When upgrading to a newer kernel ... the Nvidia kernel module will need to be rebuilt to match the new kernel.

Manual build
------------

Never had a need to do this myself. But here are the `instructions <http://wiki.debian.org/NvidiaGraphicsDrivers#Buildmanually.2Cwithacustomkernel>`_ in the Debian wiki.

Step 2 - Xorg.conf
==================

An X configuration file is no longer included by default in Debian ``squeeze``. Create a sample file by running ... ``sudo Xorg -configure``.

Open the new ``xorg.conf.new`` file in a text editor. Under ``Module`` confirm that it contains the line ``Load "glx"``.

Remove/comment out any lines that refer to the ``dri`` or ``GLCore`` modules.

Under ``Device`` change the driver - normally ``nouveau`` or ``nv`` or ``vesa`` - to ``nvidia`` ... ``Driver "nvidia"``.

Sample configuration from my own system ...

.. code-block:: bash

    Section "Module"
        Load  "dbe"
        #Load  "dri"
        Load  "extmod"
        Load  "record"
        #Load  "dri2"
        Load  "glx"
    EndSection

    Section "Device"
        Identifier  "Card0"
        #Driver      "nouveau"
        Driver      "nvidia"
        VendorName  "nVidia Corporation"
        BoardName   "C51PV [GeForce 6150]"
        BusID       "PCI:0:5:0"
    EndSection

Move the modified file to its default name and location ...

.. code-block:: bash

    $ sudo cp /root/xorg.conf.new /etc/X11/xorg.conf

Any user that wants to run 3-D code must belong to the ``video`` group. Should already be pre-configured ... but if not ``sudo adduser USERNAME video``.

Step 3 - Run
============

Logged in as regular user ... start the X server ``startx`` or restart ``sudo /etc/init.d/gdm start`` if using a graphical login manager. I needed to restart my system to get the nvidia driver to work properly.
                        
View what video driver is in use ...

.. code-block:: bash

    $ grep -B2 'Module class: X.Org Video Driver' /var/log/Xorg.0.log

You should see ...

.. code-block:: bash

    $ grep -B2 'Module class: X.Org Video Driver' /var/log/Xorg.0.log
    (II) Module nvidia: vendor="NVIDIA Corporation"
            compiled for 4.0.2, module version = 1.0.0
            Module class: X.Org Video Driver

Confirm that video acceleration is actually working ...

.. code-block:: bash

    $ glxinfo | grep rendering       
    direct rendering: Yes

For a dual-display configuration - use monitors of different resolutions and combine them into one desktop - give `Twinview <http://www.circuidipity.com/twinview.html>`_ a chance.

Good to go!
