==============
Minimal Ubuntu
==============

:date: 2014-07-07 01:23:00
:tags: ubuntu, linux, server
:slug: ubuntu-trusty-install
:modified: 2016-08-14 19:57:00

.. image:: images/screenshot/ubuntuInstall/xerus.png
    :alt: Xerus
    :align: right
    :width: 200px
    :height: 200px

**Ubuntu 16.04 "Xenial Xerus"** is the latest `Long Term Support (LTS) <https://wiki.ubuntu.com/Releases>`_ release of the popular Linux operating system. I use Ubuntu's `minimal install image <https://help.ubuntu.com/community/Installation/MinimalCD>`_ to create a **console-only base configuration** that can be customized for various tasks and `alternate desktops <http://www.circuidipity.com/i3-tiling-window-manager.html>`_.

Let's go!
=========

Below is a visual walk-through of a sample Ubuntu setup that makes use of an entire storage device divided into 3 partitions: an unencrypted ``root`` partition, and encrypted ``swap`` + ``home``. 

0. Prepare install media
------------------------

Download the `64-bit xenial minimal installer <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/netboot/mini.iso>`_ (`32-bit <http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-i386/current/images/netboot/mini.iso>`_ for older machines) and burn to CD or `flash the image <https://help.ubuntu.com/community/Installation/FromUSBStick>`_ to a USB stick. [1]_ Using the minimal console installer vs. the graphical installer provides more options during setup. [2]_

Minimal installer (requires network connection) downloads all the latest packages during setup.

1. Launch
---------

.. image:: images/screenshot/ubuntuInstall/100.png
    :align: center
    :alt: Install
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/101.png
    :align: center
    :alt: Select Language
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/102.png
    :alt: Select Location
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/103.png
    :alt: Configure Keyboard
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/104.png
    :alt: Configure Keyboard
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/105.png
    :alt: Configure Keyboard
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/106.png
    :alt: Hostname
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/107.png
    :alt: Mirror Country
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/108.png
    :alt: Mirror archive
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/109.png
    :alt: Proxy
    :align: center
    :width: 800px
    :height: 600px

Contents of the installer are now loaded into memory and the USB stick can safely be removed. [3]_ 

.. image:: images/screenshot/ubuntuInstall/110.png
    :alt: Full Name
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/111.png
    :alt: Username
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/112.png
    :alt: User password
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/113.png
    :alt: Verify password
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/114.png
    :alt: Encrypt home
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/115.png
    :alt: Configure clock
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/116.png
    :alt: Select time zone
    :align: center
    :width: 800px
    :height: 600px

2. Partitions
-------------

In the example below I create 3 partitions [4]_ on the disk:

* sda1 is a 24GB ``root`` partition 
* sda2 is a 2GB LUKS encrypted ``swap`` partition using a **random key**
* sda3 uses the remaining space as a LUKS encrypted ``home`` partition using a **passphrase**

.. image:: images/screenshot/ubuntuInstall/200.png
    :alt: Partitioning method
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/201.png
    :alt: Partition disks
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/202.png
    :alt: Partition table
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/203.png
    :alt: Free space
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/204.png
    :alt: New Partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/205.png
    :alt: Partition size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/206.png
    :alt: Primary partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/207.png
    :alt: Beginning
    :align: center
    :width: 800px
    :height: 600px

Setting ``Mount options: relatime`` decreases write operations and boosts drive speed ...

.. image:: images/screenshot/ubuntuInstall/208.png
    :alt: Mount options
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/209.png
    :alt: Mount relatime
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/210.png
    :alt: Done with partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/211.png
    :alt: Free space
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/204.png
    :alt: New partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/213.png
    :alt: Partition size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/206.png
    :alt: Primary partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/207.png
    :alt: Beginning
    :align: center
    :width: 800px
    :height: 600px
    
.. image:: images/screenshot/ubuntuInstall/215.png
    :alt: Use as
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/216.png
    :alt: Encrypt volume
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/217.png
    :alt: Encrypt key
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/218.png
    :alt: Random key
    :align: center
    :width: 800px
    :height: 600px

