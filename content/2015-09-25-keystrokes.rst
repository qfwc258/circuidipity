=====================
Keystrokes cheatsheet
=====================

:date: 2015-09-25 16:30:00
:slug: keystrokes
:tags: cheatsheet, linux, shell

**Work-in-progress:** Keystroke combos that I find useful (listed here to jog my memory!)...

Chromebook
==========

Top row on my `Jessiebook <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_  keyboard has a series of shortcut icons (``Brightness``, ``Volume``...) that identify in Linux as the ``F1-F10`` keys and the ``Search`` key (in the ``CapsLk`` position) acts as ``Super`` (Windows) modifier key.

Enable these keyboard shortcuts in Debian by first installing:

* ``xbindkeys`` - associate keys to shell commands
* ``xbacklight`` - set backlight level using RandR
* ``pulseaudio-utils`` - manage sound with pactl
* ``xvkbd`` - send characters to another client

.. code-block:: bash

    $ sudo apt-get install xbindkeys xbacklight pulseaudio-utils xvkbd

See `Chromebook to Jessiebook <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_ for a sample configuration.

Firefox
=======

``CTRL-T``
    open new tab

``CTRL-Tab``
    switch tab

``SHIFT-CTRL-Tab``
    switch tab backwards

``CTRL-W``
    close tab

``CTRL-[``
    page back

``CTRL-]``
    page forward

``CTRL-L``
    enter new address/search

``CTRL-F``
    find

``F3``
    find again

``SHIFT-F3``
    find previous

``F5``
    reload page

Shell
=====

``CTRL-A``
    move to the start of line

``CTRL-E``
    move to the end of line

``CTRL-U``
    erase from cursor to start of line

``CTRL-K``
    erase from cursor to end of line

``CTRL-L``
    clear screen

``CTRL-R``
    reverse incremental search of history

Tmux
====

My `tmux cheatsheet <http://www.circuidipity.com/tmux.html>`_.

Happy hacking!
