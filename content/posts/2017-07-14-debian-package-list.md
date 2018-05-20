---
title: "Install (almost) the same list of Debian packages on multiple machines"
date: "2017-07-14"
publishDate: "2017-07-14"
tags:
  - debian
  - linux
  - shell
  - programming
  - homebin
slug: "debian-package-list"
---

**Scenario:** I have a whole bunch of packages installed on **Machine A** and I want to replicate that package selection on **Machine B**.

## Let's go!

Machine A serves as the original source of the list of packages.

## 0. Make

Generate the list ...

```bash
dpkg --get-selections > pkg-list
```

The `pkg-list` file now contains the list of installed Debian packages on Machine A. However I want to make a few changes (hence the "almost" in the title) to the list.

Delete entries for packages that have been installed then removed (marked as `deinstall`) ...

```bash
sed -i '/deinstall/d' pkg-list
```

I also delete entries for packages that I built myself (identified using [apt-show-versions](https://tracker.debian.org/pkg/apt-show-versions)) and are not available in the Debian package archives ...

```bash
ARRAY=( $(apt-show-versions | grep -v "stretch" | awk -F: '{print $1}') )
for package in "${ARRAY[@]}"
do
    sed -i "/$package/d" pkg-list
done
```

I made the [generatePkgList](https://github.com/vonbrownie/homebin/blob/master/generatePkgList) shell script to create modified package lists.

## 1. Install

Copy `pkg-list` to Machine B and update its `dpkg` database of known packages as root ...

```bash
avail=`mktemp`
apt-cache dumpavail > "$avail"
dpkg --merge-avail "$avail"
rm -f "$avail"
```

Update the `dpkg` selections ...

```bash
dpkg --set-selections < pkg-list
```

Use `apt-get` to install the selected packages ...

```bash
apt-get dselect-upgrade
```

Link: [Debian Administrator's Handbook - 6.2. aptitude, apt-get, and apt Commands](https://debian-handbook.info/browse/stable/sect.apt-get.html)

:penguin: *Part of the* [HOME slash bin](https://www.circuidipity.com/homebin/) *project*.

Happy hacking!
