==============
Minimal Debian
==============

:date: 2015-07-07 15:43
:slug: minimal-debian
:tags: debian, linux, crypto, lvm
:modified: 2017-06-18 10:21:00

.. figure:: images/debianVader.png
    :alt: Debian Vader
    :width: 960px
    :height: 355px

**Debian 9 "Stretch"** is the latest stable release of the popular Linux operating system. I use Debian's `minimal network install image <https://www.debian.org/CD/netinst/>`_ to create a **console-only base configuration** that can be customized for various tasks and `alternate desktops <http://www.circuidipity.com/i3-tiling-window-manager.html>`_. [1]_

Let's go!
=========

`Debian GNU/Linux <http://www.debian.org>`_ is an operating system created by volunteers of one of the largest and longest-running free software projects in the world. There are 3 **release branches**: ``stretch/stable``, ``buster/testing``, and ``sid/unstable``.

Below is a visual walk-through of a sample workstation setup that makes use of the entire disk divided into 2 partitions: a ``boot`` partition, [2]_ and an **encrypted partition** used by the **Logical Volume Manager** (LVM) to create "virtual partitions" (Logical Volumes). Installing LVM on top of the encrypted partition allows:

* creation of multiple LVs protected by a single passphrase entered at boot time
* dynamic resizing of filesystems (set aside unallocated space and make use of it as needed)
* snapshots of filesystems that can be used as backups or to restore a previous state [3]_

0. Prepare install media
------------------------

Download the (unofficial image that includes non-free firmware) `64bit firmware-CURRENT-amd64-netinst.iso <https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/iso-cd/>`_ (`32bit image <https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current/i386/iso-cd/>`_ for older machines). `Verify the PGP signature <http://www.circuidipity.com/verify-pgp-signature-gnupg.html#verify-file-integrity>`_ and `flash the image <https://www.debian.org/releases/stable/amd64/ch04s03.html.en>`_ to a USB stick. [4]_

Minimal installer (requires network connection) downloads all the latest packages during setup.

1. Launch
---------

.. image:: images/screenshot/debianInstallLvm/001-stretch.png
    :align: center
    :alt: Install
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/002.png
    :align: center
    :alt: Select Language
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/003.png
    :alt: Select Location
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/004.png
    :alt: Configure Keyboard
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/005.png
    :alt: Hostname
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/006.png
    :alt: Domain
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/007.png
    :alt: Root password
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/008.png
    :alt: Verify password
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/009.png
    :alt: Full Name
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/010.png
    :alt: Username
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/011.png
    :alt: User password
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/012.png
    :alt: Verify password
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/013.png
    :alt: Select time zone
    :align: center
    :width: 800px
    :height: 600px

2. Partitions
-------------

Sample layout:

* sda1 is a 512MB ``boot`` partition
* sda2 uses the remaining storage as a LUKS encrypted partition
* LVM is installed on the encrypted partition, and contains a volume group with the 3 logical volumes ``root`` + ``swap`` + ``home``

.. image:: images/screenshot/debianInstallLvm/100.png
    :alt: Partitioning method
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/101.png
    :alt: Partition disks
    :align: center
    :width: 800px
    :height: 600px


.. image:: images/screenshot/debianInstallLvm/102.png
    :alt: Partition table
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/103.png
    :alt: Free space
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/104.png
    :alt: New partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/105.png
    :alt: Partition size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/106.png
    :alt: Primary partition
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/107.png
    :alt: Beginning
    :align: center
    :width: 800px
    :height: 600px

Modify the default mount options ... [5]_

.. code-block:: bash

    Mount point: /boot
    Mount options: relatime
    Bootable flag: on

.. image:: images/screenshot/debianInstallLvm/108.png
    :alt: Boot
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/109.png
    :alt: Free space
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/104.png
    :alt: New partition
    :align: center
    :width: 800px
    :height: 600px

Assign the remaining storage to the encrypted partition ...

.. image:: images/screenshot/debianInstallLvm/110.png
    :alt: Partition size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/106.png
    :alt: Primary partition
    :align: center
    :width: 800px
    :height: 600px

Modify the default mount options ...

.. code-block:: bash

    Use as: physical volume for encryption
    Erase data: no

If the hard disk has not been securely wiped prior to installing Debian you may want to configure ``Erase data: yes``. Note, however, depending on the size of the disk this operation can last several hours.

