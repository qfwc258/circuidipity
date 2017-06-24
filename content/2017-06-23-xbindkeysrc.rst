===============
Dot xbindkeysrc
===============

:date: 2017-06-23 23:30:00
:slug: xbindkeysrc
:tags: dotfiles, shell, linux

Bind commands to certain keys or key combos by creating ``~/.xbindkeysrc``.

Let's go!
=========

Top row on my `Stretchbook's <http://www.circuidipity.com/jessiebook-to-stretchbook.html>`_ keyboard has shortcut icons (``Brightness``, ``Volume``, etc.) that identify in Linux as ``F1-F10`` keys and the ``Search`` key (in ``CapsLk`` position) acts as a ``Super`` (Windows) modifier key.

Install some helpful utilities in Debian that we will associate with keyboard shortcuts ...

* ``xbindkeys`` - associate keys to shell commands
* ``xbacklight`` - set backlight level using RandR
* ``pulseaudio-utils`` - manage sound with ``pactl``
* ``xvkbd`` - send characters to another client 

.. code-block:: bash

    $ sudo apt install xbindkeys xbacklight pulseaudio-utils xvkbd

Enable function keys to modify sound, brightness, and page movement. Discover the **keycode** for a particular key by running ...

.. code-block:: bash

    $ xbindkeys -k

... press the key of interest, and a snippet of code is outputted that can be added to ``~/.xbindkeysrc``.

My own config for the Stretchbook ...

.. code-block:: bash

    # Backward/forward
    "xvkbd -xsendevent -text "\A\[Left]""
    F1 

    "xvkbd -xsendevent -text "\A\[Right]""
    F2 

    # Backlight decrease/increase
    "xbacklight -dec 10"
    F6
    "xbacklight -inc 10"
    F7

    # Volume mute/decrease/increase
    # paVolume - https://github.com/vonbrownie/homebin/blob/master/paVolume
    "paVolume -m"
    F8
    "paVolume -m"
    XF86AudioMute
    "paVolume -d"
    F9
    "paVolume -d"
    XF86AudioLowerVolume
    "paVolume -u"
    F10
    "paVolume -u"
    XF86AudioRaiseVolume

    # Page up/down, home, end
    "xvkbd -xsendevent -text '\[Page_Up]'"
    Alt + Up

    "xvkbd -xsendevent -text '\[Page_Down]'"
    Alt + Down

    "xvkbd -xsendevent -text '\[Home]'"
    Alt + Left

    "xvkbd -xsendevent -text '\[End]'"
    Alt + Right

Enable new key shortcuts ...

.. code-block:: bash

    $ xbindkeys

Place in ``~/.xinitrc`` to load configuration at ``startx`` ...

.. code-block:: bash

    if [ -f ~/.xbindkeysrc ]; then
        xbindkeys
    fi

Sources: `dotfiles/.xbindkeysrc <https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.chromebook>`_ and `dotfiles/.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_

Happy hacking!
