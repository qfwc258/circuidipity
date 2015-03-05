============================================
Run a Raspberry Pi from external USB storage
============================================

:date: 2015-01-29 01:05:00
:slug: run-a-raspberry-pi-from-external-usb-storage
:tags: raspberry pi, raspbian, linux, networks
:modified: 2015-03-01 18:40:00

**Update:** Home server now `upgraded to Raspberry Pi 2 <http://www.circuidipity.com/run-a-raspberry-pi-2-from-external-usb-storage.html>`_. ``(2015-03-01)``

I am exploring the use of my Pi as **24/7 uptime home server** and one of the hacks I wish to add is using Pi as a cheap and cheerful `network attached storage (NAS) <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_ device. Hmmm... How about using that USB hard drive I connect for NAS and move over the Pi root filesystem and run it from there as well?

I imagine an always-on Pi would enjoy more robust performance from a hard drive than an SD card. Thanks to all the contributors `on this discussion thread <http://www.raspberrypi.org/forums/viewtopic.php?f=29&t=44177>`_ I put my plan in motion using:

* Raspberry Pi Model B
* 5V 1A microUSB power adapter
* ethernet cable
* Raspbian Linux
* SD card (for /boot)                                                                    
* 1TB powered USB hard drive

Let's go!
=========
                                                                                    
0. Raspbian Linux
=================

`Download <http://downloads.raspberrypi.org/raspbian_latest>`_ and unpack Raspbian and write the image to a spare 4GB+ SD card: 

.. code-block:: bash

    $ sudo dd bs=1M if=YYYY-MM-DD-wheezy-raspbian.img of=/dev/sdX                   
    $ sudo sync                                                                     

Sources: `operating system images <http://www.raspberrypi.org/downloads/>`_, installing `images on Linux <http://www.raspberrypi.org/documentation/installation/installing-images/linux.md>`_

1. Raspi-config
===============

Boot the Pi with the newly-minted Raspbian SD card and set a few options in the **raspi-config** utility:

.. code-block:: bash

    4 Internationalisation Options                                                      
        * Change Locale                                                                     
        * Change Timezone                                                                   
    8 Advanced Options                                                                  
        * Hostname                                                                          
        * Memory Split  # default is GPU=64MB, for a headless server set GPU=16MB and free more memory for the CPU                                                              
        * SSH           # enable SSH server at boot to permit login to Pi over LAN                                                                    
                                                                                    
Save the new parameters and reboot.

2. Partitions
=============

Filesystem layout on the SD card:

.. code-block:: bash
                                           
    $ df -h                                                                             
    Filesystem      Size  Used Avail Use% Mounted on                                    
    rootfs          2.9G  2.4G  401M  86% /                                             
    /dev/root       2.9G  2.4G  401M  86% /                                             
    devtmpfs        239M     0  239M   0% /dev                                          
    tmpfs            49M  232K   49M   1% /run                                          
    tmpfs           5.0M     0  5.0M   0% /run/lock                                 
    tmpfs            97M     0   97M   0% /run/shm                                  
    /dev/mmcblk0p1   56M  9.7M   47M  18% /boot                                     
    
I connect my 1TB USB drive to Pi and confirm device detection:

.. code-block:: bash

    $ lsusb                                                                         
    Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp.                    
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub                  
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.                    
    Bus 001 Device 005: ID 152d:2329 JMicron Technology Corp. / JMicron USA Technology Corp. JM20329 SATA Bridge
    $ dmesg                                                                         
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

* sda1 - 20GB - Pi root filesystem
* sda2 - remaining space - file storage

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

3. Filesystems
==============

Format the new partitions as ``ext4``:

.. code-block:: bash
                                                                                
    $ sudo mke2fs -t ext4 -L rootfs /dev/sda1                                       
    $ sudo mke2fs -t ext4 -L storage /dev/sda2                                      

4. /dev/root
============

Mount the newly-formatted ``rootfs`` partition to ``/mnt``:

