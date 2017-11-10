---
title: "It is a Breeze to make QT and GTK applications look good"
date: "2017-07-03"
publishDate: "2017-07-03"
tags:
  - qt
  - gtk
  - linux
slug: "breeze-qt-gtk"
---

I went looking for a desktop style with good support for both Qt and GTK applications. **Breeze** is the default Qt style of KDE Plasma and the one I chose. I like it!

To setup on Debian ...

## Let's go!

Install the `breeze` package for Qt and `gtk3-engines-breeze` for GTK ...

```bash
sudo apt install breeze gtk3-engines-breeze
```

I am [not running KDE](http://www.circuidipity.com/i3-tiling-window-manager) or any other desktop environment, so I install a few independent configuration tools:

* `qt5ct` for Qt5 (package built from [mentors.debian.net](http://www.circuidipity.com/build-qt5ct.html))
* `qt4-qtconfig` for Qt4
* `lxappearance` for Gtk2 and Gtk3

```bash
sudo apt install qt4-qtconfig lxappearance
```

Run each config tool for its respective environment. Settings are saved to:

* `~/.config/qt5ct/qt5ct.conf` for Qt5
* `~/.config/Trolltech.conf` for Qt4
* `~/.config/gtk-3.0/settings.ini` for Gtk3
* `~/.gtkrc-2.0` for Gtk2

**Breeze-dark** is an alternative dark colour scheme. Qt5ct handles colours separately from KDE. Create or modify an existing colour scheme and save with a filename ending in `.conf` to `~/.config/qt5ct/colors`. I use [this one posted on GitHub](https://github.com/wicast/dotfiles/blob/master/qt5ct/.config/qt5ct/colors/BreezeDark.conf). Run `qt5ct` and in `Appearance` select the new custom colour scheme. Select `breeze-dark` in the other config tools.

I add to my `~/.bashrc` (which is sourced by `~/.profile`) ...

```bash
export QT_QPA_PLATFORMTHEME=qt5ct
```

Using a dark theme created a problem for me in Firefox with text entry on some websites. Gmail login, Youtube search, and others would use a near-invisible white font on a white background. **Text Contrast for Dark Themes** is a [Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/text-contrast-for-dark-themes) that fixed the issue. Good stuff!

Links: [Uniform_look_for_Qt_and_GTK_applications](https://wiki.archlinux.org/index.php/Uniform_look_for_Qt_and_GTK_applications) and [Configuration of Qt5 apps under environments other than KDE Plasma](https://wiki.archlinux.org/index.php/Qt#Configuration_of_Qt5_apps_under_environments_other_than_KDE_Plasma)

Happy hacking!
