=================================================
New life for an old laptop as a Linux home server
=================================================

:date: 2016-08-16 21:47:00
:tags: network, debian, linux
:slug: laptop-home-server
:modified: 2017-05-13 17:15:00

`PROJECT: Home Server #0 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ **Netbooks** ... remember those small, (a few) Linux-powered laptops from several years ago? I dusted off my old **Asus 900HA** netbook and put it to work as a `home server <http://www.circuidipity.com/tag-server.html>`_. Good times!

Running your own home server is a fun learning experience and offers several advantages.

Second-hand laptops -  retired in favour of more current and powerful machines - can still deliver plenty of *oomph* for running a personal server. Frugal with power and come equipped with their own built-in UPS (battery)!

Install a stable, well-tested Linux distribution and host services such as network printing and `storage (NAS) <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_, perform `backups <http://www.circuidipity.com/incremental-backups-rsnapshot.html>`_, host `web services <http://www.circuidipity.com/php-nginx-postgresql.html>`_ and much more. Start with a minimal base configuration of `Debian <http://www.circuidipity.com/tag-debian.html>`_ and gain access to tens of thousands of packages ready to install.

Privacy may be important to you. Hosting your own server running your own services gives more control over your data.

Let's go!
=========

**Hardware:** Asus 900HA netbook with 9" display, 1GB RAM, a 500GB hard drive (very easy replacement of original drive - just unscrew the netbook's bottom panel), built-in ethernet/wifi, webcam, and a host of ports (3xUSB2, VGA, sound, SD card slot). Neat and compact device!

0. Install Debian
-----------------

My `visual screenshot tour <http://www.circuidipity.com/minimal-debian.html>`_ of installing the Debian stable release. Debian's **minimal network install image** (32bit for the netbook) makes it easy to create a console-only base configuration that can be later customized for various tasks. 

I make a few modifications to my usual desktop install routine that are more appropriate for configuring a home server. I don't want an unattended server halting in the boot process waiting for a passphrase or any necessary boot mountpoints to reside on an encrypted partition. After a successful first boot I configure an encrypted container for data storage to be mounted manually to ``/media``.

Using the Debian installer I create 2 partitions on the netbook's 500GB internal storage ...

* sda1 is 512MB dedicated to ``boot`` [1]_
* sda2 is the remaining space dedicated to the **Logical Volume Manager** (LVM) that contains 2  **Logical Volumes** (LVs) ...
    * LV0 is 16GB used for ``root``
    * LV1 is 1GB used for ``swap`` encrypted with a **random key**
    * lots of space left free for the encrypted LV to be created post-install

1. Static network address
-------------------------

Login to the new home server and check which network interfaces are detected and settings ...                    
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ ip a                                                                      
                                                                                
**Wired** interfaces are usually auto-configured by default and assigned an IP address courtesy of DHCP.
                                                                                
To assign the server a **static** address (recommended), deactivate the wired interface and create a new entry in ``/etc/network/interfaces``. [2]_ Sample entry for ``enp3s0`` ...
                                                                                
.. code-block:: bash                                                            
                                                                                
    # The primary network interface                                             
    auto enp3s0                                                                 
    iface enp3s0 inet static                                                    
        address 192.168.1.88                                                    
        netmask 255.255.255.0                                                   
        gateway 192.168.1.1                                                     
        dns-nameservers 8.8.8.8                                            
                                                                                
Bring up|down interface with ``sudo if{up,down} enp3s0``.

2. SSH
------

`Install OpenSSH, create crypto keys, and disable password logins <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ to boost server security.

3. Automatic security updates
-----------------------------

`Fetch the latest fixes, install, and reboot (if necessary) <http://www.circuidipity.com/unattended-upgrades.html>`_. Hands-free!

4. Encrypted storage
--------------------

`Create a new logical volume, use LUKS to encrypt the storage, and setup a mountpoint <http://www.circuidipity.com/lvm-crypt-lv.html>`_ for manual mounting by a non-root user.

5. Power management on hard drive
---------------------------------

Default settings on the netbook frequently park and spindown the drive, generating an audible "click" sound. Too aggressive power management can reduce lifespan of drive. I want "kinder, gentler" settings.
                                                                                   
Get information on drive ...                                                     
                                                                                   
.. code-block:: bash                                                               
                                                                                   
    # hdparm -I /dev/sda                                                      

From ``man hdparm`` ...

``-B``                                                                             
    Get/set Advanced Power Management feature ... low value means aggressive power management and a high value means better performance. Possible settings range from values 1 through 127 (which permit spin-down), and values 128 through 254 (which do not permit spin-down) ... A value of 255 tells hdparm to disable APM altogether ...
                                                                                   
``-S``                                                                             
    Put the drive into idle (low-power) mode, and also set the standby (spindown) timeout for the drive ... A value of zero means "timeouts are disabled" ...
                                                                                   
On the netbook I run ...                                                         
                                                                                   
.. code-block:: bash                                                               
                                                                                   
    # hdparm -B 254 -S 0 /dev/sda                                             
                                                                                   
    /dev/sda:                                                                        
    setting Advanced Power Management level to 0xfe (254)                            
    setting standby to 0 (off)                                                       
    APM_level      = 254                                                           
                                                                                   
Create **udev rules** to setup at boot. Existing rule ...                         
                                                                                   
.. code-block:: bash                                                               
                                                                                   
    $ cat /lib/udev/rules.d/85-hdparm.rules                                          
    ACTION=="add", SUBSYSTEM=="block", KERNEL=="[sh]d[a-z]", RUN+="/lib/udev/hdparm"
                                                                                     
... and make my own ``/etc/udev/rules.d/85-hdparm.rules`` (rules in ``/etc/udev/rules.d`` have the `highest priority <http://manpages.ubuntu.com/manpages/wily/man7/udev.7.html>`_) ...
                                                                                   
.. code-block:: bash                                                               
                                                                                   
    ACTION=="add", SUBSYSTEM=="block", KERNEL=="sda", RUN+="/sbin/hdparm -B 254 -S 0 /dev/sda"

6. Services
-----------

What to do next? `Some of the services I use ... <http://www.circuidipity.com/raspberry-pi-home-server.html>`_

Happy hacking!

Notes
+++++

.. [1] Grub is not compatible with LVM, so ``/boot`` should be outside the storage managed by LVM.

.. [2] Problem: setting the network interface to static address can result in ``/etc/resolv.conf`` being overwritten every few minutes with an IPv6 address that breaks DNS. The "fix" is to maually set ``nameserver 8.8.8.8`` in resolv.conf and install the ``resolvconf`` package. Note that ``dns-nameservers`` entries are ignored if resolvconf is not installed.

