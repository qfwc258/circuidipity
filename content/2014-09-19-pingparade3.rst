========================
Ping Parade #3 -- Backup
========================

:slug: pingparade3
:tags: network, shell, programming, linux
:template: article-project-pingparade

**Make automatic backups of important stuff using a dash of shell scripting + rsync + SSH + cron!**

.. image:: images/pingparade3-0.png
    :alt: Backup
    :width: 960px
    :height: 500px

One of the advantages of setting up a `Linux home server <http://www.circuidipity.com/pingparade1.html>`_ is providing a place to do that thing which everyone agrees is important but *very few do consistently* (or even *once*): **backups**. Hopefully you never experience any loss of data... but *hope* is not a plan! A little peace of mind can be gained in a few steps as I describe the simple backup solution I use to automatically mirror my laptop's home directory on my netbook server sitting on the local area network (LAN).

Step 0 - SSH
============

Configure **OpenSSH** and **keychain** as per `these instructions <http://www.circuidipity.com/pingparade2.html>`_. Keychain makes it easy to use a **passphrase-protected encryption key** and `ssh-agent <https://en.wikipedia.org/wiki/Ssh-agent>`_ in automated scripts.

Step 1 - Script
===============

Login to the server and create a backup directory to hold the contents of $HOME: ``mkdir ~/home-backup``

On the local machine create a backup script - ``~/bin/backup_home.sh`` - that makes use of the **rsync** file-copying tool. A sample script includes:

* load the details of the **SSH key** stored in ``$HOME/.keychain/$HOSTNAME-sh``
* **mirror** ``$HOME`` to the server's ``~/home-backup`` using options ``--archive`` and ``--delete``
* **exclude** certain items from the backup like *cache* and *trash*
* **be careful nothing important is wiped out** using ``--delete`` ... run rsync in a console with option ``--dry-run`` to test your settings before saving to a script ...

.. code-block:: bash

    #!/bin/bash
    # Sample variables
    ssh_agent="$HOME/.keychain/$HOSTNAME-sh"
    rsync_options="--verbose --archive --delete"
    exclude_items="--exclude=*[Cc]ache* --exclude=*[Tt]rash*"
    local_dir="${HOME}/"
    address="192.168.1.22"
    destination="${address}:~/home-backup"

    . $ssh_agent
    rsync $rsync_options $exclude_items $local_dir $destination

Make the script executable and run manually at least once to test...

.. code-block:: bash

    $ chmod 755 ~/bin/backup_home.sh
    $ ~/bin/backup_home.sh

Step 2 - Automate
=================

**Cron** is a daemon that runs programs at specified times and I use the command ``crontab -e`` to setup my backup script to auto-run with the following parameters:

* perform a daily backup at 23:55
* run program silently in the background by redirecting output to ``/dev/null``
* any errors will be emailed to the user ...

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
    55 23 * * * $HOME/bin/backup_home.sh >/dev/null

For an alternate, more flexible rsync solution that accepts options at runtime `check out this more complete script <https://github.com/vonbrownie/linux-home-bin/blob/master/home2>`_ that I call using this `second script <https://github.com/vonbrownie/linux-home-bin/blob/master/backup-home-server>`_ executed by cron that includes logging (un)successful backup attempts to file.

Happy hacking!
