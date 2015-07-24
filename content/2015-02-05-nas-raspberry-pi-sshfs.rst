=======================================================
Network Attached Storage using a Raspberry Pi and SSHFS
=======================================================

:date: 2015-02-05 18:28:00
:slug: nas-raspberry-pi-sshfs
:tags: nas, ssh, network, raspberry pi, raspbian, debian, linux
:modified: 2015-07-05 16:21:00

`Raspberry Pi Home Server Hack #4 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ Connect a Pi to external USB storage and create a cheap and cheerful NAS device via **SSH Filesystem** (SSHFS).

With a `Pi-attached 1TB hard drive <http://www.circuidipity.com/run-a-raspberry-pi-2-from-external-usb-storage-using-raspbian.html>`_ hosting a properly configured `SSH server <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ nothing extra is required server-side. 

On the client... Install SSHFS and create a mountpoint for the remote filesystem:

.. code-block:: bash

    $ sudo apt-get install sshfs                                                          
    $ mkdir ~/NAS                                                          
                                                                                    
Mount the Pi-hosted remote filesystem (example: ``ip_address:192.168.1.88``) to the client:

.. code-block:: bash

    $ sshfs -o idmap=user 192.168.1.88:/media/external_usb_storage ~/NAS
                                                                                    
Contents of the remote hard drive now appear as local directories and files on the laptop. Data transfer between server and client is SSH-encrypted.

Use ``fusermount`` to detach from the remote storage:

.. code-block:: bash

    $ fusermount -u ~/NAS                       
                                                                           
Raspberry Pi + SSHFS is no speed demon but its very usable. On my laptop using a wireless LAN connection I am able to run Rhythmbox playing music and videos in VLC remotely hosted on the Pi.

Happy hacking!
