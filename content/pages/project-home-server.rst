=============================================
There's no place like [a Linux] home [server]
=============================================

:slug: home-server
:template: page-project
:modified: 2017-06-05 15:35:00

.. image:: images/home-server.png
    :align: right
    :alt: Home Server
    :width: 300px
    :height: 300px

Running your own **Linux home server** is a fun learning experience about how networks work and giving new life to an old laptop or using a `Raspberry Pi <http://www.circuidipity.com/tag-raspberry-pi.html>`_ is a cheap and cheerful way to get the job done!

Plus privacy may be important to you. Hosting your own server running your own services gives more control over your data.

Let's go!
=========

Install a stable, well-tested Linux distribution and provide services such as network printing and storage (NAS), perform backups, host web services and much more. Start with a minimal base configuration of `Debian <http://www.circuidipity.com/minimal-debian.html>`_ or `Ubuntu <http://www.circuidipity.com/ubuntu-trusty-install.html>`_ and gain access to tens of thousands of packages ready to install.

0. Choose your server
---------------------

**A used laptop** -  retired in favour of more current and powerful machines - can still deliver plenty of *oomph* for running a personal server. Frugal with power and come equipped with their own built-in UPS (battery)! Link: `New life for an old laptop <http://www.circuidipity.com/laptop-home-server.html>`_

**... OR ...**

Running a **Pi server** with 24/7 uptime will enjoy more robust performance operating from a hard drive (vs SD card media). Link: `Host rootfs on external USB storage <http://www.circuidipity.com/raspberry-pi-usb-storage-v4.html>`_

1. `Secure remote access using SSH keys <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_
----------------------------------------------------------------------------------------------------------------

Use cryptographic keys to secure access to your new home server.

2. `Automatic security updates <http://www.circuidipity.com/unattended-upgrades.html>`_
---------------------------------------------------------------------------------------

Fetch the latest fixes, install, and reboot (if necessary).

3. `Multiple terminal windows using tmux <http://www.circuidipity.com/tmux.html>`_
----------------------------------------------------------------------------------

A *terminal multiplexor* for creating, detaching, re-attaching work areas.

4. `Backup home <http://www.circuidipity.com/backup-over-lan.html>`_
--------------------------------------------------------------------

Make incremental and automatic backups of a home folder to the server using SSH + rsync + cron.

5. `Network attached storage <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_
----------------------------------------------------------------------------------------

External USB storage + Pi turns any hard drive into a NAS.

6. `Access from anywhere in the world using dynamic DNS <http://www.circuidipity.com/ddns-openwrt.html>`_
---------------------------------------------------------------------------------------------------------

Use a DDNS service to automatically update an IP address.

7. `Web + database <http://www.circuidipity.com/php-nginx-postgresql.html>`_
----------------------------------------------------------------------------

Host web applications using PHP + Nginx + PostgreSQL.

8. `RSS reader <http://www.circuidipity.com/ttrss.html>`_
---------------------------------------------------------

Access news feeds over the web with Tiny Tiny RSS news reader.

9. `Print and scan <http://www.circuidipity.com/network-printer-scanner.html>`_
-------------------------------------------------------------------------------

Configure a printer + scanner to receive jobs across the local network.

10. `Torrents <http://www.circuidipity.com/rtorrent.html>`_
-----------------------------------------------------------

Use a text-based BitTorrent client combined with tmux to create a lightweight torrent server.

**Happy hacking!**
