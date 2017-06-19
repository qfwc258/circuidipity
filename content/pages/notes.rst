=====
Notes
=====

:slug: notes

2017-06-19T0953
---------------

Configure menu colours in Grub by creating ``/boot/grub/custom.cfg`` with settings ...

.. code-block:: bash

    set color_normal=white/black
    set menu_color_normal=white/black
    set menu_color_highlight=white/green

2017-06-18T0949
---------------

Stop pulseaudio from respawning after halt (encountered in Ubuntu 16.04) ... When I kill pulseaudio with ``pulseaudio -k`` or ``kill -9 ID`` it immediately restarts ...

.. code-block:: bash

    $ pgrep pulse
    12808 /usr/bin/pulseaudio --start --log-target=syslog

**[ Fix! ]** There is a config file ``/etc/pulse/client.conf`` with ``autospawn = yes`` set by default. I could modify that, but chose instead to create ``~/.config/pulse/client.conf`` and set ``autospawn = no``. It works ... pulseaudio stays dead.

2017-06-17T0921
---------------

Start a new project in Git and host on Github (after setting up a default config in ``~/.gitconfig``) ...

.. code-block:: bash

    $ mkdir new_project
    $ cd new_project
    $ touch .gitignore
    $ touch README.rst      # using rst will allow github to auto-detect and configure it as a project homepage
    $ git init
    $ git add README.rst    #... or 'git add .' to add all files recursively
    $ git status
    $ git commit -a -m 'first commit'   # '-a' option auto-adds all files that are being tracked and commits them
    $ git log               # to view commit history

Connect with Github ...

.. code-block:: bash

    $ git remote add origin https://github.com/vonbrownie/sitrep.git  # connect my local repo to github for first time
    $ git remote -v  # confirm local knows about remote
    $ git push -u origin master

... and to pull in (download) changes from Github master ...

.. code-block:: bash

    $ git pull origin master

2017-06-16T0950
---------------

Stop pinned tabs from auto-loading upon Firefox startup. Goto ``about:config`` and set to **true** ...

.. code-block:: bash

    * browser.sessionstore.restore_pinned_tabs_on_demand    default boolean false

2017-06-15T0853
---------------

Debian _stretch_/stable ``xbacklight`` is acting up ...

.. code-block:: bash

	$ xbacklight -dec 10
	No outputs have backlight property

I **can** write to the file directly to increase/decreae display brightness ...

.. code-block:: bash

	$ cat /sys/class/backlight/intel_backlight/max_brightness 
	937
	$ sudo sh -c 'echo 500 > /sys/class/backlight/intel_backlight/brightness'
	$ sudo sh -c 'echo 937 > /sys/class/backlight/intel_backlight/brightness'

... or use ``xrandr`` ...

.. code-block:: bash

	$ xrandr --output eDP-1 --brightness 0.5

This is `a known issue. <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=833508>`_

**[ Fix! ]** Roll-back from ``xserver-xorg-core`` to ``xserver-xorg-video-intel``.

Create ``/etc/X11/xorg.conf.d/10-video-intel.conf`` containing ...

.. code-block:: bash

	Section "Device"
		Identifier "Intel"
		Driver "intel"
	EndSection

2017-06-14T2113
---------------

Trying to install Debian's ``flashplugin-nonfree`` package consistently fails with the error ....

.. code-block:: bash

    ERROR: wget failed to download http://people.debian.org/~bartm/flashplugin-nonfree/D5C0FC14/fp.24.0.0.221.sha512.amd64.pgp.asc

**[ Fix! ]** Manual install works courtesy of the instructions at https://wiki.debian.org/FlashPlayer#Manual_update

2017-06-14T0947
---------------

Setup colour scheme for vim. As per `Giles' <http://www.gilesorr.com/blog/>`_ recommendation I use `tir_black. <http://www.vim.org/scripts/script.php?script_id=2777>`_  Place in ``~/.vim/colors``.

Set as default colour scheme in ``init.vim`` ...

.. code-block:: bash

    colorscheme tir_black

Colour scheme works when neovim runs in terminal. Does *not* work inside tmux. Tmux is not seeing the 256 color palette ...

