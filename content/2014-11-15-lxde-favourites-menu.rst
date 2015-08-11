==========================
Pop-up custom menu in LXDE
==========================

:date: 2014-11-15 01:00:00
:slug: 20141115
:tags: lubuntu, linux, openbox, lxde

Create a hotkey-activated custom menu for favourite functions and applications.

Copy Openbox's default ``menu.xml`` and customize:

.. code-block:: bash

    $ cp /usr/share/lubuntu/openbox/menu.xml ~/.config/openbox/lubuntu-menu.xml

My `own menu <https://github.com/vonbrownie/linux-post-install/blob/master/config/generic/home/username/.config/openbox/lubuntu-menu.xml>`_ includes ``lxpanelctl menu``, search (using **catfish**), `Recent Files <https://github.com/vonbrownie/linux-home-bin/blob/master/ob-recent-files-pipemenu>`_ sub-menu, screenshot utility (**scrot**), and logout.

Create a key-combo in ``~/.config/openbox/lubuntu-rc.xml`` to activate the menu:

.. code-block:: bash

    <!-- Keybindings 'ALT+SPACEBAR for Openbox menu -->
    <keybind key="A-space">
        <action name="ShowMenu">
        <menu>root-menu</menu>
        </action>
    </keybind>

Reload the new configuration:

.. code-block:: bash

    $ openbox --reconfigure

Happy hacking!

Sources: `lubuntu-menu.xml <https://github.com/vonbrownie/linux-post-install/blob/master/config/generic/home/username/.config/openbox/lubuntu-menu.xml>`_ + `lubuntu-rc.xml <https://github.com/vonbrownie/linux-post-install/blob/master/config/generic/home/username/.config/openbox/lubuntu-rc.xml>`_ + `ob-recent-files-pipemenu <https://github.com/vonbrownie/linux-home-bin/blob/master/ob-recent-files-pipemenu>`_ (github.com/vonbrownie), `Configuring the Openbox Menu <http://crunchbanglinux.org/wiki/configuring_the_openbox_menu>`_ (crunchbanglinux.org)
