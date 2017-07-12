===================================
Debian Linux on the Asus EEEPC 1001P
====================================

:date: 2010-06-10 01:23:00
:tags: debian, linux
:slug: debian-linux-on-the-asus-eeepc-1001p

I recently acquired an *Asus EEEPC 1001P-MU17* netbook and replaced the marginal crippled operating system it included with `Debian GNU/Linux <http://www.circuidipity.com/install-debian-linux-squeeze.html>`_.

Let's go!
=========

There were a few hiccups during the install... but with the replacement of Debian's default 2.6.32 kernel with a more recent release (currently running kernel 2.6.37) most of the 1001P's hardware is supported by default. Adding a few configuration tweaks makes this one nifty little device!

0. Start
--------

Asus 1001P-MU17 Hardware specifications
```````````````````````````````````````

* Processor: Intel Atom N450
* Chipset: Intel NM10<
* Memory: 1GB DDR2-667
* Graphics: Intel GMA 3150 (kernel driver: i915)
* Display: 10.1" LED Matte 1024x600
* Hard Drive: 160GB 5400RPM Western Digital WD1600BEVT-2
* Ethernet: Atheros AR8132 (kernel driver: atl1c)
* Wireless: Atheros AR2427 802.11g (kernel driver: ath9k)
* Audio: Realtek AL269 2-Channel HD Audio
* Webcam: 0.3MP UVC Camera (kernel driver: uvcvideo)
* Battery: 6-Cell, 4400mAh, 48Wh (~7 hours runtime)
* Ports: 3 x USB 2.0, VGA, SD Reader, 100Mb Ethernet, Microphone/Headphone Jacks

Device status
`````````````

* Graphics: Works
* Ethernet: Works
* Wireless: Works
* Audio: Works
* Webcam: Works
* SD reader: Works
* Touchpad: Works

Function keys
`````````````

* Fn+F1 (Suspend-to-RAM): Works
* Fn+F2 (Toggle wireless): Not used
* Fn+F3: Not used
* Fn+F4: Not used
* Fn+F5 (Brightness down): Works
* Fn+F6 (Brightness up): Works
* Fn+F7: Not used
* Fn+F8: Use `xrandr <http://www.circuidipity.com/big-screen-little-screen-virtual-screen-dual-display-configuration-using-xrandr.html>`_ in the terminal
* Fn+F9: Not used
* Fn+F10 (Volume mute): Works
* Fn+F11 (Volume down): Works
* Fn+F12 (Volume up): Works

1. Install
----------

My `Debian install notes <http://www.circuidipity.com/install-debian-linux-squeeze.html>`_. Specific details concerning the Asus 1001P are noted below.

1.1 Configure BIOS and boot Debian installer
````````````````````````````````````````````

Power up and enter the Asus BIOS by pressing the ``F2`` key. Configure for a USB install:

* under ``Advanced`` ... ensure that both onboard camera and WLAN are ``Enabled``
* under ``Boot`` ... ensure that 1st boot device is set to ``Removable Device``
* under ``Boot`` ... ensure that boot booster is ``Disabled``

`Prepare the Debian installer <http://www.circuidipity.com/install-debian-linux-squeeze.html>`_ on a USB stick, attach, and reboot. At the BIOS screen hit ``Esc`` and select USB as boot device.

2. Configuration
----------------

2.1 Ethernet
````````````

Auto-detection probing of the ethernet interface during the install can result in device disappearing from the system and network configuration to fail (*Update:* Appears problem has been resolved with the stable release of Debian ``squeeze``). If the ethernet device was knocked out during installation:

* ensure that ``/etc/network/interfaces`` contains no hotplug entry for ``eth0`` or ``wlan0``
* shutdown netbook and remove the power cord
* remove battery and let sit for a minute or so
* restore power to netbook and startup
* ``lspci -v | grep net`` reveals the ethernet device (Atheros Communications AR8132 Fast Ethernet)
* bring up the interface... ``ifconfig eth0 up`` and ``dhclient eth0``

