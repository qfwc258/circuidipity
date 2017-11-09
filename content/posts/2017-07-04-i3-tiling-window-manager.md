---
title: "Lightweight and a delight: i3 tiling window manager"
date: "2017-07-04"
publishDate: "2017-07-04"
tags:
  - i3
  - linux
slug: "i3-tiling-window-manager"
aliases:
  - /i3-tiling-window-manager.html
---

As a former *Fluxbox* and *Openbox* user I can understand the love for a lightweight, minimal window manager where I can "paint" my applications across the screen. I was curious about [tiling window managers](https://en.wikipedia.org/wiki/Tiling_window_manager) but never quite grokked the advantage from screenshots. Seeing consoles arranged in a grid made me think [tmux](http://www.circuidipity.com/tmux) a better choice for that task, and why would I want to watch a video in a reduced square in the corner of a screen?

But then I tried [i3](https://i3wm.org/) and found my new desktop:

* low memory requirements and [startx to X](http://www.circuidipity.com/xinitrc.html) almost instantaneous
* loads sensible defaults and - thanks to the excellent [User's Guide](https://i3wm.org/docs/userguide.html) - easy to customize via text files
* toggle between **tiled**, **tabbed** (my default), **stacked**, and **floating** mode (see User's Guide)
* even if you rarely use applications in a tiled arrangement, i3 handles maximized windows, desktops, and multiple displays extremely well via keyboard

Still want to use a mouse here and here? No problem! Provides a **statusbar**, but you can swap it out for an [alternative](https://wiki.archlinux.org/index.php/I3#i3bar_alternatives) or run none at all.

Install and configure on Debian/Ubuntu ...

## Let's go!

Starting out I find myself mostly happy with the [default keybindings](https://i3wm.org/docs/userguide.html#_default_keybindings) and behaviour; making only a few adjustments and additions to [my configuration](https://github.com/vonbrownie/dotfiles/blob/master/.config/i3/config.base).

## Install

Download the **i3 metapackage** and a few desktop utilities:

* **dunst** - lightweight notification daemon
* **volnoti** - volume notification ([built separately](http://www.circuidipity.com/pavolume.html#volnoti))
* **rofi** - dynamic application launcher + window selector
* **nm-applet** - network monitor and control (provided by `network-manager-gnome`)
* **scrot** - screenshots
* **lximage-qt** - image viewer
* **urxvt** - terminal

```bash
sudo apt install i3 dunst rofi network-manager-gnome scrot lximage-qt rxvt-unicode-256color
```

## Countdown to launch

In my [~/.xinitrc](https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc) I add a few tasks before launching the window manager.

Load config parameters for X client applications, disable screen blanking, and empty the trash ...

```bash
# Config parameters for X client applications
[ -f ~/.Xresources ] && xrdb -merge ~/.Xresources

# Disable DPMS and turn off screen blanking
xset s off -dpms

# Janitor
[ -d ~/.local/share/Trash ] && rm -rf ~/.local/share/Trash/*
```

:penguin: [$HOME Slash Bin](http://www.circuidipity.com/homebin/) :: Start applications ...

* **dldsply** - detect and - if present - configure a second display
* **i3wm_conf** - [build a config at runtime for i3wm](http://www.circuidipity.com/i3-tiling-window-manager.html#conditional)
* **keyboardconf** - bind commands to keys and load key mappings
* **nm-applet** - network-manager utility
* **volnoti** - volume notification
* **urxvt** - terminal

```bash
# Applications
~/bin/dldsply -r &
~/bin/i3wm_conf &
~/bin/keyboardconf &
sleep 2
[ -x /usr/bin/nm-applet ] && nm-applet &
volnoti -t 2 &
urxvt &
```

**Launch i3!**

```bash
# Start window manager
exec i3
```

Source for startup scripts: [dldsply](https://github.com/vonbrownie/homebin/blob/master/dldsply), [i3wm_conf](https://github.com/vonbrownie/homebin/blob/master/i3wm_conf), and [keyboardconf](https://github.com/vonbrownie/homebin/blob/master/keyboardconf)

## Configuration

Window manager configuration file is `~/.config/i3/config`, which i3 offers to generate at first launch. A few changes that I make from the i3 defaults ...

### Windows and Workspaces

Remove the default tabs from windows and replace them with thin coloured bars by reducing window title font size to zero ...

```bash
font pango:monospace 0
```

... and set colours for windows ...

```bash
# Colours
# * class                 border  backgrd text    indicator
client.focused            #3daee9 #3daee9 #ffffff #2e9ef4
client.focused_inactive   #1cdc9a #1cdc9a #ffffff #484e50
client.unfocused          #4d4d4d #4d4d4d #ffffff #292d2e
client.urgent             #2f343a #900000 #ffffff #900000
```

Workspace defaults to a tabbed layout for windows, with hotkeys for toggling between different layouts ...

```bash
# Layout mode
workspace_layout tabbed

# Change layout (stacked, tabbed, toggle split)
bindsym $mod+s layout stacking
bindsym $mod+w layout tabbed
bindsym $mod+e layout toggle split
```

### Styling

**Breeze** is the default Qt style of KDE Plasma with good support for both Qt and GTK applications. More: [It is a Breeze to make QT and GTK applications look good](http://www.circuidipity.com/breeze-qt-gtk.html)

### Applications

Create a hotkey to open terminals ...

```bash
# Start a terminal
bindsym $mod+Return exec urxvt
```

Before running the `dunst` notification daemon for the first time, create a default config ...

```bash
zcat /usr/share/doc/dunst/dunstrc.example.gz > ~/.config/dunst/dunstrc
```

Start notifications and launcher in the background ...

```bash
# Start dunst - lightweight notification-daemon
exec --no-startup-id dunst -config ~/.config/dunst/dunstrc

# Start rofi - window switcher, run dialog, and dmenu replacement
bindsym $mod+F2 exec --no-startup-id rofi -monitor -1 -show run
bindsym $mod+Tab exec --no-startup-id rofi -monitor -1 -show window
```

Create hotkeys for **screenshots** ...

```bash
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
```

[Automatically put clients on specific workspaces](https://i3wm.org/docs/userguide.html#assign_workspace) ...

```bash
# Assign torrent client to workspace 10
assign [instance="transmission-qt"] 10
# Assign music player to workspace 10
assign [class="Rhythmbox"] 10
```

Volume control and notification is a combination of `pavucontrol`, `volnoti`, and [xbindkeys](http://www.circuidipity.com/xbindkeysrc) linked together in a [shell script](http://www.circuidipity.com/pavolume).

### Lock/Logout/Suspend/Reboot/Shutdown

Screen locks are handled by `i3lock`. Pick an image to serve as the lock splashscreen (example: `~/.i3lock.png`). Command `systemctl` deals with system suspend/reboot/shutdown ...

```bash
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
```

Link: [Shutdown, reboot, lock screen](https://wiki.archlinux.org/index.php/I3#Shutdown.2C_reboot.2C_lock_screen)

## Conditionals

The `~/.config/i3/config` file has no provision for interpreting conditionals, so I put my [default settings and conditions in separate files](https://github.com/vonbrownie/dotfiles/tree/master/.config/i3) and generate an appropriate config at runtime using [i3wm_conf](https://github.com/vonbrownie/homebin/blob/master/i3wm_conf).

**a) If two displays are detected** (laptop connected to external monitor) there is extra workspace configuration ...

```bash
# Automatically place workspaces on specific displays
# * external display =  PRIMARY
# * laptop display =    SECOND
workspace 1 output PRIMARY
workspace 10 output SECOND
```

Customize the included `i3bar` statusbar by adding text-based information snippets configured in `~/.config/i3/i3status.conf`: system tray, battery status, system load and temperature, and time.

Start `i3bar` on the external (primary) display and a [secondary statusbar](https://github.com/vonbrownie/dotfiles/blob/master/.config/i3/i3status-small.conf) on the other display ...

```bash
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
```

**b) If only a single display** ... 

```bash
bar {
    position top
    status_command i3status --config ~/.config/i3/i3status.conf
    font pango:Terminus 11px
    colors {
        	focused_workspace #3daee9 #3daee9 #ffffff
        	inactive_workspace #4d4d4d #4d4d4d #ffffff
        	}
}
```

## Onward

With some scripting and a few extra applications it all rolls together as a lightweight and delightful **custom desktop environment**!

Happy hacking!
