=====================================
Compile and install programs in $HOME
=====================================

:modified: 2017-07-16 18:35:00
:date: 2017-07-10 16:00:00
:slug: compile-install-homedir
:tags: shell, linux

`PROJECT: The Lifecycle of Debian Objects .: <http://www.circuidipity.com/the-lifecycle-of-debian-objects.html>`_ Debian has extensive (50,000+) package archives but sometimes I want **that one thing** they do not! Or maybe I want to re-compile the source code of a program with different options.

I can make a clean separation between **a)** programs installed by Debian packages; and **b)** programs installed by myself; by compiling and installing programs as a **non-root user** in my home directory.

Let's go!
=========

`Volnoti <https://github.com/davidbrazdil/volnoti>`_ is a lightweight volume notification tool `I like to use with i3 <http://www.circuidipity.com/i3-tiling-window-manager.html>`_ and there is no Debian package available.

0. Start
--------

Download the program source code. Source for ``volnoti`` is hosted on GitHub ...

.. code-block:: bash

    $ git clone git://github.com/davidbrazdil/volnoti.git

Check the README for any build dependencies and install. All the ``volnoti`` requirements can be satisfied with Debian packages ...

.. code-block:: bash

    $ sudo apt install libdbus-glib-1-dev libgtk2.0-dev libgdk-pixbuf2.0-dev autoconf automake

Create the **destination directory** for the program contents. By creating a program-specific directory I can easily remove a program by simply deleting the directory ...

.. code-block:: bash

    $ mkdir -p ~/opt/volnoti

1. Pre-compile
--------------

`Apply any necessary fixes <http://ubuntuforums.org/showthread.php?t=2215264&s=7aa2dfa8b89411472598e737c38f1475&p=12978792#post12978792>`_ ...

.. code-block:: bash

    $ cd volnoti
    $ ./prepare.sh
    $ cd src
    $ rm value-client-stub.h && make value-client-stub.h
    $ rm value-daemon-stub.h && make value-daemon-stub.h
    $ cd ..

2. Compile and install
----------------------

Compile and install program to the custom destination directory ...

.. code-block:: bash

    $ ./configure --prefix=$HOME/opt/volnoti
    $ make
    $ make install

Add the executable directory (``$HOME/opt/volnoti/bin``) to the PATH in `~/.profile <https://github.com/vonbrownie/dotfiles/blob/master/.profile>`_ ...

.. code-block:: bash

    # set PATH so it includes programs installed in user's home directory
    # volnoti - volume notification daemon
    if [ -d "$HOME/opt/volnoti/bin" ] ; then
        PATH="$HOME/opt/volnoti/bin:$PATH"
    fi

3. Run program
--------------

Start the ``volnoti`` daemon ...

.. code-block:: bash

    $ volnoti

Configure daemon to auto-start by adding it to `~/.xinitrc <http://www.circuidipity.com/xinitrc.html>`_ ... 

.. code-block:: bash

    volnoti -t 2 &

Links: `Volume control and notification <http://www.circuidipity.com/pavolume.html>`_ and `DontBreakDebian <https://wiki.debian.org/DontBreakDebian>`_

Happy hacking!
