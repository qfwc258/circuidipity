==============================================
Add a dynamic menu to your desktop using dmenu
==============================================

:tags: debian, linux
:slug: add-a-dynamic-menu-to-your-desktop-using-dmenu

*Dmenu* is a cool application for generating a dynamic menu on your desktop that can be activated using a hot-key combination.

A user begins typing the name of the application they wish to run and dmenu narrows down the list of possible matches as each letter is entered. When the desired choice is revealed it is highlighted and pressing ENTER launches the application.

I use `XFCE <http://www.xfce.org/>`_ as my desktop and completely ignore the built-in menu for launching applications ... relying instead on the combination of dmenu + hot-key codes for activating a few favourites.

On Debian ``dmenu`` is a part of the ``suckless-tools`` package ...

.. code-block:: bash

    $ sudo apt-get install suckless-tools

Create a bash script named ``dmenu-run.sh`` and place in ``~/bin`` ...

.. code-block:: bash

    #!/bin/bash
    exe=`dmenu_path | dmenu -fn 10x20 -nb '#000000' -nf '#ffffff' -sb green -sf '#000000'` && eval "exec $exe"

This will use ``dmenu`` to generate a horizontal menu of applications running across the top of the desktop (this can be tricky to get right... thanks `Giles <http://www.gilesorr.com/wm/helpers.html>`_ for the hint). Create a hot-key combination to activate ``dmenu-run.sh`` on your desktop when desired.
