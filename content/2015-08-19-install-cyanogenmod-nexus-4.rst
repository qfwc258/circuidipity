==============================
Install CyanogenMod on Nexus 4
==============================

:date: 2015-08-19 00:28:00
:slug: install-cyanogenmod-nexus-4
:tags: android, linux
:modified: 2015-08-21 12:26:00

Replace stock Android with CyanogenMod on the Nexus 4 using Linux.

Let's go!
=========

Thanks to a **very generous friend** who upgraded to a new smartphone I now have her old Google Nexus 4. I have dabbled with alternative Android firmwares in the past, and was inspired to give CyaonogenMod a go on this phone after reading `Android without the mothership [LWN.net] <https://lwn.net/Articles/602521/>`_.

0. Download
===========

I install CyanogenMod from a host running Debian. Download ``adb`` and ``fastboot`` install tools:

.. code-block:: bash

    $ sudo apt-get install android-tools-adb android-tools-fastboot                      
    
Nexus 4 device is code-named ``mako``. Download:
                                                                                 
* a recovery image (TWRP) - https://twrp.me/devices/lgnexus4.html (`latest is 2.8.7.0 <https://dl.twrp.me/mako/>`_ as of 7/29)
* the Cyanogenmod ROM nightly build `specific to this device <https://download.cyanogenmod.org/?device=mako&type=>`_               
                                                                                     
1. Developer Options
====================
                                                                 
On the Nexus I enable developer options by navigating to ``Settings->About phone``, click to open and make +7 taps on **Build** number. Displays ``You are now a developer``. Return to settings and ``Developer Options`` is now visible. Click to open and activate ``USB debugging``.
                                                                                     
2. Connect device
=================
                                                                    
Connect phone to host via USB:

.. code-block:: bash
                                                                                     
    $ lsusb | grep -i nexus                                                              
    Bus 001 Device 003: ID 18d1:4ee2 Google Inc. Nexus 4 (debug)                         
    $ adb devices -l                                                                     
    * daemon not running. starting it now on port 5037 *                                 
    * daemon started successfully *                                                      
    List of devices attached                                                             
    [...]       offline usb:1-12

Confirm ``Allow usb debugging`` in pop-up on the phone. Re-run:

.. code-block:: bash

    $ adb devices -l                                                                     
    List of devices attached                                                             
    [...]       device usb:1-12 product:occam model:Nexus_4 device:mako  
                                                                                     
3. Unlock bootloader
====================
                                                                 
Boot the device into **fastboot** mode:

.. code-block:: bash
                                                
    $ adb reboot bootloader                                                              
                                                                                     
Once device is in fastboot mode, verify host sees device and unlock:

.. code-block:: bash

    $ fastboot devices -l                                                                
    [...]       fastboot usb:1-12                                             
    $ fastboot oem unlock                                                                
                                                                                     
4. Install TWRP
===============
                                                                      
While in fastboot mode flash the TWRP recovery image:

.. code-block:: bash

    $ fastboot flash recovery twrp-VERSION-mako.img                                      
    sending 'recovery' (9028 KB)...                                                      
    OKAY [  0.287s]                                                                      
    writing 'recovery'...                                                                
    OKAY [  0.501s]                                                                      
    finished. total time: 0.787s                                                         
                                                                                     
Reboot the bootloader:

.. code-block:: bash
                                                               
    $ fastboot reboot-bootloader                                                         
    rebooting into bootloader...                                                         
    OKAY [  0.001s]                                                                      
    finished. total time: 0.001s                                                         
                                                                                     
Use the device volume keys to navigate to **Recovery** mode and power key to select. TWRP recovery starts. Tap **Wipe** and swipe to start **Factory Reset**.

5. Install CyanogenMod
======================
                                                               
Copy the CyanogenMod distribution zip file into device:

.. code-block:: bash
                                               
    $ adb push cm-12.1-VERSION-NIGHTLY-mako.zip /sdcard                            
    3753 KB/s (263171832 bytes in 68.465s)                                          
                                                                                
Return to TWRP main menu and tap **Install**. Search in file system for the freshly-installed zip and tap to select. Tap checkbox Zip file signature verification and swipe to confirm flash. The message ``Successfull`` should appear. Tap ``Reboot System`` and device boots into CyanogenMod. Yes!

6. F-Droid
==========

As a replacement for the non-free Google Play Store app I use the `F-Droid <https://f-droid.org/about/>`_ free software app repository:

* on the phone navigate to ``Settings->Security->Unknown sources`` and tap to allow 

* `download the F-Droid app <https://f-droid.org/FDroid.apk>`_ to host and install the ``apk`` to phone using `adb <https://developer.android.com/tools/help/adb.html#move>`_

.. code-block:: bash                                                               
                                                                                   
    $ adb install /path/to/FDroid.apk                                              
    4373 KB/s (3942326 bytes in 0.880s)                                            
            pkg: /data/local/tmp/FDroid.apk                                        
    Success                                                                        

Two apps I like and use daily are `fbreader <https://f-droid.org/repository/browse/?fdfilter=fbreader&fdid=org.geometerplus.zlibrary.ui.android>`_ for ebooks and `AntennaPod <https://f-droid.org/repository/browse/?fdfilter=podcast&fdid=de.danoeh.antennapod>`_ for downloading and listening to podcasts. 

Happy hacking!
