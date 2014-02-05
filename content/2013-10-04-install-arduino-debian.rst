=========================
Install Arduino on Debian
=========================

:tags: arduino, electronics, debian, linux
:slug: install-arduino-debian

I have been exploring the *Arduino Uno* microcontroller board this week and it is proving a fun entry point to hardware hacking and programming.

Installing the `Arduino development environment <http://playground.arduino.cc/Learning/Linux>`_ on Debian or Ubuntu involves ... 0) adding my USER to the ``dialout`` group (and logging out and back in again for the change to take effect); 1) install package dependencies and; 2) download the Debian packages for Arduino for manual installation ...

.. code-block:: highlight bash

    $ sudo adduser USER dialout
    $ sudo apt-get update && sudo apt-get install openjdk-7-jre avr-libc avrdude binutils-avr extra-xdg-menus gcc-avr libftdi1 libjna-java librxtx-java

Versions of the Arduino software packaged for official Ubuntu and Debian releases are often outdated. Download the latest packages for `arduino-core <http://packages.debian.org/sid/arduino-core>`_ and `arduino <http://packages.debian.org/sid/arduino>`_ from Debian's ``unstable`` branch and install manually ...

.. code-block:: bash

    $ sudo dpkg -i arduino-core_VERSION_all.deb
    $ sudo dpkg -i arduino_VERSION_all.deb

Connect the Uno to a computer via USB, open the Arduino IDE and confirm that the port setting is properly set to ``Tools->Serial Port->/dev/ttyACM0``. Ready to go!
