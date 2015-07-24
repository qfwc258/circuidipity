===========================================================
Print copy scan using the Epson NX215 all-in-one with Linux
===========================================================

:date: 2010-08-12 01:23:00
:tags: printer, scanner, debian, linux
:slug: print-copy-scan-using-the-epson-nx215-all-in-one-with-debian

While browsing through my local cluster of computer stores I came across the *Epson Stylus NX215 All-in-one Printer* which I purchased on sale for $40.

Now someone who prints a *lot* probably should be looking at laser printers. But the higher operating costs of inkjets are not really a deterrent for my modest printing needs when the trade-off is a good sale price on a device that includes a scanner/copier in a single space-saving package. Epson is one of the better-supported brands in Linux and the NX215 works well... *after* bouncing over a few speedbumps to printshop glory.

This is how I configured the printer to play nice with my Debian host machine ...

Step 0 - Download
=================

Unpack the Epson, load it up with ink and paper, then switch the printer back off. Do not connect the device via USB cable just yet. On the host computer running Debian:

.. code:: bash

    $ sudo apt-get install cups lsb libltdl7 sane-utils xsane

Download printer and scanner packages from `Avasys <http://avasys.jp/eng/linux_driver/>`_ . On their Linux driver page... select your printer type and model. For the NX215 all-in-one I download:

* Epson-Stylus_NX215-pipslite-en.ppd

* pipslite_VERSION.deb

* iscan-data_VERSION_all.deb

* iscan_VERSION.deb

Step 1 - Install print drivers
==============================

Attempting to install the print driver at this point will generate a complaint about a missing ``libltdl3`` dependency and will result in a broken package. In Debian ``stable`` the ``libltdl3`` library has been superseded by ``libltdl7`` and the Avasys package is hardcoded to look for the former. A way around this is to create a symlink before installing the drivers:

.. code-block:: bash

    $ sudo ln -s /usr/lib/libltdl.so.7 /usr/lib/libltdl.so.3

Now install the *Photo Image Print System Lite* package:

.. code-block:: bash

    $ sudo dpkg --ignore-depends=libltdl3 -i pipslite_VERSION.deb

Copy the downloaded *PostScript Printer Description (PPD)* file to ``/etc/cups/ppd``:

.. code-block:: bash

    $ sudo cp Epson-Stylus_NX215-pipslite-en.ppd /etc/cups/ppd/
    $ sudo chmod 644 /etc/cups/ppd/Epson-Stylus_NX215-pipslite-en.ppd
    $ sudo /etc/init.d/cups restart

Step 2 - Configure CUPS
=======================

Now connect the NX215 via USB cable to the computer and switch on the printer. Running ``dmesg`` on my desktop outputs:

.. code-block:: bash

    $ dmesg
    [418676.456021] usb 1-1: new high speed USB device using ehci_hcd and address 8
    [418676.596366] usb 1-1: New USB device found, idVendor=04b8, idProduct=084f
    [418676.596370] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
    [418676.596373] usb 1-1: Product: USB2.0 MFP(Hi-Speed)
    [418676.596376] usb 1-1: Manufacturer: EPSON
    [418676.596378] usb 1-1: SerialNumber: 4C39544B3033343183
    [418676.596487] usb 1-1: configuration #1 chosen from 1 choice
    [418676.604068] usblp0: USB Bidirectional printer dev 8 if 1 alt 0 proto 2 vid 0x04B8 pid 0x084F
    [418676.605087] scsi11 : SCSI emulation for USB Mass Storage devices
    [418676.605194] usb-storage: device found at 8
    [418676.605196] usb-storage: waiting for device to settle before scanning
    [418681.604309] usb-storage: device scan complete
    [418681.606512] scsi 11:0:0:0: Direct-Access     EPSON    Stylus Storage   1.00 PQ: 0 ANSI: 2
    [418681.607084] sd 11:0:0:0: Attached scsi generic sg6 type 0
    [418681.613113] sd 11:0:0:0: [sdf] Attached SCSI removable disk

Kernel driver *usb-storage* is detecting the printer SD slot. It can be used to print photos directly from a memory card without using a computer. I have not yet tried this feature (and with the price of ink I doubt I will make use of it).

Navigate with a web browser to http://localhost:631 and use the *Common Unix Printing System (CUPS)* to add the printer. CUPS detects the NX215 as a *Epson Stylus NX210* but despite the small difference in model number it does not appear to make a difference in use. During the CUPS configuration select the PPD installed in ``/etc/cups/ppd``.

Step 3 - Copier
===============

One feature of the NX215 is the ability to act as a photocopier and make a duplicate of a document with the host computer powered off. Nothing to configure here... it works as expected.

Step 4 - Scanner
================

``Xsane`` is a popular Linux scanner tool with many options. For a simple front-end to xsane that is useful for basic scanning needs I installed the Avasys-sponsored ``iscan`` package:

.. code-block:: bash

    $ sudo dpkg -i iscan-data_VERSION.deb
    $ sudo dpkg --ignore-depends=libltdl3 -i iscan_VERSION.deb

Before you can scan as a non-privileged user... that user account needs to be added to the ``lp`` and ``scanner`` groups:

.. code-block:: bash

    $ sudo adduser USERNAME lp
    $ sudo adduser USERNAME scanner

Log out and back in again to update the user group list. Test the configuration by first running ``xsane``. If ``xsane`` outputs an error message:

.. code-block:: bash

    Failed to open device 'epkowa:usb:001:008':
    Access to resource has been denied.

... confirm that the affected user is a member of the ``lp|scanner`` groups.

Step 5 - Modify dpkg
====================

Since I earlier installed ``pipslite`` and ``iscan`` by ignoring the ``libltdl3`` dependency... the Debian package management tools will complain about broken packages every time I try to install something new. To fix this (thanks `Dale <http://danson.grafidog.com/2010/02/epson-nx510-scanner-and-ubuntu-904.html>`_)... start by making a backup of ``/var/lib/dpkg/status`` ...

.. code-block:: bash

    $ sudo cp /var/lib/dpkg/status /var/lib/dpkg/status.bak

Open a text editor and modify the entries for the ``pipslite`` and ``iscan`` packages by removing the reference to ``libltdl3``. After making this change Debian will no longer treat these packages as broken or try to remove them.

Done! Good printer/scanner at a good price. I like it!