.. code-block:: bash

    $ tput colors
    8

**[ Fix! ]** Add to ``~/.tmux.conf`` ...

.. code-block:: bash

    set -g default-terminal "rxvt-unicode-256color"

**Note:** Kill all existing tmux sessions. It is not enough simply to start a fresh session. Helpful! http://stackoverflow.com/a/25940093

Launch a new tmux session. Neovim colours work OK!

.. code-block:: bash

    $ echo $TERM
    rxvt-unicode-256color
    $ tput colors
    256

2017-06-13T0847
---------------

Created a Debian _stretch_ virtualbox guest but ``virtualbox-guest-{dkms,utils,x11}`` packages no longer available ... but there *are* pkgs in `_sid_. <https://tracker.debian.org/pkg/virtualbox>`_

**[ Fix! ]** Install the _sid_ pkgs. Setup **apt-pinning** in ``/etc/apt/preferences`` ...

.. code-block:: bash

    Package: *
    Pin: release n=stretch
    Pin-Priority: 900

    Package: *
    Pin: release a=unstable
    Pin-Priority: 300

Add unstable to ``sources.list`` ...

.. code-block:: bash

    deb http://deb.debian.org/debian/ unstable main contrib non-free

Update and install ...

.. code-block:: bash

    # apt -t unstable install virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
    # adduser dwa vboxsf

2017-06-12T1041
---------------

Local install of Python modules as non-root user. Example ...

.. code-block:: bash

    $ pip3 install exifread
    
... libraries are installed to ``~/.local/lib/python-ver/`` and the bins are placed in ``~/.local/bin/``.

Add ``~/.local/bin`` to user's $PATH.

2017-06-11T1020
---------------

If SSH session is frozen ... Use the key-combo **Enter, Shift + `, .** [Enter, Tilde, Period]  to drop the connection.

2017-06-10T0838
---------------

Microphone problem on Thinkpad x230 running Ubuntu 16.04 ... No sound input and **mic** not detected.

**[ FIX! ]** Get capture device ...                                                          

.. code-block:: bash

	$ arecord -l                                                                         
	card 0: ... device 0: ...                                                            
                                                                                     
... and edit ``/etc/pulse/default.pa`` with ``load-module module-alsa-source device=hw:0,0``.

Kill and respawn pulseaudio ...

.. code-block:: bash
                                                        
	$ pulseaudio -k

2017-06-09T0941
---------------
Restart network service on Ubuntu ... Sometimes after wake-from-suspend the network connection is down and network-manager's wifi ap list fails to refresh.
                                                                                
**[ FIX! ]** Simple systemd way ...                                                   
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo systemctl restart NetworkManager.service                             
                                                                                
If that doesn't work ... Try using ``nmcli`` to stop and start network-manager directly ...
                                                                                
.. code-block:: bash                                                             
                                                                                
    $ sudo nmcli networking off                                                 
    $ sudo nmcli networking on                                                  
                                                                                
Old-fashioned SysV init script method still works on 16.04 ...                
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo /etc/init.d/networking restart                                       
        ... or ...                                                              
    $ sudo /etc/init.d/network-manager restart                                  
                                                                                
Last resort ...                                             
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo ifdown -a  # -a brings down all interfaces                           
    $ sudo ifup -a

2017-06-08T0920
---------------
Attaching to a wifi network with ``nmcli`` (network-manager cli client) ...

.. code-block:: bash

    $ nmcli radio
    $ nmcli device
    $ nmcli device wifi rescan
    $ nmcli device wifi connect SSID-Name password PASS

2017-06-07T1219
---------------
Disable `Pelican <http://www.circuidipity.com/tag-pelican.html>`_ from auto-generating ``archives.html`` by adding to ``pelicanconf.py`` ...

.. code-block:: bash

    ARCHIVES_SAVE_AS = ''

From `URL Settings <http://docs.getpelican.com/en/latest/settings.html#url-settings>`_: "If you do not want one or more of the default pages to be created ... set the corresponding ``*_SAVE_AS`` setting to '' to prevent the relevant page from being generated."
