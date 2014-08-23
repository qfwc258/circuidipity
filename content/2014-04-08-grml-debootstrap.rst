=====================================
Install Debian using grml-debootstrap
=====================================

:slug: grml-debootstrap
:tags: grml, debian, linux, chromebook
:modified: 22 August 2014

`Grml <http://grml.org/>`_ is a Debian-based Linux distribution optimized for running off USB sticks and taking care of sysadmin duties. One of its cool programs that I have been exploring is `grml-debootstrap <http://grml.org/grml-debootstrap/>`_ ... a console application that makes it very easy to set custom options and install Debian.

Here is a step-by-step process using grml-debootstrap to implement the following sample Debian minimal install on the 16GB solid-state drive (SSD) of my `Acer C720 Chromebook <http://http://www.circuidipity.com/c720-sidbook.html>`_:

* create encrypted root + swap
* install Debian **_wheezy_** (stable)
* upgrade to Debian **_sid_** (unstable) rolling release
* configure `TRIM <https://wiki.archlinux.org/index.php/Solid_State_Drives>`_ on the SSD to maximize performance

Source: Debian installation with `GRUB2 + GPT + LUKS crypto <http://michael-prokop.at/blog/2014/02/28/state-of-the-art-debianwheezy-deployments-with-grub-and-lvmsw-raidcrypto/>`_ (michael-prokop.at/blog)

Step 0 - Prepare USB boot device
================================

`Download <http://grml.org/download/>`_ an installer image (I selected the 32+64bit **grml96** combo) and simply ``dd`` the image to a spare USB device.

An alternate, more flexible approach (does not take over the entire drive) is `transforming a USB stick into a GRUB boot device <http://www.circuidipity.com/multi-boot-usb.html>`_ then adding the grml ISO as a menu entry that can co-exist with `multiple Linux distros <http://www.circuidipity.com/grubs.html>`_.

Step 1 - Boot, network and partitions
=====================================

Boot Grml with the **toram** option ``grml64-full - advanced options -> copy Grml to RAM``. This way we can make use of the USB boot device as storage for any extra packages or scripts we might want to use on the new Debian system.

Use the ``grml-network`` command to launch an interactive configuration of network interfaces. A sample entry generated for wifi in ``/etc/network/interfaces`` ...                              

.. code-block:: bash

    iface wlan0 inet dhcp                                                         
        wireless-mode auto                                                          
        wireless-essid YOUR_SSID                                             
        wpa-ssid YOUR_SSID                                      
        wpa-psk YOUR_PASSWORD                                                        

A sample **GUID Partition Table** (GPT) layout:

* sda1 - BIOS boot partition - 2MB                                              
* sda2 - boot - 200MB                                                    
* sda3 - swap - 1GB                                          
* sda4 - root - remaining space                                 
   
Create the above using ``parted`` (note: any changes are **executed instantly**) ...

.. code-block:: bash

    parted -a optimal /dev/sda                                                      
    print                                                                           
    mklabel gpt                                   
    unit mib                                                                        
    mkpart primary 1 3                                                              
    name 1 grub                                                                     
    set 1 bios_grub on                                                              
    mkpart primary 3 203                                                            
    name 2 boot                                                                     
    mkpart primary 203 1203                                                         
    name 3 swap                                                                     
    mkpart primary 1203 -1                                                          
    name 4 root                                                                     
    print                                                                           
    quit                                                                            
                                                                                
To verify that a partition is properly aligned query it using ``blockdev`` ('0' return = aligned) ...

.. code-block:: bash

    blockdev --getalignoff /dev/sdaX                               
    0                                                                               

Sources: `Grml boot cheatcodes <http://git.grml.org/?p=grml-live.git;a=blob_plain;f=templates/GRML/grml-cheatcodes.txt;hb=HEAD>`_ (git.grml.org), the `BIOS Boot Partition <https://www.gnu.org/software/grub/manual/html_node/BIOS-installation.html>`_ (gnu.org), and `partitioning disks using parted <http://www.gentoo.org/doc/en/handbook/handbook-amd64.xml?part=1&chap=4>`_ (gentoo.org)

Step 2 - Cryptsetup
===================

Configure the newly-created root partition for encrypted storage and create filesystems for ``boot`` and ``crypt-root`` ...

