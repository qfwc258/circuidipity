=======================================================
Duplicate Debian package selection on multiple machines
=======================================================

:date: 2014-05-28 01:23:00
:slug: dpkg-duplicate
:tags: debian, linux, shell, programming, github

I am happy with the selection of packages installed on my `Debian-powered laptop <http://www.circuidipity.com/c720-sidbook.html>`_ and discovered an easy method to **duplicate** the configuration on another machine.

On the 'master' machine generate a list of installed packages...

.. code-block:: bash

    $ dpkg --get-selections | grep -v deinstall > deb-pkg-list.txt

Move the generated list to the target machine. Configure the package manager to duplicate the selection on the new system...

.. code-block:: bash

    $ PKGS=$(mktemp)
    $ sudo apt-cache dumpavail > "$PKGS"
    $ sudo dpkg --merge-avail "$PKGS"
    $ sudo rm -f "$PKGS"
    $ sudo dpkg --clear-selections
    $ sudo dpkg --set-selections < deb-pkg-list.txt
    $ sudo apt-get dselect-upgrade

I created a `shell script <https://github.com/vonbrownie/linux-home-bin/blob/master/dpkgDup>`_ that includes the above steps for generating and restoring package lists.

Happy hacking!

Sources: `dpkgDup <https://github.com/vonbrownie/linux-home-bin/blob/master/dpkgDup>`_, `Debian Administrator's Handbook <http://debian-handbook.info/browse/wheezy/sect.apt-get.html>`_