If the hard disk has not been securely wiped prior to installing Ubuntu (using a utility like `DBAN <http://www.circuidipity.com/multi-boot-usb.html>`_) you may want to configure ``Erase data: yes``. Note, however, that depending on the size of the disk this operation can last several hours ...

.. image:: images/screenshot/ubuntuInstall/219.png
    :alt: Done with partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/220.png
    :alt: Free space
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/204.png
    :alt: New partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/222.png
    :alt: Partition size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/206.png
    :alt: Primary partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/224.png
    :alt: Use as
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/216.png
    :alt: Encrypt volume
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/216-1.png
    :alt: Encrypt key
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/216-2.png
    :alt: Passphrase
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/226.png
    :alt: Done with partition
    :align: center
    :width: 800px
    :height: 600px
 
.. image:: images/screenshot/ubuntuInstall/227.png
    :alt: Configure encrypted volumes
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/228.png
    :alt: Write changes
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/229.png
    :alt: Create encrypted volumes
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/230.png
    :alt: Devices to encrypt
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/231.png
    :alt: Finish
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/232.png
    :alt: Encrypt passphrase
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/233.png
    :alt: Verify passphrase
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/234.png
    :alt: Configure encrypt volume
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/235.png
    :alt: Mount point
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/236.png
    :alt: Mount home
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/237.png
    :alt: Mount options
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/209.png
    :alt: Mount relatime
    :align: center
    :width: 800px
    :height: 600px

**Reserved blocks** can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large, **non-root partitions** extra space can be gained by reducing the ``5%`` default reserve set by Ubuntu to ``1%`` ...

.. image:: images/screenshot/ubuntuInstall/239.png
    :alt: Reserved blocks
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/240.png
    :alt: Percent reserved
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/241.png
    :alt: Done with partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/242.png
    :alt: Finish
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/243.png
    :alt: Write changes
    :align: center
    :width: 800px
    :height: 600px

3. Install packages and finish up
---------------------------------

.. image:: images/screenshot/ubuntuInstall/300.png
    :alt: No automatic updates
    :align: center
    :width: 800px
    :height: 600px

**Alternative:** For a `home server setup <http://www.circuidipity.com/laptop-home-server.html>`_ I like to select ``Install security updates automatically`` for a device often running unattended ...

.. image:: images/screenshot/ubuntuInstall/300-1.png
    :alt: Install security updates
    :align: center
    :width: 800px
    :height: 600px

Select ``[*] standard system utilities``  and leave the remaining tasks unmarked if you wish to start with a minimal, console-only base configuration ready for further customization ... [5]_

.. image:: images/screenshot/ubuntuInstall/301.png
    :alt: Software selection
    :align: center
    :width: 800px
    :height: 600px

**Alternative:** Or - again, for a home server - select the few extras included in ``[*] Basic Ubuntu server`` ...

.. image:: images/screenshot/ubuntuInstall/301-1.png
    :alt: Software selection
    :align: center
    :width: 800px
    :height: 600px

Packages are downloaded and the installer makes its finishing touches ...

.. image:: images/screenshot/ubuntuInstall/302.png
    :alt: GRUB
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/303.png
    :alt: UTC
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/304.png
    :alt: Finish install
    :align: center
    :width: 800px
    :height: 600px

4. First boot
-------------

System will display a passphrase prompt to unlock encrypted ``home`` partition ...

.. image:: images/screenshot/ubuntuInstall/305.png
    :alt: Enter encrypt passphrase
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/ubuntuInstall/306.png
    :alt: Login
    :align: center
    :width: 800px
    :height: 600px

Login ... then run ``timedatectl`` to confirm system time+date is properly set.

5. GRUB
-------

After running a minimal install on my `C720 Ubuntubook <http://www.circuidipity.com/c720-ubuntubook.html>`_ with encrypted ``swap`` + ``home`` partitions I ran into this issue: `"Black screen instead of password prompt for boot encryption" <https://bugs.launchpad.net/ubuntu/+source/cryptsetup/+bug/1375435>`_.

I had to enter my passphrase blind and ``ALT+F1`` to console. When I tried removing the GRUB options ``splash`` and/or ``quiet`` I lost the ability to enter the passphrase at all and a hard reset was required.

