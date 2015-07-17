===================================================
Lightweight and a delight: i3 tiling window manager
===================================================

:date: 2015-07-17 00:20:00
:slug: i3-tiling-window-manager
:tags: i3, debian, linux

As a former **Fluxbox** and **Openbox** user I can understand the love for a lightweight, minimal window manager where I can "paint" my applications across the screen.

Subsequently I wandered through **Xfce** and **LXDE** and all the way to the other end of the scale with Ubuntu's *all-in* desktop environment **Unity**. I was curious about `tiling window managers <https://en.wikipedia.org/wiki/Tiling_window_manager>`_ but never quite grokked the advantage from screenshots: seeing consoles arranged in a grid made me think `tmux <http://www.circuidipity.com/tmux.html>`_ a better choice for *that* task, and why would I want to watch a video in a reduced square in the corner of a screen?

And then I tried `i3 <https://i3wm.org/>`_ and realized I have found my new default desktop:

* ``startx`` to X almost instantaneous on `Jessiebook <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_

* loads sensible defaults and - thanks to the excellent `User's Guide <https://i3wm.org/docs/userguide.html>`_ - easy to customize via text files

* toggle between **tiled**, **tabbed** (my default), **stacked**, and **floating** mode (see User's Guide)
 
* even if you rarely use applications in a tiled arrangement, i3 handles maximized windows, desktops, and multiple displays extremely well via keyboard

Still want to use a mouse here-and-there? Hey, i3 is flexible and OK with that. Provides a statusbar, but you can swap it out for an `alternative <https://wiki.archlinux.org/index.php/I3#i3bar_alternatives>`_ or run none at all.

Starting out I find myself mostly happy with the `default keybindings <https://i3wm.org/docs/userguide.html#_default_keybindings>`_ and behaviour; making only a few adjustments and additions to my ``~/.i3/config``.

Sources: `.i3/config <https://github.com/vonbrownie/dotfiles/blob/master/.i3/config>`_ and statusbar (for Jessiebook) `.i3status.conf <https://github.com/vonbrownie/dotfiles/blob/master/.i3status.conf.chromebook>`_

Auto-start applications
=======================

At launch I have configured i3 to run a script to detect/setup a second display if attached (using ``xrandr``), open a terminal, and run any extra commands as determined by ``$HOSTNAME``: 

.. code-block:: bash

    # Auto-start
    exec_always --no-startup-id $HOME/bin/dlDsply
    exec --no-startup-id $HOME/bin/startxX
    # Start a terminal
    #bindsym $mod+Return exec i3-sensible-terminal
    bindsym $mod+Return exec urxvt

Sources: `.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_, `dlDsply <https://github.com/vonbrownie/homebin/blob/master/dldsply>`_, `startxX <https://github.com/vonbrownie/homebin/blob/master/startxX>`_

Containers
==========

Arrange containers (windows):

.. code-block:: bash

    # Layout mode for new containers
    workspace_layout tabbed
    # Enable floating mode
    for_window [class="Remmina"] floating enable
    for_window [class="Remmina"] border normal
    for_window [class="VirtualBox"] floating enable
    for_window [class="VirtualBox"] border normal
    for_window [class="Vlc"] floating enable
    for_window [class="Vlc"] border normal

Styling
=======

Fonts:

.. code-block:: bash

    font pango:Terminus 11px

Colours:

.. code-block:: bash

    # Colours
    # class                   border  backgrd text    indicator
    client.focused            #1793d0 #1793d0 #ffffff #2e9ef4
    client.focused_inactive   #333333 #333333 #ffffff #484e50
    client.unfocused          #2d2d2d #2d2d2d #ffffff #292d2e
    client.urgent             #2f343a #900000 #ffffff #900000


Applications:

Use ``lxappearance`` to setup the **Clearlooks** theme and ``qtconfig-qt4`` to configure QT apps to use the ``GTK+`` default theme:

.. code-block:: bash

    $ sudo apt-get install gnome-themes-standard gtk2-engines lxappearance qt4-qtconfig

Launcher:

.. code-block:: bash

    bindsym $mod+d exec dmenu_run -fn 'Terminus 11' -nb '#2d2d2d' -nf '#ffffff' -sb '#1793d0' -sf '#ffffff'

Sound
=====

I use ``xbindkeys`` and a standalone `shell script <https://github.com/vonbrownie/homebin/blob/master/paVolume>`_ to control PulseAudio volume levels and notifications.

Source: `paVolume <http://www.circuidipity.com/pavolume.html>`_

Screenshots
===========

Take screenshots using ``scrot`` and ``eog`` displays images:

.. code-block:: bash

    $ sudo apt-get install scrot eog

Keybindings:

.. code-block:: bash

    # Screenshot
    # * desktop
    bindsym --release Print exec --no-startup-id scrot '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'
    # * active Window
    bindsym --release $mod+Print exec --no-startup-id scrot -d 4 -u -z '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'
    # * selected area... (click and move mouse)
    bindsym --release Shift+Print exec --no-startup-id scrot -s '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'

LockScreen/Logout/Suspend/Reboot/Shutdown
==========================================

Debian's i3 metapackage installs ``i3lock`` to handle locking screens (``-i IMAGE.png`` adds a lockscreen wallpaper) and ``systemctl`` deals with system suspend/reboot/shutdown:

.. code-block:: bash

    set $Locker i3lock -i ~/.i3lock.png && sleep 1
    set $mode_system System (l) lock, (e) logout, (s) suspend, (r) reboot, (Shift+s) shutdown
    mode "$mode_system" {
        bindsym l exec --no-startup-id $Locker, mode "default"
        bindsym e exec --no-startup-id i3-msg exit, mode "default"
        bindsym s exec --no-startup-id $Locker && sync && systemctl suspend, mode "default"
        bindsym r exec --no-startup-id systemctl reboot, mode "default"
        bindsym Shift+s exec --no-startup-id systemctl poweroff -i, mode "default"  

        # back to normal: Enter or Escape
        bindsym Return mode "default"
        bindsym Escape mode "default"
    }
    bindsym $mod+Pause mode "$mode_system"

Source: `i3 shutdown <https://wiki.archlinux.org/index.php/I3#Shutdown.2C_reboot.2C_lock_screen>`_

Happy hacking!