.. image:: images/screenshot/debianInstallLvm/111.png
    :alt: Physical volume for encryption
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/112.png
    :alt: Configure encrypted volumes
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/113.png
    :alt: Write changes
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/114.png
    :alt: Create encrypted
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/115.png
    :alt: Devices to encrypt
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/116.png
    :alt: Finish
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/117.png
    :alt: Passphrase
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/118.png
    :alt: Verify passphrase
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/119.png
    :alt: Partition disks
    :align: center
    :width: 800px
    :height: 600px

Modify the default mount options ...

.. code-block:: bash

    Use as: physical volume for LVM

.. image:: images/screenshot/debianInstallLvm/120.png
    :alt: Physical volume for LVM
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/121.png
    :alt: Configure LVM
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/122.png
    :alt: Write changes
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/123.png
    :alt: Create volume group
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/124.png
    :alt: Vg name
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/125.png
    :alt: Device for vg
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/126.png
    :alt: Create lv
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/127.png
    :alt: Vg
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/128.png
    :alt: Lv root
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/129.png
    :alt: Lv root size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/130.png
    :alt: Create lv
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/131.png
    :alt: Vg
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/132.png
    :alt: Lv swap
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/133.png
    :alt: Lv swap size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/134.png
    :alt: Create lv
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/135.png
    :alt: Vg
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/136.png
    :alt: Lv home
    :align: center
    :width: 800px
    :height: 600px

Set aside some unused space for future requirements. LVM makes it easy to expand or create new filesystems as needed ...

.. image:: images/screenshot/debianInstallLvm/137.png
    :alt: Lv home size
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/138.png
    :alt: Finish lvm
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/139.png
    :alt: Select lv root
    :align: center
    :width: 800px
    :height: 600px

Modify the default mount options ...

.. code-block:: bash

    Use as: Ext4
    Mount point: /
    Mount options: relatime

.. image:: images/screenshot/debianInstallLvm/140.png
    :alt: Lv root config
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/141.png
    :alt: Select lv swap
    :align: center
    :width: 800px
    :height: 600px

Modify the default mount options ...

.. code-block:: bash

    Use as: swap area

.. image:: images/screenshot/debianInstallLvm/142.png
    :alt: Lv swap config
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/143.png
    :alt: Select lv home
    :align: center
    :width: 800px
    :height: 600px

Modify the default mount options ... [6]_

.. code-block:: bash

    Use as: Ext4
    Mount point: /home
    Mount options: relatime
    Reserved blocks: 1%

.. image:: images/screenshot/debianInstallLvm/144.png
    :alt: Lv home config
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/145.png
    :alt: Finish partitioning
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/146.png
    :alt: Write changes
    :align: center
    :width: 800px
    :height: 600px

3. Install packages and finish up
---------------------------------

.. image:: images/screenshot/debianInstallLvm/200.png
    :alt: Configure package manager
    :align: center
    :width: 800px
    :height: 600px

Use the Debian global mirrors service `deb.debian.org <https://wiki.debian.org/DebianGeoMirror>`_ ...

.. image:: images/screenshot/debianInstallLvm/201-1.png
    :alt: Mirror hostname
    :align: center
    :width: 800px
    :height: 600px


.. image:: images/screenshot/debianInstallLvm/202.png
    :alt: Mirror directory
    :align: center
    :width: 800px
    :height: 600px


.. image:: images/screenshot/debianInstallLvm/203.png
    :alt: Proxy
    :align: center
    :width: 800px
    :height: 600px


.. image:: images/screenshot/debianInstallLvm/204.png
    :alt: Popularity contest
    :align: center
    :width: 800px
    :height: 600px

Select only ``[*] standard system utilities`` and leave the remaining tasks [7]_ unmarked ...
    
.. image:: images/screenshot/debianInstallLvm/205.png
    :alt: Software selection
    :align: center
    :width: 800px
    :height: 600px

Packages are downloaded and the installer makes its finishing touches ...

.. image:: images/screenshot/debianInstallLvm/206.png
    :alt: Downloading
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/207.png
    :alt: Install GRUB to MBR
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/208.png
    :alt: GRUB device
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/209.png
    :alt: Finish
    :align: center
    :width: 800px
    :height: 600px

4. First boot
-------------

