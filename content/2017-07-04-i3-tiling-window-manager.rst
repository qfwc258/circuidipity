===================================================
Lightweight and a delight: i3 tiling window manager
===================================================

:modified: 2017-07-16 18:35:00
:date: 2017-07-04 09:17:00
:slug: i3-tiling-window-manager
:tags: i3, debian, linux

`PROJECT: The Lifecycle of Debian Objects .: <http://www.circuidipity.com/the-lifecycle-of-debian-objects.html>`_ As a former **Fluxbox** and **Openbox** user I can understand the love for a lightweight, minimal window manager where I can "paint" my applications across the screen. I was curious about `tiling window managers <https://en.wikipedia.org/wiki/Tiling_window_manager>`_ but never quite grokked the advantage from screenshots. Seeing consoles arranged in a grid made me think `tmux <http://www.circuidipity.com/tmux.html>`_ a better choice for that task, and why would I want to watch a video in a reduced square in the corner of a screen?

But then I tried `i3 <https://i3wm.org/>`_ and found my new desktop ...

* low memory requirements and `startx to X <http://www.circuidipity.com/xinitrc.html>`_  almost instantaneous on `Stretchbook <http://www.circuidipity.com/jessiebook-to-stretchbook.html>`_
* loads sensible defaults and - thanks to the excellent `User's Guide <https://i3wm.org/docs/userguide.html>`_ - easy to customize via text files
* toggle between **tiled**, **tabbed** (my default), **stacked**, and **floating** mode (see User's Guide)
* even if you rarely use applications in a tiled arrangement, i3 handles maximized windows, desktops, and multiple displays extremely well via keyboard

Still want to use a mouse here and here? No problem! Provides a **statusbar**, but you can swap it out for an `alternative <https://wiki.archlinux.org/index.php/I3#i3bar_alternatives>`_ or run none at all.

Install and configure on Debian ...

Let's go!
=========

Starting out I find myself mostly happy with the `default keybindings <https://i3wm.org/docs/userguide.html#_default_keybindings>`_ and behaviour; making only a few adjustments and additions to `my configuration <https://github.com/vonbrownie/dotfiles/blob/master/.config/i3/config.base>`_.

Install
-------

Download the **i3 metapackage** and a few desktop utilities ...

* **dunst** - lightweight notification daemon
* **volnoti** - volume notification (`built separately <http://www.circuidipity.com/pavolume.html#volnoti>`_)
* **rofi** - dynamic application launcher + window selector
* **nm-applet** - network monitor and control (provided by ``network-manager-gnome``)
* **scrot** - screenshots
* **lximage-qt** - image viewer
* **urxvt** - terminal

.. code-block:: bash

    $ sudo apt install i3 dunst rofi network-manager-gnome scrot lximage-qt rxvt-unicode-256color

Countdown to launch
-------------------

In my `~/.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_ I add a few tasks before launching the window manager.

Load config parameters for X client applications, disable screen blanking, and empty the trash ...

.. code-block:: bash

    # Config parameters for X client applications
    [ -f ~/.Xresources ] && xrdb -merge ~/.Xresources

    # Disable DPMS and turn off screen blanking
    xset s off -dpms

    # Janitor
    [ -d ~/.local/share/Trash ] && rm -rf ~/.local/share/Trash/*

Start applications ...

* **dldsply** - detect and - if present - configure a second display
* **i3wm_conf** - `build a config at runtime for i3wm <http://www.circuidipity.com/i3-tiling-window-manager.html#conditionals>`_
* **keyboardconf** - bind commands to keys and load key mappings
* **nm-applet** - network-manager utility
* **volnoti** - volume notification
* **urxvt** - terminal

.. code-block:: bash

    # Applications
    ~/bin/dldsply -r &
    ~/bin/i3wm_conf &
    ~/bin/keyboardconf &
    sleep 2
    [ -x /usr/bin/nm-applet ] && nm-applet &
    volnoti -t 2 &
    urxvt &

**Launch i3!**

.. code-block:: bash

    # Start window manager
    exec i3

Source for startup scripts: homebin/`dldsply <https://github.com/vonbrownie/homebin/blob/master/dldsply>`_; homebin/`i3wm_conf <https://github.com/vonbrownie/homebin/blob/master/i3wm_conf>`_; and homebin/`keyboardconf <https://github.com/vonbrownie/homebin/blob/master/keyboardconf>`_

Configuration
-------------

Window manager configuration file is ``~/.config/i3/config``, which i3 offers to generate at first launch. A few changes that I make from the i3 defaults ...

Windows and Workspaces
``````````````````````

Remove the default tabs from windows and replace them with thin coloured bars by reducing window title font size to zero ...

.. code-block:: bash

    font pango:monospace 0

... and set colours for windows ...

.. code-block:: bash

    # Colours
    # * class                 border  backgrd text    indicator
    client.focused            #3daee9 #3daee9 #ffffff #2e9ef4
    client.focused_inactive   #1cdc9a #1cdc9a #ffffff #484e50
    client.unfocused          #4d4d4d #4d4d4d #ffffff #292d2e
    client.urgent             #2f343a #900000 #ffffff #900000

Workspace defaults to a tabbed layout for windows, with hotkeys for toggling between different layouts ...

.. code-block:: bash

    # Layout mode
    workspace_layout tabbed

    # Change layout (stacked, tabbed, toggle split)
    bindsym $mod+s layout stacking
    bindsym $mod+w layout tabbed
    bindsym $mod+e layout toggle split

Styling
```````

**Breeze** is the default Qt style of KDE Plasma with good support for both Qt and GTK applications. More: `It is a Breeze to make QT and GTK applications look good <http://www.circuidipity.com/breeze-qt-gtk.html>`_

Applications
````````````

Create a hotkey to open terminals ...

.. code-block:: bash

	# Start a terminal
	bindsym $mod+Return exec urxvt

Before running the ``dunst`` notification daemon for the first time, create a default config ...

.. code-block:: bash

	$ zcat /usr/share/doc/dunst/dunstrc.example.gz > ~/.config/dunst/dunstrc

Start notifications and launcher in the background ...

.. code-block:: bash

	# Start dunst - lightweight notification-daemon
	exec --no-startup-id dunst -config ~/.config/dunst/dunstrc

	# Start rofi - window switcher, run dialog, and dmenu replacement
	bindsym $mod+F2 exec --no-startup-id rofi -monitor -1 -show run
	bindsym $mod+Tab exec --no-startup-id rofi -monitor -1 -show window

Create hotkeys for **screenshots** ...

.. code-block:: bash

	# Screenshots using scrot + lximage-qt
	# * desktop image
	bindsym --release Print exec --no-startup-id scrot \
	'%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && lximage-qt ~/Downloads/$f'
	bindsym --release $mod+F4 exec --no-startup-id scrot \
	'%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && lximage-qt ~/Downloads/$f'
	# * active window image
	bindsym --release Shift+Print exec --no-startup-id scrot -d 4 -u -z \
	'%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && lximage-qt ~/Downloads/$f'
	bindsym --release Shift+F4 exec --no-startup-id scrot -d 4 -u -z \
	'%Y-%m-%dT%H%M%S.png' -e 'mv $f ~/Downloads && lximage-qt ~/Downloads/$f'

`Automatically put clients on specific workspaces <https://i3wm.org/docs/userguide.html#assign_workspace>`_ ...

.. code-block:: bash

	# Assign torrent client to workspace 10
	assign [instance="transmission-qt"] 10
	# Assign music player to workspace 10
	assign [class="Rhythmbox"] 10

Volume control and notification is a combination of ``pavucontrol``, ``volnoti``, and `xbindkeys <http://www.circuidipity.com/xbindkeysrc.html>`_ linked together in a `shell script <http://www.circuidipity.com/pavolume.html>`_.

Lock/Logout/Suspend/Reboot/Shutdown
```````````````````````````````````

Screen locks are handled by ``i3lock``. Pick an image to serve as the lock splashscreen (example: ``~/.i3lock.png``). Command ``systemctl`` deals with system suspend/reboot/shutdown ...

.. code-block:: bash

	set $Locker i3lock -i ~/.i3lock.png && sleep 1
	set $mode_system System (l) lock, (e) logout, (s) suspend, (r) reboot, \
	(Shift+s) shutdown
	mode "$mode_system" {
    	bindsym l exec --no-startup-id $Locker, mode "default"
    	bindsym e exec --no-startup-id i3-msg exit, mode "default"
    	bindsym s exec --no-startup-id $Locker && sync && systemctl suspend, \
    	mode "default"
    	bindsym r exec --no-startup-id systemctl reboot, mode "default"
    	bindsym Shift+s exec --no-startup-id systemctl poweroff -i, mode "default"  
    	# back to normal: Enter or Escape
    	bindsym Return mode "default"
    	bindsym Escape mode "default"
	}
	bindsym $mod+Pause mode "$mode_system"

Link: `Shutdown, reboot, lock screen <https://wiki.archlinux.org/index.php/I3#Shutdown.2C_reboot.2C_lock_screen>`_

Conditionals
------------

The ``~/.config/i3/config`` file has no provision for interpreting conditionals, so I put my `default settings and conditions in separate files <https://github.com/vonbrownie/dotfiles/tree/master/.config/i3>`_ and generate an appropriate config at runtime using `i3wm_conf <https://github.com/vonbrownie/homebin/blob/master/i3wm_conf>`_.

**a) If two displays are detected** (laptop connected to external monitor) there is extra workspace configuration ...

