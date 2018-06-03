---
title: "Command line tools: Debian -stable- setup"
date: "2018-06-03"
publishDate: "2017-06-18"
tags:
  - debian
  - linux
  - shell
  - programming
  - projects
slug: "debian-stable-setup"
---

I created a *Debian setup script* - [debian-stable-setup.sh](https://github.com/vonbrownie/linux-post-install/blob/master/scripts/debian-stable-setup/debian-stable-setup.sh) - that is ideally run immediately following the first successful boot into a [minimal install](https://www.circuidipity.com/minimal-debian/) of Debian's _stable_ (code-named _stretch_) release.

A choice of either a **workstation** or **server** setup is available. *Server* is a basic console setup, whereas the *workstation* choice is a more extensive configuration using the lightweight [Openbox](https://www.circuidipity.com/openbox/) window manager and a range of desktop applications.

Alternately, in lieu of a pre-defined list of Debian packages, the user may specify their own [custom list of packages](https://www.circuidipity.com/debian-package-list/) to be installed.

**Script tasks include:**

<img style="float:right;" src="/img/debian-stable-setup.png" />

* Add `backports` repository, update package list, [upgrade packages](https://www.circuidipity.com/minimal-debian/#8-main-non-free-contrib-and-backports).
* [Install SSH server]( https://www.circuidipity.com/ssh-keys/), create `$HOME/.ssh`.
* Enable [periodic TRIM](https://www.circuidipity.com/minimal-debian/#11-ssd) on SSD drives. Create a weekly TRIM job.
* [GRUB extras](https://www.circuidipity.com/grub/): Add a bit of colour, a bit of sound, and wallpaper!
* Modify [/etc/sudoers.d/](https://www.circuidipity.com/minimal-debian/#10-sudo) to allow sudo group members extra privileges.
* Configure [automatic security updates](https://www.circuidipity.com/unattended-upgrades/).
* [Replicate list of packages](https://www.circuidipity.com/debian-package-list/) from one machine to another.
* Install *console* packages, including:
    * Editor: `neovim`
    * Multiplexer: `tmux`
* Install *server* packages, including:
    * Security: `fail2ban`
    * Log analyser: `logwatch`
* Install X environment and *Openbox*.
* Setup the *Arc* theme for Openbox, GTK2+3, and QT; *Papirus* icons; *Ubuntu* fonts.
* Install *desktop* packages, including:
    * Terminal: `urxvt`
    * Video: `vlc`
    * Audio: `rhythmbox`
    * PDF: `qpdfview`
    * Graphics: `gimp`
    * Office: `libreoffice`
    * Torrents: `transmission`
    * Network: `network-manager`
* Download and [install latest Firefox](https://www.circuidipity.com/notes/#2018-05-10t2212) in `$HOME/opt`.

![Debian stretch](/img/debian_9_banner.png)

### NAME

debian-stable-setup.sh - Setup a machine running the Debian _stable_ release

### SYNOPSIS

`debian-stable-setup.sh [OPTION]`

### OPTIONS

```bash
-h              print details
-p PKG_LIST     install packages from PKG_LIST
```

### EXAMPLES

Run script (requires superuser privileges) ...

```bash
./debian-stable-setup.sh
```

Install the list of packages specified in `my-pkg-list` ...

```bash
./debian-stable-setup.sh -p my-pkg-list
```

### SOURCE

[debian-stable-setup](https://github.com/vonbrownie/linux-post-install/tree/master/scripts/debian-stable-setup)

Happy hacking!
