===================================================
Lightweight and a delight: i3 tiling window manager
===================================================

:date: 2015-07-17 00:20:00
:slug: i3-tiling-window-manager
:tags: i3, ubuntu, linux
:modified: 2016-04-30 16:38:00

As a former **Fluxbox** and **Openbox** user I can understand the love for a lightweight, minimal window manager where I can "paint" my applications across the screen. I was curious about `tiling window managers <https://en.wikipedia.org/wiki/Tiling_window_manager>`_ but never quite grokked the advantage from screenshots: seeing consoles arranged in a grid made me think `tmux <http://www.circuidipity.com/tmux.html>`_ a better choice for that task, and why would I want to watch a video in a reduced square in the corner of a screen?

And then I tried `i3 <https://i3wm.org/>`_ and found my new default desktop:

* ``startx`` to X almost instantaneous on `Ubuntubook <http://www.circuidipity.com/c720-ubuntubook.html>`_

* loads sensible defaults and - thanks to the excellent `User's Guide <https://i3wm.org/docs/userguide.html>`_ - easy to customize via text files

* toggle between **tiled**, **tabbed** (my default), **stacked**, and **floating** mode (see User's Guide)
 
* even if you rarely use applications in a tiled arrangement, i3 handles maximized windows, desktops, and multiple displays extremely well via keyboard

Still want to use a mouse here-and-there? Hey, i3 is flexible and OK with that. Provides a statusbar, but you can swap it out for an `alternative <https://wiki.archlinux.org/index.php/I3#i3bar_alternatives>`_ or run none at all.

Starting out I find myself mostly happy with the `default keybindings <https://i3wm.org/docs/userguide.html#_default_keybindings>`_ and behaviour; making only a few adjustments and additions to my ``~/.i3/config`` and ``/.i3status.conf``. [1]_

Install
=======

I use the third-party `i3 Ubuntu repository <https://i3wm.org/docs/repositories.html>`_. Download and install the keyring, configure apt, and install the latest window manager packages ...

.. code-block:: bash

    $ wget http://debian.sur5r.net/i3/pool/universe/s/sur5r-keyring/sur5r-keyring_2015.12.29_all.deb
    $ sudo dpkg -i sur5r-keyring*.deb
    $ sudo cp /etc/apt/sources.list /etc/apt/sources.list.$(date +%FT%H%M%S).bak
    $ sudo echo "## i3 window manager" >> /etc/apt/sources.list
    $ sudo echo "deb http://debian.sur5r.net/i3/ $(lsb_release -c -s) universe" >> /etc/apt/sources.list
    $ sudo apt update && sudo apt install i3 i3status i3lock

Auto-start applications
=======================

In my ``~/.xinitrc`` I have added a few applications to start at launch: a script to detect and setup a second display if attached (using ``xrandr``), another script to configure things like my Thinkpad USB keyboard and empty Trash, and finally open a terminal.

In the i3 configuration file I replace the default dynamic application launcher ``dmenu`` with `rofi <https://davedavenport.github.io/rofi/>`_ (``sudo apt install rofi``) ...

.. code-block:: bash

    # rofi - window switcher, run dialog and dmenu replacement                         
    bindsym F3 exec --no-startup-id rofi -show run                                     
    bindsym $mod+Tab exec --no-startup-id rofi -show window

Window tabs
===========

I remove tabs from windows and replace them with thin coloured bars by reducing window title font size to zero ...

.. code-block:: bash

    # Font for window titles. Will also be used by the bar unless a different font  
    # is used in the bar {} block below.                                            
    font pango:DejaVu Sans Mono 0

... and setting the colour for active/inactive windows ...

.. code-block:: bash

    # Colours                                                                       
    # * class                 border  backgrd text    indicator                     
    client.focused            #ff0000 #ff0000 #ffffff #2e9ef4                       
    client.focused_inactive   #333333 #333333 #ffffff #484e50                       
    client.unfocused          #000000 #000000 #ffffff #292d2e                       
    client.urgent             #2f343a #900000 #ffffff #900000

Containers
==========

Arrange containers (windows) to default to a **tabbed** layout ... and allow a few applications to start in alternate **floating** (unmaximized) mode ...

.. code-block:: bash

    # Layout mode for new containers
    workspace_layout tabbed
    # Enable floating mode
    for_window [class="Remmina"] floating enable
    for_window [class="Remmina"] border normal
    for_window [class="VirtualBox"] floating enable
    for_window [class="VirtualBox"] border normal
    for_window [class="vlc"] floating enable
    for_window [class="vlc"] border normal

Screenshots
===========

I install **scrot** for screenshots and **eog** as image viewer ...

.. code-block:: bash

    $ sudo apt install scrot eog

... and configure key combos to trigger desktop/active window/selected area snapshots ...

.. code-block:: bash

    # Screenshot                                                                    
    # * desktop                                                                     
    bindsym --release Print exec --no-startup-id scrot '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'
    bindsym --release F4 exec --no-startup-id scrot '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'
    # * active Window                                                               
    bindsym --release $mod+Print exec --no-startup-id scrot -d 4 -u -z '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'
    bindsym --release $mod+F4 exec --no-startup-id scrot -d 4 -u -z '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'
    # * selected area... (click and move mouse)                                     
    bindsym --release Shift+Print exec --no-startup-id scrot -s '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'
    bindsym --release Shift+F4 exec --no-startup-id scrot -s '%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && eog ~/Downloads/$f'

Sound
=====

I use a combination of **pavucontrol**, **volnoti** (a lightweight sound notification utility), **xbindkeys** + `shell script <http://www.circuidipity.com/pavolume.html>`_ to control PulseAudio volume levels.

Styling
=======

Theme dependencies, fonts, and config utilities ...

.. code-block:: bash

    $ sudo apt install gnome-themes-standard gtk2-engines-murrine gtk2-engines-pixbuf fonts-liberation ttf-ubuntu-font-family xfonts-terminus lxappearance qt4-qtconfig
    
I use the `Ambiance Colors GTK <http://www.ravefinity.com/p/download-ambiance-radiance-colors.html>`_ and `Vibrancy Color Icon <http://www.ravefinity.com/p/vibrancy-colors-gtk-icon-theme.html>`_ themes. Download the ``*.deb`` packages separately and install using ``sudo dpkg -i *.deb``.

Run ``lxappearance`` to setup the GTK theme (outputs to ``~/.gtkrc-2.0`` and ``~/.config/gtk-{2,3}.0``) and ``qtconfig-qt4`` to configure QT4 (outputs to ``~/.config/Trolltech.conf``) to use the ``GTK+`` default theme.

Theming for QT5 applications can be configured using the ``qt5ct`` utility. `Download the qt5ct package <http://ppa.launchpad.net/nilarimogard/webupd8/ubuntu/pool/main/q/qt5ct/>`_ available on the `WebUpd8 PPA <https://launchpad.net/~nilarimogard/+archive/ubuntu/webupd8>`_ and ``sudo dpkg -i qt5ct*.deb``.

Add to ``~/.xinitrc`` ...

.. code-block:: bash

    export QT_QPA_PLATFORMTHEME="qt5ct"

Exit from X and log back in. Run ``qt5ct`` (outputs to ``~/.config/qt5ct/qt5ct.conf``) and configure QT5 to use GTK settings.

See: `Uniform look for QT and GTK applications <https://wiki.archlinux.org/index.php/Uniform_look_for_Qt_and_GTK_applications>`_ and `Configure QT5 with QT5CT <http://www.webupd8.org/2015/11/configure-qt5-application-style-icons.html>`_

LockScreen/Logout/Suspend/Reboot/Shutdown
=========================================

Screen locks are handled by ``i3lock`` and ``systemctl`` deals with system suspend/reboot/shutdown ...

.. code-block:: bash

    # Lock/Logout/Suspend/Reboot/Shutdown                                           
    # * https://wiki.archlinux.org/index.php/I3#Shutdown.2C_reboot.2C_lock_screen   
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

Happy hacking!

Notes
-----

.. [1] My configs and scripts: `.i3/config <https://github.com/vonbrownie/dotfiles/blob/master/.i3/config>`_, statusbar (for my Chromebook) `.i3status.conf <https://github.com/vonbrownie/dotfiles/blob/master/.i3status.conf.chromebook>`_, `.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_, dual-display detect/config script `dldsply <https://github.com/vonbrownie/homebin/blob/master/dldsply>`_, some `xinit extras <https://github.com/vonbrownie/homebin/blob/master/xtra>`_, and `.gtkrc-2.0 <https://github.com/vonbrownie/dotfiles/blob/master/.gtkrc-2.0>`_ generated by running ``lxappearance``.
