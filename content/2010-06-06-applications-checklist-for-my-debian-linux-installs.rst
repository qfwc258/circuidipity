=====================================================
Applications checklist for my Debian Squeeze installs
=====================================================

:tags: debian, linux
:slug: applications-checklist-for-my-debian-linux-installs

These are some Linux applications I like to include with a `desktop installation <http://www.circuidipity.com/install-debian-linux-squeeze.html>`_ of Debian Squeeze.

Terminal: rxvt-unicode, tmux
----------------------------

.. code-block:: bash

    $ sudo apt-get install rxvt-unicode xfonts-terminus tmux

`Tmux <http://tmux.sourceforge.net/>`_  "is a terminal multiplexer: it enables a number of terminals (or windows), each running a separate program, to be created, accessed, and controlled from a single screen ... [then] detached from a screen and continue running in the background, then later reattached."

Editor: vim, gedit
------------------

.. code-block:: bash

    $ sudo apt-get install vim gedit

Desktop menu: dmenu
-------------------

.. code-block:: bash

    $ sudo apt-get install suckless-tools

Remote login: ssh
-----------------

*SSH client*

Install an SSH client and configure SSH public key authentication:

.. code-block:: bash

    $ sudo apt-get install openssh-client ssh-askpass keychain rsync

Generate an RSA user-key pair:

.. code-block:: bash

    $ mkdir ~/.ssh 
    $ cd ~/.ssh 
    $ ssh-keygen -v -t rsa -b 2048 -C username@hostname

Transfer the newly-generated public-key to any remote machine running SSH server. ``Keychain`` is a front-end to ``ssh-add`` that exists through an entire uptime across all sessions. To source ssh-keychain at startup edit ``~/.bashrc``:

.. code-block:: bash

    keychain ~/.ssh/id_rsa 
    . ~/.keychain/$HOSTNAME-sh

*SSH server*

Install the SSH server package:

.. code-block:: bash

    $ sudo apt-get install openssh-server

Restrict SSH login access to certain users by editing ``/etc/ssh/sshd_config``:

.. code-block:: bash

    PermitRootLogin no

    # permit only specified users ssh access
    AllowUsers yourUsername

Restart your SSH server after modifying and saving the configuration ... ``/etc/init.d/ssh restart``.

Copy that newly-generated RSA public-key from your client machine into your user account on the server:

.. code-block:: bash

    $ mkdir ~/.ssh
    $ touch ~/.ssh/authorized_keys
    $ cat id_rsa.pub >> ~/.ssh/authorized_keys

Network Manager: network-manager-gnome
--------------------------------------

.. code-block:: bash

    $ sudo apt-get install network-manager network-manager-gnome

Web Browser: iceweasel
----------------------

The default ``Firefox/Iceweasel (3.5)`` included in ``Squeeze`` is rather dated. More recent versions of the browser have been backported by the `Debian Mozilla Team <http://mozilla.debian.net>`_ .

First configure the package manager to track the backported Iceweasel release packages .. then grab the latest version:

.. code-block:: bash

    $ sudo apt-get -t squeeze-backports install iceweasel

Flash plug-in
-------------

.. code-block:: bash

    $ sudo apt-get install flashplugin-nonfree

Java
----

I use Google Video Chat (below) and experienced a slew of problems with ``openjdk`` that were finally resolved when I switched to the ``sun-java`` packages.
 
.. code-block:: bash

    $ sudo apt-get install sun-java6-jre sun-java6-plugin

VOIP: google-talk
-----------------

To add video chat to Gmail...  install dependencies:

.. code-block:: bash

    $ sudo apt-get install libglew1.5

Download the Debian package for the google-talk plugin from <http://www.google.com/chat/video> and install:

.. code-block:: bash

    $ sudo dpkg -i google-talkplugin_current_VERSION.deb

Bittorrent: rtorrent
--------------------

.. code-block:: bash

    $ sudo apt-get install rtorrent

Images: gimp, eog, geeqie, imagemagick, scrot
---------------------------------------------

.. code-block:: bash

    $ sudo apt-get install gimp gimp-data-extras gimp-help-en eog geeqie imagemagick scrot

Scanner: xsane, simple-scan
---------------------------

.. code-block:: bash

    $ sudo apt-get install xsane simple-scan

Document reader: xchm, evince
-----------------------------

.. code-block:: bash

    $ sudo apt-get install xchm evince

Office Suite: libreoffice
-------------------------

With `backports <http://backports-master.debian.org/>`_ enabled ...

.. code-block:: bash

    $ sudo apt-get -t squeeze-backports install libreoffice libreoffice-gtk libreoffice-help-en-us

Multimedia Codecs and Plugins: *assorted*
-----------------------------------------

.. code-block:: bash

    $ sudo apt-get install gstreamer0.10-plugins-{base,good,bad,ugly} gstreamer0.10-alsa gstreamer0.10-ffmpeg gstreamer0.10-tools
    $ sudo apt-get install lame vorbis-tools flac id3 id3v2 normalize-audio w32codecs
    $ sudo apt-get install libdvdcss2 libdvdnav4 libdvdread4

Audio Player: rhythmbox
-----------------------

.. code-block:: bash

    $ sudo apt-get install rhythmbox

Video Player: vlc
-----------------

.. code-block:: bash

    $ sudo apt-get install vlc

File-Handling and Compression Tools: *assorted*

.. code-block:: bash

    $ sudo apt-get install antiword cabextract fastjar file-roller html2text lzip lxsplit par2 p7zip-full unrar unrtf unzip

.. image:: images/debian-banner.png
    :width: 800px
    :height: 75px
    :alt: Get Debian
