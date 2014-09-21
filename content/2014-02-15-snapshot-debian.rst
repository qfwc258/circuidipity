===============
Snapshot Debian
===============

:date: 2014-02-15 01:23:00
:slug: snapshot-debian
:tags: debian, linux

Debian's `snapshot archive <http://snapshot.debian.org/>`_ is a collection of every past and current Debian package searchable by name and version number. Perhaps a ``dist-upgrade`` has messed up a package and a fix is not readily available? It is possible courtesy of this archive to download and install a previous version.

*Example:* I am using the latest 64-bit kernel offered by Debian ``linux-image-3.12-1-amd64`` and I can find all the previous ``linux-image-VERSION-ARCHITECTURE`` packages at http://snapshot.debian.org/binary/?cat=l. If I click on my `kernel package <http://snapshot.debian.org/binary/linux-image-3.12-1-amd64/>`_ it lists the different versions available and I can select a ``deb`` binary for download and install with ``dpkg -i linux-image-*.deb``.
