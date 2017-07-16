======================================================================
Install (almost) the same list of Debian packages on multiple machines
======================================================================

:modified: 2017-07-16 18:35:00
:date: 2017-07-14 12:37:00
:slug: debian-package-list
:tags: debian, linux, shell, programming

`PROJECT: The Lifecycle of Debian Objects .: <http://www.circuidipity.com/the-lifecycle-of-debian-objects.html>`_ **Scenario:** I have a whole bunch of packages installed on **Machine A** and I want to replicate that package selection on **Machine B**.

Let's go!
=========

Machine A serves as the original source of the list of packages.

0. Make
-------

Generate the list ...

.. code-block:: bash

    $ dpkg --get-selections > pkg-list
    
The ``pkg-list`` file now contains the list of installed Debian packages on Machine A. However I want to make a few changes (hence the "almost" in the title) to the list.

Delete entries for packages that have been installed then removed (marked as ``deinstall``) ...

.. code-block:: bash

    $ sed -i '/deinstall/d' pkg-list
    
I also delete entries for packages that I built myself (identified using `apt-show-versions <https://tracker.debian.org/pkg/apt-show-versions>`_) and are not available in the Debian package archives ...

.. code-block:: bash

    ARRAY=( $(apt-show-versions | grep -v "stretch" | awk -F: '{print $1}') )
    for package in "${ARRAY[@]}"
    do
        sed -i "/$package/d" pkg-list
    done

I made the `generatePkgList <https://github.com/vonbrownie/homebin/blob/master/generatePkgList>`_ shell script to create modified package lists.

1. Install
----------

Copy ``pkg-list`` to Machine B and update its ``dpkg`` database of known packages ...

.. code-block:: bash

    # avail=`mktemp`
    # apt-cache dumpavail > "$avail"
    # dpkg --merge-avail "$avail"
    # rm -f "$avail"

Update the ``dpkg`` selections ...

.. code-block:: bash

    # dpkg --set-selections < pkg-list

Use ``apt-get`` to install the selected packages ...

.. code-block:: bash

    # apt-get dselect-upgrade

Link: `Debian Administrator's Handbook - 6.2. aptitude, apt-get, and apt Commands <https://debian-handbook.info/browse/stable/sect.apt-get.html>`_

Happy hacking!
