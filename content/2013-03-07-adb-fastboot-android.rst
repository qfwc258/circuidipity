======================================
Install ADB and Fastboot Android Tools
======================================

:date: 2013-03-07 01:23:00
:tags: android, debian, linux
:slug: adb-fastboot-android

Rooting my Nexus 7 tablet required the installation of *ADB* and *Fastboot*. ADB stands for *Android Debugging Bridge* and enables command-line control of Android devices connected to a host machine while Fastboot is used to flash software to Android via USB. Both tools are provided by the Android SDK.

This is how I setup Android tools on my laptop running Debian ``sid``.

0 Prepare devices
=================

Configure Android for `USB debugging <http://www.circuidipity.com/mtp.html>`_ and the host for `MTP <http://www.circuidipity.com/mtp.html>`_. This step confirms host is capable of detecting and mounting the Android device. Because things have changed in the latest Jelly Bean ...

1 Android SDK
=============

Debian has packages for ADB and Fastboot but they are slightly out-of-date even in ``sid``. Android 4.2.2 now requires the *RSA key fingerprint* of the attempting-to-connect host to be confirmed before allowing ADB to do its stuff. Which requires the very latest version of ADB to even *see* the RSA confirmation request (I kept running into ``device offline`` output from the Debian-supplied ADB).

Remove the Debian-supplied Android tools if they are installed ...

.. code-block:: bash

    $ sudo apt-get purge android-tools-adb android-tools-fastboot

... and download the latest `Android SDK <http://developer.android.com/sdk/index.html>`_ (for my 64-bit host I chose ``adt-bundle-linux-x86_64.zip``) and unpack. ADB and Fastboot are located in ``adt-bundle-linux-x86_64/sdk/platform-tools``.

If you are running 64-bit Debian then enable *multiarch* to use 32-bit ADB and Fastboot (yes they are 32-bit even though packed in the x86_64 bundle) and install their dependencies ...

.. code-block:: bash

    $ sudo dpkg --add-architecture i386
    $ sudo apt-get update ; apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386

2 ADB
=====

Navigate to platform-tools and start ADB ``./adb start-server``.

I connect my Nexus 7 to Debian and now see Android requesting confirmation of the RSA key fingerprint ...

.. code-block:: bash

    Allow USB debugging?

    The computer's RSA key fingerprint is:
    STRING

    [*] Always allow from this computer

    OK

ADB now detects my tablet ...

.. code-block:: bash

    $ adb devices
    List of devices attached
    STRING                device

3 Path
======

To permit running ADB and Fastboot outside of platform-tools I add the executables to $PATH by creating symbolic links in ``~/bin`` ...

.. code-block:: bash

    $ ln -s /path/to/adt-bundle-linux-x86_64/sdk/platform-tools/adb ~/bin/
    $ ln -s /path/to/adt-bundle-linux-x86_64/sdk/platform-tools/fastboot ~/bin

The groundwork is now in place to dive into some Android mods and rooting!

Happy hacking!
