===========
Backup home
===========

:date: 2015-02-03 00:10:00
:slug: backup-home
:tags: ssh, crypto, network, raspbian, debian, linux, shell, programming, raspberry pi
:modified: 2015-07-05 16:11:00

`Raspberry Pi Home Server Hack #3 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ Make **automatic backups** of a home folder using a dash of shell scripting + rsync + SSH + cron!

Let's go!
=========

One of the advantages of setting up a `Linux home server <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ is providing a 24/7 uptime location to store backups of important files. A little peace of mind can be gained in a few steps as I describe the simple backup solution I use to automatically mirror my laptop's home folder over the local area network (LAN).

**Server** is a `Raspberry Pi 2 <http://www.circuidipity.com/tag-raspberry-pi.html>`_ (example: ``login:pi/ip_address:192.168.1.88``) connected to a `1TB USB hard drive <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_ running `Raspbian <http://www.circuidipity.com/tag-raspbian.html>`_.

0. SSH
======

`Secure remote access using keys <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ to configure SSH for encrypted connections between server and client. ``Keychain`` makes it easy to use a passphrase-protected encryption key in automated scripts.

1. Script
=========

On the server
-------------

Create a backup directory to hold the contents of ``home``:

.. code-block:: bash

    $ mkdir ~/backup-home

On the client
-------------

Create a backup script using the ``rsync`` file-copy tool. A sample ``myRsync`` script to backup ``HOME`` includes:

* load the details of the SSH key stored in ``$HOME/.keychain/$HOSTNAME-sh``
* mirror ``$HOME/`` to ``192.168.1.88:~/backup-home/`` using options ``--archive`` and ``--delete``
* exclude certain items from the backup like ``cache`` and ``trash``

.. role:: warning

:warning:`WARNING!` Take care nothing important is wiped out using ``--delete``. First run ``rsync`` in a console with option ``--dry-run`` to test settings:

.. code-block:: bash

    $ rsync --verbose --archive --delete --dry-run ~/ pi@192.168.1.88:~/backup-home/

Sample script:

.. code-block:: bash

    #!/bin/bash
    # ~/bin/myRsync
    ssh_agent="${HOME}/.keychain/$HOSTNAME-sh"
    rsync_options="--verbose --archive --delete"
    rsync_exclude="--exclude=*[Cc]ache* --exclude=*[Tt]rash*"
    rsync_src="${HOME}/"
    rsync_dest="pi@192.168.1.88:~/backup_home/"

    . $ssh_agent
    echo $(date)
    rsync $rsync_options $rsync_exclude $rsync_src $rsync_dest

Place the script in ``~/bin`` and make it executable. Run manually at least once to test:

.. code-block:: bash

    $ chmod 744 ~/bin/myRsync
    $ ~/bin/myRsync

2. Automate
===========

**Cron** is a daemon that runs programs at specified times. Use the command ``crontab -e`` to setup ``myRsync`` to auto-run with the following parameters (example):

* perform a daily backup at ``23:55``
* log program activity by redirecting output to ``/home/USERNAME/cron.log``

.. code-block:: bash

    # To define the time you can provide concrete values for                           
    # minute (m), hour (h), day of month (dom), month (mon),                           
    # and day of week (dow) or use '*' in these fields (for 'any').#                   
    #                                                                                  
    # Output of the crontab jobs (including errors) is sent through                    
    # email to the user the crontab file belongs to (unless redirected).               
    #                                                                                  
    # For more information see the manual pages of crontab(5) and cron(8)              
    #                                                                                  
    # m h  dom mon dow   command                                                       
                                                                                   
    # Daily backup of $HOME to the netbook server                                
    55 23 * * * /home/username/bin/myRsync >> /home/username/cron.log

Happy hacking!

Source: `myRsync <https://github.com/vonbrownie/homebin/blob/master/myRsync>`_