**Fix:** Modify ``/etc/default/grub`` ...                                                    

.. code-block:: bash

    # Force the kernel to boot in normal text mode with '=text'                     
    GRUB_GFXPAYLOAD_LINUX=text
    
... and update ...

.. code-block:: bash

    $ sudo update-grub

Now it works! My chromebook is the only device I have run into this issue.

See: `GNU gfxpayload <https://www.gnu.org/software/grub/manual/html_node/gfxpayload.html>`_

6. Network
----------

Check which network interfaces are detected and settings ...

.. code-block:: bash

    $ ip a
    
**Wired** interfaces are usually auto-configured by default and assigned an IP address courtesy of DHCP.

To assign a **static** address, deactivate the wired interface and create a new entry in ``/etc/network/interfaces``. Sample entry for ``enp3s0`` ...

.. code-block:: bash

    # The primary network interface
    auto enp3s0
    #iface enp3s0 inet dhcp
    iface enp3s0 inet static
        address 192.168.1.88
        netmask 255.255.255.0
        gateway 192.168.1.1
        dns-nameservers 192.168.1.1

Bring up|down interface with ``sudo if{up,down} enp3s0``.

Create a temporary **wireless** interface connection to WPA2 encrypted access points manually using ``wpa_supplicant`` + ``wpa_passphrase`` + ``dhclinet``. Sample setup of ``wlp1s0`` ...

.. code-block:: bash

    $ sudo ip link set wlp1s0 up            # bring up interface
    $ iw dev wlp1s0 link                    # get link status
    $ sudo iw dev wlp1s0 scan | grep SSID   # scan for access points
    $ sudo -i                               # simulate a root login shell (for wpa_supplicant)
    # wpa_supplicant -B -i wlp1s0 -c<(wpa_passphrase "MY_SSID" "MY_PASSPHRASE")   # connect to WPA/WPA2 ... '-B' sends the process to the background
    # exit
    $ sudo dhclient wlp1s0                  # obtain IP address

More permanent configurations may be set in ``/etc/default/interfaces``. Sample setup [6]_ with a static IP address ...

.. code-block:: bash

    iface wlp1s0 inet static
        address 192.168.1.77
        netmask 255.255.255.0
        gateway 192.168.1.1                                                              
        wpa-ssid MY_SSID
        wpa-psk MY_PASSPHRASE
        dns-nameservers 8.8.8.8 8.8.4.4                                                  
                                                                                     
Alternative setup using DHCP ...

.. code-block:: bash               
                                                                                     
    allow-hotplug wlp1s0
    iface wlp1s0 inet dhcp
        wpa-ssid MY_SSID
        wpa-psk MY_PASSPHRASE                                       
        dns-nameservers 8.8.8.8 8.8.4.4

Once a link is established an optional network manager utility may be installed. Package ``network-manager-gnome`` provides the console ``nmcli`` and graphical ``nm-applet`` clients ...

.. code-block:: bash

    $ sudo apt install network-manager-gnome 

Comment out (deactivate) any entries in ``/etc/network/interfaces`` that will be managed by ``network-manager``.

7. Where to go next ...
-----------------------

... is up to YOU. Yeehaw.

Happy hacking!

Notes
-----

.. [1] An alternative is adding the image to a `USB stick with multiple Linux installers <http://www.circuidipity.com/multi-boot-usb.html>`_.

.. [2] Specifically, the console installer provides a **random key** option for the encrypted swap partition.

.. [3] Recommended: Otherwise the partitioning tool may designate the USB device as primary (sda) storage and lead to broken partition layouts.

.. [4] For storage devices >=128GB I create separate ``root`` + ``swap`` + ``home`` partitions. Smaller devices get ``boot`` + ``swap`` + ``root`` partitions. Note encrypted ``root`` **requires** an unencrypted ``boot``.

.. [5] The task selection menu can be run post-install using ``sudo tasksel``.

.. [6] Multiple wireless static IP address setups can be created with ``iface wlp1s0_NAME inet static`` and [de]activated with ``sudo if{up.down} wlp1s0=wlp1s0_NAME``.
