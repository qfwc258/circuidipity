==============================================
Add a dynamic menu to your desktop using dmenu
==============================================

:date: 2011-03-22 01:23:00
:tags: shell, programming, openbox, linux
:slug: add-a-dynamic-menu-to-your-desktop-using-dmenu
:modified: 15 April 2014

*Dmenu* is a cool application for generating a dynamic menu on your desktop that can be activated using a hot-key combination.

A user begins typing the name of the application they wish to run and dmenu narrows down the list of possible matches as each letter is entered. When the desired choice is revealed it is highlighted and pressing ENTER launches the application.

I use `Openbox <http://openbox.org/>`_ as my window manager and completely ignore the built-in menu for launching applications ... relying instead on the combination of dmenu + hot-key codes for activating a few favourites.

On Debian ``dmenu`` is a part of the ``suckless-tools`` package ...

.. code-block:: bash

    $ sudo apt-get install suckless-tools

Create a bash script named ``dmenu-run.sh`` and place in ``$HOME/bin`` ...

.. code-block:: bash

    #!/bin/bash
    # Generate a dynamic applications menu
    # Source: bitmap fonts <https://en.wikipedia.org/wiki/Fixed_%28typeface%29>

    dmenu_run -b -i -fn '10x20' \
        -nb '#000000' -nf '#ffffff' -sb '#d64937' -sf '#000000'

This will use ``dmenu`` to generate a horizontal menu of applications running across the bottom of the desktop (this can be tricky to get right... thanks `Giles <http://www.gilesorr.com/wm/helpers.html>`_ for the hint). Create a hot-key combination to activate ``dmenu-run.sh`` on your desktop.

Source: `dmenu-run.sh <https://github.com/vonbrownie/linux-home-bin/blob/master/dmenu-run.sh>`_