.. code-block:: bash

	# Automatically place workspaces on specific displays
	# * external display =  PRIMARY
	# * laptop display =    SECOND
	workspace 1 output PRIMARY
	workspace 10 output SECOND

Customize the included ``i3bar`` statusbar by adding text-based information snippets configured in ``~/.config/i3/i3status.conf``: system tray, battery status, system load and temperature, and time.

Start ``i3bar`` on the external (primary) display and a `secondary statusbar <https://github.com/vonbrownie/dotfiles/blob/master/.config/i3/i3status-small.conf>`_ on the other display ...

.. code-block:: bash

	bar {
    	output PRIMARY
    	position top
    	status_command i3status --config ~/.config/i3/i3status.conf
    	font pango:Terminus 11px
    	colors {
        	focused_workspace #3daee9 #3daee9 #ffffff
        	inactive_workspace #4d4d4d #4d4d4d #ffffff
        	}
	}

	bar {
    	output SECOND
    	position top
    	tray_output none
    	status_command i3status --config ~/.config/i3/i3status-small.conf
    	font pango:Terminus 11px
    	colors {
        	focused_workspace #3daee9 #3daee9 #ffffff
        	inactive_workspace #4d4d4d #4d4d4d #ffffff
        	}
	}

**b) If only a single display** ... 

.. code-block:: bash

	bar {
    	position top
    	status_command i3status --config ~/.config/i3/i3status.conf
    	font pango:Terminus 11px
    	colors {
        	focused_workspace #3daee9 #3daee9 #ffffff
        	inactive_workspace #4d4d4d #4d4d4d #ffffff
        	}
	}

Onward
------

With some scripting and a few extra applications it all rolls together as a lightweight and delightful **custom desktop environment**!

Happy hacking!
