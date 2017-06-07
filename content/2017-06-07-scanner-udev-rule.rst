=================
Scanner udev rule
=================

:date: 2017-06-07 14:56:00
:slug: scanner-udev-rule
:tags: scanner, network, shell, linux

**[ Problem ]** Client error trying to scan to a **Brother MFC-J450DW** configured as a `network scanner <http://www.circuidipity.com/network-printer-scanner.html>`_ ...

.. code-block:: bash

    scanimage: open of device net:192.168.... failed: Invalid argument

Scanner **does** accept jobs from the server. User belongs to the ``lp``, ``lpadmin``, and ``scanner`` groups.

**[ Fix! ]** Set world-writable permission on the scanner bus device ...

.. code-block:: bash

    $ lsusb
    Bus 001 Device 006: ID 04f9:02fa Brother Industries, Ltd
    $ ls /dev/bus/usb/001/006
    crw-rw-r-- 1 root lp 189, 5 Jun  6 17:24 /dev/bus/usb/001/006
    $ sudo chmod 666 /dev/bus/usb/001/006
    $ ls /dev/bus/usb/001/006
    crw-rw-rw- 1 root lp 189, 5 Jun  6 17:24 /dev/bus/usb/001/006

... and it works. But when device is unplugged and re-plugged back in again it will be created with the old permissions.

A more enduring fix is to create a **udev rule** with desired permissions. First, retrieve the ``idVendor`` and ``idDevice`` of the scanner ...

.. code-block:: bash

    $ lsusb | grep Brother
    Bus 001 Device 006: ID 04f9:02fa Brother Industries, Ltd

... then create ``/lib/udev/rules.d/61-scanner.rules`` for **04f9:02fa** with desired permissions ...

.. code-block:: bash

    SUBSYSTEMS=="usb", ATTRS{idVendor}=="04f9", ATTRS{idProduct}=="02fa", GROUP="lp", MODE="0666"

Reload rules ...

.. code-block:: bash

    $ sudo udevadm control --reload 

... or simply disconnect and re-connect scanner to test ...

.. code-block:: bash

    $ ls /dev/bus/usb/001/007
    crw-rw-rw- 1 root lp 189, 6 Jun  6 18:45 /dev/bus/usb/001/007

Happy hacking!
