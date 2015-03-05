===========
Backup home
===========

:date: 2015-02-03 00:10:00
:slug: backup-home
:tags: networks, ubuntu, linux, shell, programming, github, raspberry pi
:modified: 2015-03-01 19:13:00

`Raspberry Pi Home Server Hack #3 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ Make automatic backups of a **home folder** using a dash of shell scripting + rsync + SSH + cron!

One of the advantages of setting up a `Linux home server <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ is providing an always-available location to store backups of important files. A little peace of mind can be gained in a few steps as I describe the simple backup solution I use to automatically mirror my laptop's home folder on the local area network (LAN) server.

Let's go!
=========

**Backup server** is a `Raspberry Pi 2 <http://www.circuidipity.com/run-a-raspberry-pi-2-from-external-usb-storage.html>`_ connected to a `1TB external USB hard drive <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_ running Ubuntu 14.04 LTS located at ip address ``192.168.1.88`` with username ``pi``.

0. SSH
======

`Secure remote access using SSH keys <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ to configure SSH for encrypted connections between (Pi) server and (laptop) client. ``Keychain`` + ``ssh-agent``  make it easy to use a passphrase-protected **encryption key** in automated scripts.

1. Script
=========

1.1 On the server
-----------------

Create a backup directory to hold the contents of ``HOME``:

.. code-block:: bash

    $ mkdir ~/backup-home

1.2 On the client
-----------------

Create a backup script that uses ``rsync`` file-copy tool. A sample ``myRsync`` script to backup ``HOME`` includes:

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

**Cron** is a daemon that runs programs at specified times. Use the command ``crontab -e`` to setup ``myRsync`` to auto-run with the following parameters:

* perform a daily backup at ``23:55``
* log program activity by redirecting output to ``/home/pi/cron.log``

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
    55 23 * * * /home/pi/bin/myRsync >> /home/pi/cron.log

I stashed a more complete ``myRsync`` `script on Github <https://github.com/vonbrownie/linux-home-bin/blob/master/myRsync>`_.

Happy hacking!