2.2 Wireless
````````````

Works "out-of-box". Interface is identified as ``wlan0``.

2.3 EEEPC
`````````

Install the ``eeepc-acpi-scripts`` to enable the function keys and the ability to suspend-to-RAM (sleep) ...

.. code-block:: bash

    $ sudo apt-get install eeepc-acpi-scripts

2.4 Power management
````````````````````

.. code-block:: bash

    $ sudo apt-get install acpid acpi cpufrequtils pm-utils

Verify ``acpi-cpufreq`` module is loaded... otherwise ``sudo modprobe acpi-cpufreq``.

Output detailed information about the CPU(s) by running ``cpufreq-info``.

Settings are in ``/sys/devices/system/cpu/cpu0/cpufreq``. CPU speed can be monitored in real-time by running ...

.. code-block:: bash

    $ watch grep \"cpu MHz\" /proc/cpuinfo

Default scaling governor is ``ondemand``.

2.5 Screen brightness
`````````````````````

Post-install the display brightness is extremely low and the assigned function keys for adjusting the brightness level cause the setting to jump all over the place. This can be fixed by editing ``/etc/default/grub`` and modifying ``GRUB_CMDLINE_LINUX_DEFAULT`` ...

.. code-block:: bash

    GRUB_CMDLINE_LINUX_DEFAULT="quiet acpi_osi=Linux acpi_backlight=vendor"

Save your changes and run ``sudo update-grub2``. Reboot... login... and run ...

.. code-block:: bash

    $ sudo `echo 15 > /sys/class/backlight/eeepc/brightness`

2.6 Touchpad
````````````

By default the touchpad is limited to finger-tap=left-mouse-click. *HAL* and *fdi* files were previously used to enable more mouse-click and scrolling functions but their use is now deprecated... *udev* is the way to go now.

Determine type of touchpad used in the 1001P ...

.. code-block:: bash

    $ egrep -i 'synap|alps|etps' /proc/bus/input/devices
    N: Name="SynPS/2 Synaptics TouchPad"

Use ``xinput`` to determine the properties of the touchpad and add new functions ...

.. code-block:: bash

    $ sudo apt-get install xinput
    $ xinput --list | grep Synaptic     # determine ``DEVICE_ID`` of the touchpad ... on the 1001P its ``id=13``)
    $ xinput --list-props 13

Create a shell script using xinput to configure the touchpad for left-middle-right mouse clicks with finger taps and two-finger scrolling, save it in ``~/bin`` and source it to run at login. On my 1001P running Fluxbox window manager I add the line ``touchpad_config &`` to ``~/.fluxbox/startup``.

2.7 Suspend-to-RAM
``````````````````

Using the ``eeepc-acpi-scripts`` and key combo ``Fn + F1`` to put the netbook to sleep "just works".

2.8 Microphone
``````````````

Muted by default. Need to enable capture in ``alsamixer``.

2.9 Hard drive management
`````````````````````````

I noticed a frequent clicking noise from the drive heads on my netbook. Digging online reveals discussion about over-aggressive power management settings on hard drives that rapidly mount/unmount/remount and gradually wear out the drive. Feedback suggests that laptop drives are good for roughly ~600000 *load_cycles*.

To check the drive and alter management settings ...

.. code-block:: bash

    $ sudo apt-get install smartmontools hdparm
    $ sudo smartctl -a /dev/sda | egrep -i 'Power_On_Hours|Load_Cycle_Count'

In my situation I felt ``Load_Cycle_Count`` was increasing too rapidly and I found the *click-click-click* of the drive every few seconds a nuisance. I use ``hdparm`` to set powersaving mode to less aggressive tactics... which eliminated the clicking ``hdparm -B 254 /dev/sda``.

To make the change permanent edit ``/etc/hdparm.conf`` by adding to the end of the file ...

.. code-block:: bash

    command_line {
        hdparm -q -B 254 /dev/sda
