===================
Incremental backups
===================

:date: 2015-08-12 01:27:00
:slug: incremental-backups-rsnapshot
:tags: network, debian, linux, raspberry pi
:modified: 2016-02-12 23:13:00

`Raspberry Pi Home Server Hack #3 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ Make incremental and automatic backups of a home folder using **rsnapshot + cron** (and manual backups via **public transit**).

Let's go!
=========

Backup strategy **Version 0** for my home folder was **rsync** + **portable** + **subway**. That is, I would simply make a periodic, manual sync of files using **rsync** from my primary computer to a **portable** encrypted `USB hard drive <http://www.circuidipity.com/encrypt-external-drive.html>`_. Then ride the **subway** to a family/friend's place and swap drives (offsite backup).

**Version 1** expanded to **cron** + **rsync** + **Raspberry Pi** + **portable** + **subway**. One of the advantages of setting up a `Raspberry Pi home server <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ is providing a 24/7 uptime location to automatically (using **cron**) mirror my laptop's home folder over the local area network (LAN).

These backups are **snapshots** of home at a particular date. Pi server has a backup of 24 hours or less, the USB drive has another snapshot a few weeks old, the offsite another snapshot from a month ago. But there is no ordered progression of backups from Day 2 to Day 3, Week 4, Month 5, etc. One alternative is to every day stash an entire backup of my home folder but its a sub-optimal use of resources and would quickly fill a hard drive.

A much better solution is to use `rsnapshot <http://rsnapshot.org/>`_  to make **incremental backups** and my backup strategy **Version 2** now incorporates:

* **cron** + **rsnapshot** + **cron** + **rsync** + **Raspberry Pi** + **portable** + **subway**;
* nightly a cron job runs ``rsnapshot`` to sync ``/home/`` and ``/etc/`` to ``/my/backup/location/daily.0/``;
* ``daily.0`` increments to ``daily.1``, ``daily.1`` to ``daily.2``, etc. (retention set to 7 days)
* ``--hard-links`` is how ``rsnapshot`` performs its minimal-storage-magic... if a file remains unchanged in the next backup a hard link is created so subsequent backups only contain modified files and links;
* in the wee morning hours another cron job syncs ``/my/backup/location/`` to Pi server;
* every Saturday ``daily.6`` rotates to ``weekly.0`` (and ``weekly.0`` to ``weekly.1`` ... with 4 week retention);
* on the 1st of the month ``weekly.3`` rotates to ``month.0`` (12 month retention);
* every week or so I sync ``/my/backup/location/`` to the USB drive;
* every month or so I ride the subway to offsite storage and swap drives

0. Rsnapshot
============

Install ``rsnapshot``, make a directory to store backups, and make a copy of the default config file:

.. code-block:: bash

    $ sudo apt-get install rsnapshot
    $ mkdir /my/backup/location
    $ sudo cp /etc/rsnapshot.conf /etc/rsnapshot.conf.default                              
                                                                                     
Modify ``/etc/rsnapshot.conf`` (important to separate fields with **TABS** not spaces). Example of a few tweaks:

.. code-block:: bash

    snapshot_root   /my/backup/location                                       
    
    cmd_cp          /bin/cp
    cmd_rm          /bin/rm
    cmd_rsync       /usr/bin/rsync
    cmd_du          /usr/bin/du
    cmd_rsnapshot_diff      /usr/bin/rsnapshot-diff

    retain  daily   7                                                                    
    retain  weekly  4                                                                    
    retain  monthly 12                                                                   
                                                                                     
    exclude_file    /home/USER/.rsyncExclude  # ...and create this file with list of things to exclude from backup
                                                                                     
    link_dest       1                                                                    
                                                                                     
    sync_first      1  # allows better recovery in the event that rsnapshot is interrupted (see: ``man rsnapshot``)

    # LOCALHOST                                                                          
    backup  /home/          localhost/                                                   
    backup  /etc/           localhost/                                                   
    
Check config syntax and run backup test:

.. code-block:: bash

    $ sudo rsnapshot configtest
    $ sudo rsnapshot -t sync                                                               
                                                                                     
If everything checks out OK go ahead and run:

.. code-block:: bash

    $ sudo rsnapshot sync && sudo rsnapshot daily && rsnapshot du                                          
                                                                                     
Automate backups by modifying the sample cron file provided in ``/etc/cron.d/rsnapshot`` and running jobs as root. Example config:

.. code-block:: bash

    # m h  dom mon dow   command                                                         
    50 23 * * *     root    /usr/bin/rsnapshot sync && /usr/bin/rsnapshot daily                  
    40 22 * * 6     root    /usr/bin/rsnapshot weekly                                            
    30 21 1 * *     root    /usr/bin/rsnapshot monthly 

1. Backup the backup
====================

Rsnapshot operates as a **pull** program: it pulls in backups from local and remote devices. Instead of juggling access permissions to allow the rsnapshot server to talk with other devices I decided to limit ``rsnapshot`` to making backups on ``localhost`` and use `my already-configured SSH key setup <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ to **push** a snapshot of the backup to my Raspberry Pi for remote storage.

1.1 On the Pi
-------------

Create a directory to store the backup:

.. code-block:: bash

    $ mkdir /path/to/backup                                             

1.2 On localhost
----------------

Set the ip address and hostname of the Pi server in ``/etc/hosts``:

.. code-block:: bash

    192.168.1.88    raspberry.server

Test synching ``/my/backup/location/`` on ``localhost`` to ``raspberry.server:/path/to/backup/`` with the ``rsync --dry-run`` option (I exclude ``/etc/`` from the backup):

.. code-block:: bash

    rsync --dry-run --archive --hard-links --numeric-ids --delete --exclude=etc/ --verbose /my/backup/location/ raspberry.server:/path/to/backup/

If everything checks out OK drop ``--dry-run`` and re-run the command to make a proper backup.

I use ``keychain`` to manage `SSH keys for password-less logins to the Pi <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_. Create a ``backupSnap.sh`` shell script and place in ``~/bin``:

.. code-block:: bash

    #!/bin/bash                                                                     
    . ${HOME}/.keychain/${HOSTNAME}-sh                                              
    rsync --archive --hard-links --numeric-ids --delete --exclude=etc/ /my/backup/location/ $1

Automate the backups by creating a cron job (example that runs daily at 04:50):

.. code-block:: bash
                                                                                
    # m h  dom mon dow   command                                                    
    50 4 * * *  /home/USERNAME/bin/backupSnap.sh raspberry.server:/path/to/backup/      

2. External drive and offsite storage
=====================================

I connect my USB drive and sync the backup to the device:

.. code-block:: bash

    $ /home/USERNAME/bin/backupSnap.sh /media/USB/path/to/backup/

... and take my hard drive for `a ride on the subway <http://ttc.ca/Routes/General_Information/Maps/index.jsp>`_ to say hello to my offsite storage!

Happy hacking!
