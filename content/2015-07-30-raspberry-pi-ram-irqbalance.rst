=========================================
Raspberry Pi RAM gobbled up by irqbalance
=========================================

:date: 2015-07-30 14:50:00
:slug: raspberry-pi-ram-irqbalance
:tags: raspberry pi, linux
:modified: 2015-08-04 16:34

**Problem:** After a few days uptime my Pi sees hundreds of MB gobbled up by the ``irqbalance`` daemon (which balances interrupts across multiple CPUs). Package version is ``1.0.6-3`` on Debian ``jessie/armhf`` and its a `known bug <https://bugs.launchpad.net/ubuntu/+source/irqbalance/+bug/1247107>`_.

**Fix:** **0)** Restart ``irqbalance`` in nightly cron job, or **1)** Compile and install a newer, patched version (my choice).

Remove buggy ``irqbalance``:

.. code-block:: bash

    $ sudo systemctl stop irqbalance                                                       
    $ sudo apt-get --purge remove irqbalance                                               

Install development tools on the Pi:

.. code-block:: bash

    $ sudo apt-get install build-essential autogen automake libtool pkg-config checkinstall
                                                                                     
`Download source <https://github.com/Irqbalance/irqbalance>`_ and unpack:

.. code-block:: bash

    $ wget https://github.com/Irqbalance/irqbalance/archive/v1.0.9.tar.gz && tar xvzf v1.0.9.tar.gz

**Checkinstall** is an easy way to make Debian packages for personal use. Compile and (check)install:

.. code-block:: bash

    $ cd irqbalance-1.0.9                                                                  
    $ /autogen.sh                                                                          
    $ ./configure                                                                          
    $ make                                                                                 
    $ sudo checkinstall make install

Start new ``irqbalance``:

.. code-block:: bash

    $ sudo /usr/local/sbin/irqbalance &

Optional: Configure the daemon for `systemd control and auto-start at boot <http://www.circuidipity.com/writing-systemd-service-files.html>`_.

I have been running the daemon for a few days now and it stays around 0.6% memory usage vs **20%** (and growing) of the previous packaged version.

Happy hacking!
