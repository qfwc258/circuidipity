---
title: "Debian _stable_ setup"
date: "2017-06-18"
publishDate: "2017-06-18"
tags:
  - debian
  - linux
  - shell
  - programming
slug: "debian-stable-setup"
---

![Debian stretch](/img/debian_9_banner.png)

## SYNOPSIS

```bash
    debian-stable-setup.sh [ options ] USER
```

## OPTIONS

```bash

    -h              print details
    -b              basic setup (console only)
    -p PKG_LIST     install packages from PKG_LIST
```

## EXAMPLE

Post-install setup of a machine running Debian _stable_ release  for (existing) USER 'foo' ...

```bash
sudo ./debian-stable-setup.sh foo
```

Install packages from 'pkg-list' ...

```bash
sudo ./debian-stable-setup.sh -p pkg-list foo
```

## DESCRIPTION

Script **debian-stable-setup.sh** is ideally run immediately following the first successful boot into your new Debian installation.

Building on a [minimal install](http://www.circuidipity.com/minimal-debian) the system will be configured to track Debian's _stable_ release. A choice of either ...

1) a basic console setup; or
2) a more complete setup which includes the [i3 tiling window manager](http://www.circuidipity.com/i3-tiling-window-manager) plus a packages collection suitable for a workstation; or
3) install the [same list of packages as PKG_LIST](http://www.circuidipity.com/debian-package-list)

... will be installed.

## USE

**0.** Install program folder on target machine.

**1.** Copy `config.sample` to `config` and (optional) enable settings. All settings are **disabled** by default.

**2.** Run program!

## DEPENDS

`bash`

Source: [debian-stable-setup](https://github.com/vonbrownie/linux-post-install/tree/master/scripts/debian-stable-setup)

Happy hacking!
