=====================================
Duplicate package selection in Debian
=====================================

:date: 2014-05-28 01:23:00
:slug: dpkg-duplicate
:tags: debian, linux, install, shell
:modified: 2015-07-06 13:25

I am happy with the selection of packages installed on my primary Debian box and discovered an easy method [1]_ to duplicate the setup on a secondary machine.

Generate a list of installed packages on the original:

.. code-block:: bash

    $ dpkg --get-selections | grep -v deinstall > pkg-list.txt

Move the generated list to the target machine. Configure the package manager [2]_ to duplicate the selection:

.. code-block:: bash

    $ PKGS=$(mktemp)
    $ sudo apt-cache dumpavail > "$PKGS" && sudo dpkg --merge-avail "$PKGS" && sudo rm "$PKGS"
    $ sudo dpkg --clear-selections && sudo dpkg --set-selections < pkg-list.txt
    $ sudo apt-get dselect-upgrade

Happy hacking!

Notes
-----

.. [1] Source: `Debian Administrator's Handbook <http://debian-handbook.info/browse/wheezy/sect.apt-get.html>`_
.. [2] Added an option to supply [PACKAGE_LIST] to my `debian-post-install script <https://github.com/vonbrownie/linux-post-install/blob/master/scripts/debian-post-install.sh>`_
