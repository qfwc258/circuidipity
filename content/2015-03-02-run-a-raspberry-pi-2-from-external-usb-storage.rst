==========================================
Run a Raspberry Pi 2 from USB storage v2.0
==========================================

:date: 2015-03-02 00:05:00
:slug: run-a-raspberry-pi-2-from-external-usb-storage
:tags: raspberry pi, ubuntu, linux, network
:modified: 2015-07-24 12:34:00

**Update:** Pi now running `Debian Jessie <http://www.circuidipity.com/raspberry-pi-usb-storage-v4.html>`_.

I am exploring the use of my Pi as **24/7 uptime home server** and one of the hacks I wish to add is using Pi as a cheap and cheerful `network attached storage (NAS) <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_ device. Hmmm... How about using that USB hard drive I connect for NAS and move over the Pi root filesystem and run it from there as well?

Let's go!
=========

I imagine an always-on Pi would enjoy more robust performance from a hard drive than SD card. [1]_ I put my plan in motion using:

* Raspberry Pi 2 Model B
* 5V 2A microUSB power adapter
* Ubuntu 14.04 Linux 
* 4GB microSD card (for initial setup and future ``boot`` partition)                                                                    
* 1TB powered USB hard drive
* ethernet cable
* HDMI display + USB keyboard (for initial setup) 

With the move to ARMv7 the Raspberry Pi 2 is now capable of running the ARM port of Ubuntu. A community-created `Ubuntu 14.04 LTS minimal image <https://wiki.ubuntu.com/ARM/RaspberryPi>`_ with an updated ``3.18`` kernel and firmware suitable for Pi 2 is now available. [2]_

0. Download
===========

**Using Linux:** Import the `lead developer's <http://www.finnie.org/2015/02/16/raspberry-pi-2-update-ubuntu-14-04-image-available/>`_ GPG key:

.. code-block:: bash                                                                
                                                                                    
    $ gpg --keyserver pgp.mit.edu --recv-key 86AE8D98                               
    gpg: keyring `/home/username/.gnupg/secring.gpg' created                             
    gpg: requesting key 86AE8D98 from hkp server pgp.mit.edu                        
    gpg: /home/username/.gnupg/trustdb.gpg: trustdb created                              
    gpg: key 86AE8D98: public key "Ryan Finnie <ryan@finnie.org>" imported          
    gpg: no ultimately trusted keys found                                           
    gpg: Total number processed: 1                                                  
    gpg:               imported: 1  (RSA: 1)                                        
    $ gpg --fingerprint 86AE8D98                                                    
    pub   4096R/86AE8D98 2012-04-11                                                 
    Key fingerprint = 42E2 C8DE 8C17 3AB1 02F5  2C6E 7E60 A3A6 86AE 8D98            
    uid                  Ryan Finnie <ryan@finnie.org>                              
    uid                  Ryan Finnie <ryan.finnie@canonical.com>                    
    uid                  [jpeg image of size 1669]                                  
    sub   4096R/C50F6695 2012-04-11                                                 
                                                                                    
Download the `latest ubuntu-trusty image and GPG signature <http://www.finnie.org/software/raspberrypi/>`_ for Pi 2:                           
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ wget -c http://www.finnie.org/software/raspberrypi/2015-02-19-ubuntu-trusty.zip
    $ wget -c http://www.finnie.org/software/raspberrypi/2015-02-19-ubuntu-trusty.zip.asc

Verify and unpack the image:

.. code-block:: bash

    $ gpg --verify 2015-02-19-ubuntu-trusty.zip.asc 2015-02-19-ubuntu-trusty.zip
    gpg: Signature made Thu 19 Feb 2015 12:46:09 PM EST using RSA key ID 86AE8D98
    gpg: Good signature from "Ryan Finnie <ryan@finnie.org>"                        
    gpg:                 aka "Ryan Finnie <ryan.finnie@canonical.com>"          
    gpg:                 aka "[jpeg image of size 1669]"                        
    gpg: WARNING: This key is not certified with a trusted signature!           
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: 42E2 C8DE 8C17 3AB1 02F5  2C6E 7E60 A3A6 86AE 8D98
    $ unzip 2015-02-19-ubuntu-trusty.zip
                                                                                
