---
title: "Minimal to Morebuntu"
date: "2016-05-01"
publishDate: "2016-05-01"
tags:
  - ubuntu
  - linux
  - i3
  - shell
  - programming
slug: "morebuntu"
---

<img style="float:right;" src="/img/ubuntu-crane-300.png" />

Start with a **minimal install of Ubuntu 16.04 "Xenial Xerus"** and roll a **Morebuntu** customized with the **i3 tiling window manager** plus a collection of desktop applications.

## Let's go!

I use Ubuntu's [minimal install image](https://help.ubuntu.com/community/Installation/MinimalCD) to create a console-only base configuration.

## 0. Minimal Ubuntu

**Start here:** A [visual walk-through of a sample Ubuntu setup](/ubuntu-trusty-install) that makes use of an entire storage device divided into 3 partitions: an unencrypted `root` partition, and encrypted `swap + home`.

## 1. Install X

After a successful first boot and network active ... setup the X environment ...

```bash
sudo apt install xorg xinput xbindkeys xbacklight xvkbd fonts-liberation ttf-ubuntu-font-family
sudo apt install rxvt-unicode-256color xfonts-terminus
```

## 2. Window Manager

**Lots** of choices! I like the [lightweight and delightful i3 window manager](/i3-tiling-window-manager), with the latest packages provided by the i3 project's [Ubuntu repository](https://i3wm.org/docs/repositories.html).

**Styling:** I use [Ambiance Colors](http://www.ravefinity.com/p/download-ambiance-radiance-colors.html) + [Vibrancy Color Icon](http://www.ravefinity.com/p/vibrancy-colors-gtk-icon-theme.html) themes. Download the `deb` packages and install with `sudo dpkg -i *.deb`.

Depends: `gtk2-engines-{murrine,pixbuf}` ...

```bash
sudo apt install gnome-themes-standard gtk2-engines-murrine gtk2-engines-pixbuf lxappearance qt4-qtconfig
```

Theming for QT5 apps can be configured using the `qt5ct` utility. Download the package [available on the WebUpd8 PPA](http://ppa.launchpad.net/nilarimogard/webupd8/ubuntu/pool/main/q/qt5ct/) and install.

## 3. Applications

Install some favourite desktop packages ...

* **editor** - `vim`
* **terminal** - `rxvt-unicode`, `tmux`
* **net** - `firefox`, `transmission-gtk`
* **multimedia** - `ubuntu-restricted-extras`, `vlc`, `rhythmbox` (with `--no-install-recommends`)
* **images** - `eog`, `scrot`, `geeqie`, `gimp`
* **docs** - `libreoffice`, `qpdfview`

```bash
sudo apt install vim rxvt-unicode tmux most
sudo apt --no-install-recommends install rhythmbox
sudo apt install pulseaudio pulseaudio-utils pavucontrol gstreamer1.0-pulseaudio alsa-utils sox
sudo apt install firefox default-jre icedtea-plugin transmission-gtk
sudo apt install ubuntu-restricted-extras ffmpeg rhythmbox-plugins vlc
sudo apt install eog scrot geeqie gimp gimp-help-en gimp-data-extras
sudo apt install libreoffice libreoffice-help-en-us libreoffice-gnome qpdfview
```

## 4. Update-alternatives

Configure symbolic links that determine default commands ...

```bash
sudo update-alternatives --config editor
sudo update-alternatives --config pager
sudo update-alternatives --config x-terminal-emulator
```

## 5. Morebuntu

My [morebuntu shell script](https://github.com/vonbrownie/linux-post-install/blob/master/scripts/morebuntu.sh) that covers most of steps 1-4.

Happy hacking!
