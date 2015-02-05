=======================================================
Network Attached Storage using a Raspberry Pi and SSHFS
=======================================================

:date: 2015-02-05 18:28:00
:slug: nas-raspberry-pi-sshfs
:tags: networks, raspberry pi, linux

`Raspberry Pi Home Server Hack #4 >> <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ Connect a Pi to external USB storage and create a cheap, cheerful, encrypted traffic NAS device via **SSH Filesystem (SSHFS)**.

With a `Pi-attached 1TB hard drive <http://www.circuidipity.com/run-a-raspberry-pi-from-external-usb-storage.html>`_ hosting a properly configured `SSH server <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ nothing extra is required server-side. On my Chromebook I install SSHFS, add my username to the ``FUSE`` group, and create a local ``piNAS`` mountpoint for the remote filesystem:

.. code-block:: bash

    $ sudo apt-get install sshfs                                                          
    $ sudo adduser USERNAME fuse                                                               
    $ mkdir ~/piNAS                                                          
                                                                                    
Log out and back in for new permissions to be activated. To mount the Pi-hosted remote filesystem to the Chromebook:                                                                             

.. code-block:: bash

    $ sshfs -o idmap=user ip_address_of_the_Pi:/media/your_external_usb_storage ~/piNAS
                                                                                    
Contents of the remote hard drive now appear as local directories and files on the Chromebook. Data transfer between server and client is SSH-encrypted.

To detach from remote storage unmount the drive using ``fusermount``:

.. code-block:: bash

    $ fusermount -u ~/piNAS                       
                                                                           
Raspberry Pi + SSHFS is no speed demon but its very usable. On my Chromebook connected to the LAN via wireless I am able to run Rhythmbox playing music and videos in VLC that are remotely hosted on the Pi.

Happy hacking!
