=================================
Restore stock Android for Nexus 7
=================================

:date: 2014-10-08 17:43:00
:slug: 20141008
:tags: android, linux

**Device:** Nexus 7 2012 (model) -> grouper (device) -> nakasi (device-appropriate Google ROMs)                   

After experimenting a bit with `CyanogenMod <http://www.cyanogenmod.org/>`_, my first attempt to restore stock Android to my tablet hit a snag when the flashing procedure stumbled over the included bootloader file in Google's tarball: ``bootloader-grouper-4.23.img`` packaged in the v4.4.4 ``KTU84P`` factory image. `The solution <http://forum.xda-developers.com/showthread.php?t=2417097&page=7>`_ was to download a bootloader extracted from an earlier image and swap out the buggy version in the current image.

To successfully flash a factory image under Linux:
==================================================

0. Backup
---------

This procedure **erases all data** on the tablet. Google settings will be restored during post-install setup but anything of importance stored in device memory will require backup.

1. Tools
--------

Verify that `MTP <http://www.circuidipity.com/mtp.html>`_ and `adb + fastboot <http://www.circuidipity.com/adb-fastboot-android.html>`_ are installed.

2. Image
--------

`Download the latest device-specific factory image <https://developers.google.com/android/nexus/images>`_ and unpack the tarball. Factory images for my Nexus 7 are code-named **nakasi**.

3. Replace bootloader
---------------------

Work around the buggy bootloader by `downloading and replacing it with this alternate file <http://forum.xda-developers.com/showpost.php?p=44903559&postcount=1>`_.

4. Fastboot
-----------

Connect the tablet. Start adb and restart the tablet in fastboot mode:

.. code-block:: bash                                            
                                                                                    
    $ adb start-server                                                                  
    $ adb reboot bootloader                                                           
                                                                                    
5. Flash image
--------------

Navigate to the factory image folder and run:

.. code-block:: bash

    $ ./flash-all.sh

After flashing is complete the device will reboot into its default factory state. 

Happy hacking!

Sources: `Factory Images for Nexus Devices <https://developers.google.com/android/nexus/images>`_ (developers.google.com), `Factory image bootloader problem <http://forum.xda-developers.com/showthread.php?t=2417097>`_ (forum.xda-developers.com)