.. code-block:: bash

    cryptsetup luksFormat -c aes-xts-plain64 -s 256 /dev/sda4                       
    cryptsetup luksOpen /dev/sda4 crypt_root                                        
    mkfs.ext4 /dev/sda2                                                             
    mkfs.ext4 /dev/mapper/crypt_root                                                
   
Step 3 - Install Debian
=======================

Any extra packages to be installed can be added to the list in ``/etc/debootstrap/packages`` and scripts to customize the setup can be placed in ``/etc/debootstrap/chroot-scripts/``.

**Tip:** If configuring a device that only has a wireless interface (Chromebook) add the ``wireless-tools`` and ``wpasupplicant`` packages to the install list.

GRML auto-detects the ``crypt_root``, updating ``fstab`` and creating a mountpoint for the device in ``/media``. Mount the newly-created partitions and install a minimal Debian setup...

.. code-block:: bash

    mount /media/crypt_root                                     
    mkdir /media/crypt_root/boot                                                               
    mount -t ext4 /dev/sda2 /media/crypt_root/boot                                             
    # optional: with 'toram' usb stick can be mounted to /media... check /etc/fstab for auto-generated entries       
    grml-debootstrap --target /media/crypt_root --password "PASSWORD" --hostname HOSTNAME      

If ``grml-debootstrap`` is run with no options a limited interactive menu is provided ... otherwise the necessary Debian packages are downloaded and system setup runs unattended to completion.

Source: `grml-debootstrap HOWTO <http://grml.org/grml-debootstrap/>`_ (grml.org)

Step 4 - Adjust crypttab, fstab, initramfs
==========================================

Next step is to enter ``chroot`` and perform post-install configuration ...

.. code-block:: bash

    grml-chroot /media/crypt_root /bin/bash                                                    
    grub-install /dev/sda                                                           
    update-grub                                                                     
    # For SSD add the 'discard' option
    echo "crypt_root /dev/sda4 none luks,discard" >> /etc/crypttab                  
    echo "crypt_swap /dev/sda3 /dev/urandom cipher=aes-xts-plain64,size=256,discard,swap" >> /etc/crypttab
    echo "/dev/mapper/crypt_root / ext4 noatime,discard,errors=remount-ro 0 1" > /etc/fstab
    echo "/dev/sda2 /boot ext4 noatime,discard 0 2" >> /etc/fstab                   
    echo "/dev/mapper/crypt_swap none swap sw,discard 0 0" >> /etc/fstab            
    update-initramfs -u -k all                                                      

Source: `TRIM configuration on solid-state drives <http://www.linuxjournal.com/content/solid-state-drives-get-one-already>`_ (linuxjournal.com)

Step 5 - Sid, swappiness, locales, and timezone
===============================================

It is possible to use grml-debootstrap to directly install a Debian _sid_/unstable setup. But I have experienced greater success by first installing a minimal stable system before doing a dist-upgrade to track the unstable rolling release.

**Optional:** Continue configuration inside ``chroot`` and dist-upgrade to unstable by modifying ``/etc/apt/sources.list`` ...

.. code-block:: bash

    ### unstable ###
    deb http://http.debian.net/debian unstable main contrib non-free
    deb-src http://http.debian.net/debian unstable main contrib non-free

Run ``apt-get update && apt-get dist-upgrade``

The `swappiness <https://en.wikipedia.org/wiki/Swappiness>`_ parameter controls the preference of the kernel to move processes out of physical memory to the swap partition. Range is 0-100, default is set to 60 and lower values cause the kernel to avoid swapping and higher values prompt more frequent swap use.

To reduce writes on the SSD set a low value of '1' ...

.. code-block:: bash

    # check current swappiness value
    cat /proc/sys/vm/swappiness
    # temporarily change value
    /sbin/sysctl vm.swappiness=1
    # permanently change value... modify 'vm.swappiness' value in /etc/sysctl.conf...
    vm.swappiness=1

Configure the system environment for your local language and timezone using ``dpkg-reconfigure locales`` and ``dpkg-reconfigure tzdata``

Step 6 - Reboot
===============

Exit the chroot, unmount partitions, and reboot into Debian ...

.. code-block:: bash

    exit
    umount /media/crypt_root/boot                                                              
    umount /media/crypt_root                                                                
    cryptsetup luksClose /dev/mapper/crypt_root
    reboot

Happy hacking!
