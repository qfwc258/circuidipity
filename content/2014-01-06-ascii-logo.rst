==============================
Add ascii logo to login prompt
==============================

:date: 2014-01-06 01:23:00
:tags: debian, linux
:slug: ascii-logo

`Linuxlogo <http://www.deater.net/weave/vmwprod/linux_logo/>`_ provides Tux, the Debian swirl, and other distro logos that can be displayed - along with system information - at the console login prompt:

.. code-block:: bash
    
    $ sudo apt-get install linuxlogo
    $ sudo cp /etc/issue /etc/issue.bak
    $ sudo sh -c 'linux_logo -L debian -F ".: Greetings, Carbon-Based Biped :.\n\n#O Version #V\nCompiled #C\n#H \\l" > /etc/issue'