1. Install to SD card
=====================

In lieu of the usual ``dd`` I use `bmap-tools <https://source.tizen.org/documentation/reference/bmaptool/bmap-tools-project>`_ and ``2015-02-19-ubuntu-trusty.bmap`` to write ``2015-02-19-ubuntu-trusty.img`` to the SD card. **Advantages:** speed boost, and bmaptool's inability to write to mounted devices (in case you pick a wrong device/partition like, say, your *home* drive... ``dd``'s nickname *disk destroyer* is no idle boast):

.. code-block:: bash

    $ sudo apt-get install bmap-tools
    $ sudo bmaptool copy --bmap 2015-02-19-ubuntu-trusty.bmap 2015-02-19-ubuntu-trusty.img /dev/sdX

2. Pi Boot 
==========

Login username and password are both ``ubuntu``.

Filesystem layout on the SD card:

.. code-block:: bash
                                           
    $ df -h                                                                             
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/mmcblk0p2  1.7G  456M  1.1G  30% /
    devtmpfs        458M  4.0K  458M   1% /dev
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    none             93M  260K   93M   1% /run
    none            5.0M     0  5.0M   0% /run/lock
    none            462M     0  462M   0% /run/shm
    none            100M     0  100M   0% /run/user
    /dev/mmcblk0p1   64M  9.7M   55M  16% /boot/firmware

3. Partition external hard drive
================================

I connect the 1TB USB hard drive to Pi and confirm device detection:

.. code-block:: bash

    $ lsusb                                                                         
    Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp.                    
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub                  
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.                    
    Bus 001 Device 005: ID 152d:2329 JMicron Technology Corp. / JMicron USA Technology Corp. JM20329 SATA Bridge
    $ dmesg -t                                                                        
    [ ... ]                                                                         
    usb 1-1.3: new high-speed USB device number 5 using dwc_otg      
    usb 1-1.3: New USB device found, idVendor=152d, idProduct=2329   
    usb 1-1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=5
    usb 1-1.3: Product: USB to ATA/ATAPI bridge                      
    usb 1-1.3: Manufacturer: JMicron                                 
    usb 1-1.3: SerialNumber: DCA5968053FF                            
    usb-storage 1-1.3:1.0: USB Mass Storage device detected          
    usb-storage 1-1.3:1.0: Quirks match for vid 152d pid 2329: 8020  
    scsi0 : usb-storage 1-1.3:1.0                                    
    scsi 0:0:0:0: Direct-Access     WDC WD10 EARS-00Y5B1           PQ: 0 ANSI: 2 CCS
    sd 0:0:0:0: [sda] 1953525168 512-byte logical blocks: (1.00 TB/931 GiB)
    sd 0:0:0:0: [sda] Write Protect is off                           
    sd 0:0:0:0: [sda] Mode Sense: 28 00 00 00                        
    sd 0:0:0:0: [sda] No Caching mode page found                     
    sd 0:0:0:0: [sda] Assuming drive cache: write through            
    sd 0:0:0:0: [sda] No Caching mode page found                     
    sd 0:0:0:0: [sda] Assuming drive cache: write through            
    sd 0:0:0:0: Attached scsi generic sg0 type 0                     
    sda: sda1                                                       
    sd 0:0:0:0: [sda] No Caching mode page found                     
    sd 0:0:0:0: [sda] Assuming drive cache: write through            
    sd 0:0:0:0: [sda] Attached SCSI disk                             
   
Device is ``sda``. Use **fdisk** to create 2 new partitions on the USB drive:

* sda1 - 20GB - root filesystem
* sda2 - remaining space - storage

