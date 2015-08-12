============================================
Run remote X applications on a local display
============================================

:date: 2015-08-11 15:43:00
:slug: x11-forwarding-ssh
:tags: ssh, crypto, network, graphics, linux

Run remote X applications on a local display with X11 forwarding over SSH.

Let's go!
=========

I give my `Jessiebook's smallish amount of RAM <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_ a bit of a break by enlisting other machines on my home network to run X apps. Once `SSH is properly configured <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html>`_ it is easy to use X11 forwarding to have apps running on the server show up on the client's local display.

On the server
-------------

Activate X11 forwarding on the OpenSSH server by modifying ``/etc/ssh/sshd_config``:

.. code-block:: bash

    X11Forwarding yes                                                                    
                                                                                     
... and restart the server:

.. code-block:: bash

    $ sudo systemctl restart sshd.service
                               
On the client
-------------

X11 forwarding options can be configured system-wide in ``/etc/ssh/ssh_config`` or per-user in ``~/.ssh/config`` or simply forward X on a connection-by-connection basis at login with the ``-X`` option:

.. code-block:: bash

    $ ssh -X remote.host                                                                   
                                                                                     
Some apps might require the ``ForwardX11Trusted`` option to allow the full set of X functions from a **trusted** remote server:

.. code-block:: bash

    $ ssh -Y remote.host

.. role:: warning

:warning:`WARNING!` An intruder on the SSH server will be able to capture everything on the local screen and every keystroke with ``ForwardX11Trusted`` enabled.
                                                                                     
If SSH has properly configured X11 forwarding it sets ``$DISPLAY``:

.. code-block:: bash
                                                                                     
    $ echo $DISPLAY                                                                      
    localhost:10.0                                                                       
                                                                                     
Launch an X app on the server and it opens on the local display:

.. code-block:: bash

    $ urxvt &                                                                          

Logging into a remote host just to run a single app can be overkill. Run one-off commands with the ``-f`` option which backgrounds the SSH client before running the app:

.. code-block:: bash

    $ ssh -fX remote.host urxvt

One interesting use I discovered for X11 forwarding is running the ``rhythmbox`` music player. A limitation of X11 forwarding is that sound is not transmitted to the client's audio hardware. Turns out that is a **feature** on my home network setup because my speakers are connected to the server. I launch ``rhythmbox`` on the server, display and `control the player <http://www.circuidipity.com/thinkpad-usb-keyboard-trackpoint.html>`_ on the client, and the `good and funky sounds <https://www.youtube.com/watch?v=mZDYJYqcYK4>`_ issue forth from the server!

I create the ``Jukebox`` alias in ``~/.bash_aliases`` to X11 forward the player as a one-off command:

.. code-block:: bash

    alias Jukebox='ssh -fX remote.host rhythmbox'

Happy Hacking!