.. image:: images/screenshot/debianInstallLvm/300.png
    :alt: GRUB menu
    :align: center
    :width: 800px
    :height: 600px

User is prompted for the passphrase to unlock the encrypted partition ...

.. image:: images/screenshot/debianInstallLvm/301-1.png
    :alt: Unlock passphrase
    :align: center
    :width: 800px
    :height: 600px

.. image:: images/screenshot/debianInstallLvm/302-stretch.png
    :alt: Login
    :align: center
    :width: 800px
    :height: 600px

Login and run ``timedatectl`` to confirm system date+time is properly configured.

5. GRUB
-------

After running a minimal install on my Acer C720 Chromebook with encrypted swap + home partitions I ran into this issue: `"Black screen instead of password prompt for boot encryption" <https://bugs.launchpad.net/ubuntu/+source/cryptsetup/+bug/1375435>`_.

I had to enter my passphrase blind and ``ALT+F1`` to console. When I tried removing the GRUB options ``splash`` and/or ``quiet`` I lost the ability to enter the passphrase at all and a hard reset was required.

**Fix:** Modify ``/etc/default/grub`` ...

.. code-block:: bash

    ## Force the kernel to boot in normal text mode with '=text'
    GRUB_GFXPAYLOAD_LINUX=text

... and update ...

.. code-block:: bash

    # update-grub

Now it works! My chromebook is currently the only device I have run into this issue.

See: `GNU gfxpayload <https://www.gnu.org/software/grub/manual/html_node/gfxpayload.html>`_

6. Network
----------

Check which network interfaces are detected and settings ...

.. code-block:: bash

    $ ip a
    
**Wired** interfaces are usually auto-configured by default and assigned an IP address courtesy of DHCP.

To assign a **static** address, deactivate the wired interface and create a new entry in ``/etc/network/interfaces``. [8]_ Sample entry for ``enp3s0`` ...

.. code-block:: bash

    # The primary network interface
    auto enp3s0
    iface enp3s0 inet static
        address 192.168.1.88
        netmask 255.255.255.0
        gateway 192.168.1.1
        dns-nameservers 8.8.8.8 8.8.4.4

Bring up|down interface with ``if{up,down} enp3s0``.

Create a temporary **wireless** interface connection to WPA2 encrypted access points manually using ``wpa_supplicant`` + ``wpa_passphrase`` + ``dhclinet``. Sample setup of ``wlp1s0`` ...

.. code-block:: bash

    # ip link set wlp1s0 up             ## bring up interface
    # iw dev wlp1s0 link                ## get link status
    # iw dev wlp1s0 scan | grep SSID    ## scan for access points
    # wpa_supplicant -i wlp1s0 -c<(wpa_passphrase "MY_SSID" "MY_PASSPHRASE")   ## connect to WPA/WPA2 ... add '-B' to background process
    # dhclient wlp1s0                   ## obtain IP address

More permanent configurations may be set in ``interfaces``. Sample setup [9]_ with a static IP address ...

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

Once a link is established install an (optional) network manager utility. Packages ``network-manager`` and ``network-manager-gnome`` provide the console ``nmcli`` and graphical ``nm-applet`` clients respectively . Comment out (deactivate) any entries in ``interfaces`` that will be managed by ``network-manager``.

7. Secure access using SSH keys
-------------------------------

Create `cryptographic keys, install the OpenSSH server, and configure remote access. <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_

8. Main, non-free, contrib, and backports
-----------------------------------------

Debian uses three archives to distinguish between software packages based on their licenses. **Main** is enabled by default and includes everything that satisfies the conditions of the `Debian Free Software Guidelines. <https://www.debian.org/social_contract#guidelines>`_ **Non-free** contains packages that do not meet all the conditions of the DFSG but can be freely distributed, and **contrib** packages are open-source themselves but rely on software in non-free to work.

`Backports <https://backports.debian.org/>`_ contains packages drawn from the testing (and sometimes unstable) archive and modified to work in the current stable release. All backports are disabled by default (to prevent unintended system upgrades) and are installed on a per PACKAGE basis by running ...

.. code-block:: bash

    # apt -t stretch-backports install PACKAGE

Modify ``/etc/apt/sources.list`` to add contrib, non-free, and backports ...

