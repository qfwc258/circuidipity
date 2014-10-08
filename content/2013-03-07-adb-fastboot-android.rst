======================================
Install ADB and Fastboot Android Tools
======================================

:date: 2013-03-07 01:23:00
:tags: android, debian, linux
:slug: adb-fastboot-android
:modified: 2014-10-08 17:31:00

Rooting my **Nexus 7** required the installation of **ADB** and **Fastboot**. ADB stands for *Android Debugging Bridge* and enables command-line control of Android devices connected to a host machine while Fastboot is used to flash software to Android via USB. Both tools are provided by the **Android SDK**.

To setup Android tools under Debian:
====================================

0. Prepare devices
------------------

Configure Android for `USB debugging <http://www.circuidipity.com/mtp.html>`_ and the host for `MTP <http://www.circuidipity.com/mtp.html>`_. This step confirms host is capable of detecting and mounting the Android device.

1. Android SDK
--------------

Install packages:

.. code-block:: bash

    $ sudo apt-get install android-tools-adb android-tools-fastboot

2. ADB
------

Start ADB:

.. code-block:: bash

    $ adb start-server

Android 4.2.2 now requires the **RSA key fingerprint** of the connecting host to be confirmed before allowing ADB to do its stuff. Coonnect the tablet and Android prompts for confirmation:

.. code-block:: bash

    Allow USB debugging?

    The computer's RSA key fingerprint is:
    STRING

    [*] Always allow from this computer

    OK

ADB now detects my tablet:

.. code-block:: bash

    $ adb devices
    List of devices attached
    STRING                device

Happy hacking!