.. code-block:: bash

    $ sudo mount -t ext4 /dev/sda1 /mnt                                             
    $ df -h                                                                         
    Filesystem      Size  Used Avail Use% Mounted on                                
    rootfs          2.9G  2.4G  401M  86% /                                         
    /dev/root       2.9G  2.4G  401M  86% /                                         
    devtmpfs        239M     0  239M   0% /dev                                      
    tmpfs            49M  220K   49M   1% /run                                      
    tmpfs           5.0M     0  5.0M   0% /run/lock                                 
    tmpfs            97M     0   97M   0% /run/shm                                  
    /dev/mmcblk0p1   56M  9.7M   47M  18% /boot                                     
    /dev/sda1        20G   44M   19G   1% /mnt                                      
    
Use **rsync** to copy contents of ``root`` on the SD card to the ``rootfs`` partition on the USB device:

.. code-block:: bash

    $ sudo rsync -axv / /mnt

5. New rootfs
=============

Modify options in ``/boot/cmdline.txt`` - located on the **SD card** - to point the bootloader to ``root`` filesystem on the USB device:

.. code-block:: bash

    Original:                                                                      
    dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
    
    Modified:
    dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1 root=/dev/sda1 rootfstype=ext4 elevator=deadline rootwait rootdelay=5

6. fstab
========

Create new mountpoint for the ``storage`` partition:

.. code-block:: bash

    $ sudo mkdir /mnt/media/USB0

Modify options in ``/mnt/etc/fstab`` - located on the **USB device** - to mount ``rootfs`` and ``storage`` partitions [1]_ at boot. Sample configuration for ``sda1`` and ``sda2``:

.. code-block:: bash

    proc            /proc           proc    defaults          0       0
    /dev/mmcblk0p1  /boot           vfat    defaults          0       2
    # partitions on USB
    /dev/sda1   /       ext4    defaults,noatime  0       1
    /dev/sda2   /media/USB0  ext4    defaults,noatime  0       0
    # comment out root filesystem on SD card
    #/dev/mmcblk0p2  /               ext4    defaults,noatime  0       1
    # a swapfile is not a swap partition, so no using swapon|off from here on, use  dphys-swapfile swap[on|off]  for that

7. Reboot
=========

Save modifications and reboot. Login and check the new filesystem layout:

.. code-block:: bash
                                                                                
    $ df -h
    Filesystem     Type      Size  Used Avail Use% Mounted on
    rootfs         rootfs     20G  2.6G   16G  15% /
    /dev/root      ext4       20G  2.6G   16G  15% /
    devtmpfs       devtmpfs  239M     0  239M   0% /dev
    tmpfs          tmpfs      49M  236K   49M   1% /run
    tmpfs          tmpfs     5.0M     0  5.0M   0% /run/lock
    tmpfs          tmpfs      97M     0   97M   0% /run/shm
    /dev/mmcblk0p1 vfat       56M  9.7M   47M  18% /boot
    /dev/sda2      ext4      898G  343G  510G  41% /media/USB0
                                                                         
8. Post-install
===============

8.1 Password
------------

A ``raspberry`` is a tasty fruit but a lousy password. Change password for username ``pi``:

.. code-block:: bash

    $ passwd
                                                                                
8.2 Sudo
--------

Default setting in Raspbian is to allow ``pi`` to use ``sudo`` without prompting for a password. Disable password-less ``sudo`` by running: 

.. code-block:: bash

    $ sudo visudo -s

... and comment out the ``NOPASSWD`` entry:

.. code-block:: bash

    #includedir /etc/sudoers.d
    #pi ALL=(ALL) NOPASSWD: ALL

8.3 Upgrade
-----------

With the newly-configured ``rootfs`` up-and-running now is a good time to update Raspbian:

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get dist-upgrade

8.4 Static Address
------------------

A Raspberry Pi that is going to stay home and run as a server can be configured to use a **static network address**. Sample ``/etc/network/interfaces`` modification that disables ``dhcp`` and sets ip address ``192.168.1.88``:

.. code-block:: bash

    #iface eth0 inet dhcp                                                       
    auto eth0                                                                   
    iface eth0 inet static                                                      
        address 192.168.1.88                                                    
        netmask 255.255.255.0                                                   
        gateway 192.168.1.1                                                     
                                                                                
Happy hacking!

Notes
-----

.. [1] Pi requires an SD card to boot... so we continue using original ``/boot``.