.. code-block:: bash

    # Base repository
    deb http://deb.debian.org/debian/ stretch main contrib non-free
    deb-src http://deb.debian.org/debian/ stretch main contrib non-free

    # Security updates
    deb http://security.debian.org/debian-security stretch/updates main contrib non-free
    deb-src http://security.debian.org/debian-security stretch/updates main contrib non-free

    # Stable updates
    deb http://deb.debian.org/debian stretch-updates main contrib non-free
    deb-src http://deb.debian.org/debian stretch-updates main contrib non-free

    # Stable backports
    deb http://deb.debian.org/debian stretch-backports main contrib non-free
    deb-src http://deb.debian.org/debian stretch-backports main contrib non-free

Any time ``sources.list`` is modified be sure to update the package database ...

.. code-block:: bash

    # apt update

9. Automatic security updates
-----------------------------

Fetch and install `the latest fixes courtesy of unattended upgrades. <http://www.circuidipity.com/unattended-upgrades.html>`_

10. Sudo
--------

Install ``sudo`` to temporarily provide your USER (example: ``foo``) account with root privileges ...

.. code-block:: bash

    # apt install sudo
    # adduser foo sudo

To allow ``foo`` to shutdown or reboot the system, first create the file ``/etc/sudoers.d/00-alias`` containing ...

.. code-block:: bash

    # Cmnd alias specification
    Cmnd_Alias SHUTDOWN_CMDS = /sbin/poweroff, /sbin/reboot, /sbin/shutdown

Starting with Stretch, if you run as USER the command ``dmesg`` to read the contents of the kernel message buffer you will see ...

.. code-block:: bash

    dmesg: read kernel buffer failed: Operation not permitted

Turns out it is `a (security) feature not a bug! <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=842226#15>`_

To allow ``foo`` to read the kernel log without being prompted for a password - and use our newly-created ``Cmnd_Alias SHUTDOWN_CMDS`` - create the file ``/etc/sudoers.d/01-nopasswd`` containg the ``NOPASSWD`` option ...

.. code-block:: bash

	# Allow specified users to execute these commands without password
	foo ALL=(ALL) NOPASSWD: SHUTDOWN_CMDS, /bin/dmesg

I add aliases for the commands in my ``~/.bashrc`` to auto-include ``sudo`` ...

.. code-block:: bash

    alias dmesg='sudo dmesg'
    alias poweroff='sudo /sbin/poweroff'
    alias reboot='sudo /sbin/reboot'
    alias shutdown='sudo /sbin/shutdown'

11. Where to go next ...
------------------------

... is up to YOU. I created a `post-install configuration script <https://github.com/vonbrownie/linux-post-install/tree/master/scripts/debian-stable-setup>`_ that builds on a minimal install towards a more complete console setup, and can also install the `i3 tiling window manager <http://www.circuidipity.com/i3-tiling-window-manager.html>`_ plus a packages collection suitable for a workstation.

Happy hacking!

Notes
+++++

.. [1] Image courtesy of `jschild <http://jschild.deviantart.com/art/Facebook-cover-debian-Darth-Vader-380351614>`_.

.. [2] Note that encrypted ``root`` **requires** an unencrypted ``boot``.

.. [3] Very helpful! `LVM post on the Arch Wiki <https://wiki.archlinux.org/index.php/LVM>`_.

.. [4] An alternative is adding the image to a `USB stick with multiple Linux installers <http://www.circuidipity.com/multi-boot-usb.html>`_.

.. [5] ``Mount options: relatime`` decreases write operations and boosts drive speed.

.. [6] Reserved blocks can be used by privileged system processes to write to disk - useful if a full filesystem blocks users from writing - and reduce disk fragmentation. On large **non-root partitions** extra space can be gained by reducing the default 5% reserve set aside by Debian to 1%.

.. [7] Task selection menu can be used post-install by running (as root) ``tasksel``.

.. [8] Problem: setting the network interface to static address can result in ``/etc/resolv.conf`` being overwritten every few minutes with an IPv6 address that breaks DNS. The "fix" is to maually set ``nameserver 8.8.8.8`` in resolv.conf and install the ``resolvconf`` package. Note that ``dns-nameservers`` entries are ignored if resolvconf is not installed.

.. [9] Multiple wireless static IP address setups can be created with ``iface wlp1s0_NAME inet static`` and [de]activated with ``if{up.down} wlp1s0=wlp1s0_NAME``.