.. code-block:: bash

    $ sudo fdisk /dev/sda                                                           
                                                                                
    Command (m for help): p                                                         
                                                                                
    Disk /dev/sda: 1000.2 GB, 1000204886016 bytes                                   
    255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors         
    Units = sectors of 1 * 512 = 512 bytes                                          
    Sector size (logical/physical): 512 bytes / 512 bytes                           
    I/O size (minimum/optimal): 512 bytes / 512 bytes                               
    Disk identifier: 0x00000000                                                     
                                                                                
    Device Boot      Start         End      Blocks   Id  System                  
                                                                                
    Command (m for help): n                                                         
    Partition type:                                                                 
      p   primary (0 primary, 0 extended, 4 free)                                  
      e   extended                                                                 
    Select (default p): p                                                           
    Partition number (1-4, default 1):                                              
    Using default value 1                                                           
    First sector (2048-1953525167, default 2048):                                   
    Using default value 2048                                                        
    Last sector, +sectors or +size{K,M,G} (2048-1953525167, default 1953525167): +20G
                                                                                
    Command (m for help): n                                                         
    Partition type:                                                                 
      p   primary (1 primary, 0 extended, 3 free)                                  
      e   extended                                                                 
    Select (default p): p                                                           
    Partition number (1-4, default 2):                                              
    Using default value 2                                                           
    First sector (41945088-1953525167, default 41945088):                           
    Using default value 41945088                                                    
    Last sector, +sectors or +size{K,M,G} (41945088-1953525167, default 1953525167):
    Using default value 1953525167                    

    Command (m for help): p                                                         
                                                                                
    Disk /dev/sda: 1000.2 GB, 1000204886016 bytes                                   
    255 heads, 63 sectors/track, 121601 cylinders, total 1953525168 sectors         
    Units = sectors of 1 * 512 = 512 bytes                                          
    Sector size (logical/physical): 512 bytes / 512 bytes                           
    I/O size (minimum/optimal): 512 bytes / 512 bytes                               
    Disk identifier: 0x00000000                                                     
                                                                                
    Device Boot      Start         End      Blocks   Id  System                  
    /dev/sda1            2048    41945087    20971520   83  Linux                   
    /dev/sda2        41945088  1953525167   955790040   83  Linux                   
                                                                                
    Command (m for help): w                                                         
    The partition table has been altered!                                           
                                                                                
    Calling ioctl() to re-read partition table.                                     
    Syncing disks.            

Format the new partitions using filesystem ``ext4``:

.. code-block:: bash
                                                                                
    $ sudo mke2fs -t ext4 -L rootfs /dev/sda1                                       
    $ sudo mke2fs -t ext4 -L storage /dev/sda2                                      

4. Rsync
========

Mount the newly-formatted ``rootfs`` partition to ``/mnt``:

.. code-block:: bash

    $ sudo mount -t ext4 /dev/sda1 /mnt                                             
    
Use **rsync** to copy contents of ``root`` on the SD card to the ``rootfs`` partition on the USB device:

.. code-block:: bash

    $ sudo rsync -axv / /mnt

5. New rootfs
=============

5.1 On the SD card
------------------

Modify options in ``/boot/cmdline.txt`` to point the bootloader to ``root`` filesystem on the USB device:

.. code-block:: bash

    Original:                                                                      
    dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootwait
    
    Modified:
    dwc_otg.lpm_enable=0 console=tty1 root=/dev/sda1 rootwait rootdelay=5

5.2 On the USB hard drive
-------------------------

Create new mountpoint for the ``storage`` partition:

.. code-block:: bash

    $ sudo mkdir /mnt/media/USB0

Modify options in ``/mnt/etc/fstab`` to mount ``rootfs`` and ``storage`` partitions at boot. [3]_ Example for ``sda1`` and ``sda2``:

.. code-block:: bash

    proc            /proc           proc    defaults          0       0
    # comment out root filesystem on SD card
    #/dev/mmcblk0p2  /               ext4    defaults,noatime  0       1
    # partitions on USB hard drive
    /dev/sda1       /       ext4    defaults,noatime          0       1
    /dev/sda2       /media/USB0 ext4    defaults,noatime      0       0
    /dev/mmcblk0p1  /boot/firmware  vfat    defaults          0       2

6. Reboot
=========

Save modifications and reboot:

.. code-block:: bash

    $ sudo reboot
    
Log in and check out the new filesystem layout:

.. code-block:: bash
                                                                                
    $ df -h
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda1        20G  590M   18G   4% /
    devtmpfs        458M  4.0K  458M   1% /dev
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    none             93M  280K   93M   1% /run
    /dev/sda2       898G  326G  527G  39% /media/USB0
    none            5.0M     0  5.0M   0% /run/lock
    none            462M     0  462M   0% /run/shm
    none            100M     0  100M   0% /run/user
    /dev/mmcblk0p1   64M  9.9M   55M  16% /boot/firmware

7. Post-install
===============

7.1 Administrator
-----------------

Ubuntu is a great operating system but a not-so-great username and a lousy password. Example: change default username/group ``ubuntu`` to ``pi`` and set a new password.

Unlock ``root`` account by setting a new password:

.. code-block:: bash

    $ sudo passwd root

Log out and back in as ``root`` and configure ``pi``:

.. code-block:: bash

    # usermod -l pi -m -d /home/pi ubuntu
    # groupmod -n pi ubuntu
    # passwd pi

**Optional:** Re-lock ``root`` by disabling the password:

.. code-block:: bash

    $ sudo passwd -dl root

7.2 Hostname
------------

Example: Modify hostname ``ubuntu`` to ``raspberry`` in ``/etc/hostname`` and ``/etc/hosts`` and restart the ``hostname`` service:

.. code-block:: bash

    $ sudo service hostname restart

Log out and back in and hostname ``raspberry`` is visible.

7.3 Timezone
------------

Default timezone is ``UTC``. Modify to appropriate value:

.. code-block:: bash

    $ cat /etc/timezone 
    Etc/UTC
    $ sudo dpkg-reconfigure tzdata  # ...and follow the interactive menu to set (example) 'America/Toronto'...

    Current default time zone: 'America/Toronto'
    Local time is now:      Sun Mar  1 18:28:32 EST 2015.
    Universal Time is now:  Sun Mar  1 23:28:32 UTC 2015.

7.4 Upgrade
-----------

With the newly-configured ``rootfs`` up-and-running now is a good time to update Ubuntu:

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get dist-upgrade

7.5 Swap
--------

Ubuntu on Pi does not include a swap partition/file. Generate a (default) 2GB ``/var/swap`` file at boot by installing:

.. code-block:: bash

    $ sudo apt-get install dphys-swapfile

7.6 Static Address
------------------

A Raspberry Pi that is going to stay home and run as a server can be configured to use a **static network address**. Sample ``/etc/network/interfaces`` modification that disables ``dhcp`` and sets ip address ``192.168.1.88`` and connects to a router (that handles DNS) at ``192.168.1.1``:

.. code-block:: bash

    #iface eth0 inet dhcp                                                       
    auto eth0                                                                   
    iface eth0 inet static                                                      
        address 192.168.1.88                                                    
        netmask 255.255.255.0                                                   
        gateway 192.168.1.1
        dns-nameservers 192.168.1.1

7.7 OpenSSH Server
------------------

Install and configure SSH for remote access to our (soon-to-be) headless Pi home server:

.. code-block:: bash

    $ sudo apt-get install openssh-server

Check out `securing access to remote servers using SSH keys <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_.

Happy hacking!

Notes
-----

.. [1] `Discussion thread (raspberrypi.org/forums) <http://www.raspberrypi.org/forums/viewtopic.php?f=29&t=44177>`_ about moving root to external USB storage.
.. [2] `Version 1 <http://www.circuidipity.com/run-a-raspberry-pi-from-external-usb-storage.html>`_ used Raspbian on a Raspberry Pi Model B.
.. [3] Pi requires an SD card to boot so we continue using original ``/boot``.
