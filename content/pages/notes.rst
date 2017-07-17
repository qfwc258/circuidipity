=====
Notes
=====

:slug: notes

N2017-07-17T09:41
-----------------

`Linuxlogo <http://www.deater.net/weave/vmwprod/linux_logo/>`_ provides Tux, the Debian swirl, and other distro logos that can be displayed - along with system information - at the console login prompt ...

.. code-block:: bash
    
    $ sudo apt-get install linuxlogo
    $ sudo cp /etc/issue /etc/issue.bak
    $ sudo sh -c 'linux_logo -L debian -F ".: Greetings, Carbon-Based Biped :.\n\n#O Version #V\nCompiled #C\n#H \\l" > /etc/issue'

N2017-07-14T15:38
-----------------

Correct the 'stripping effect' in QT applications using the **Breeze Dark** theme. Example: Transmission-qt would show file listings in alternating background colours, with every other line rendered in light background and foreground colours.

**[ Fix! ]** Offending colour is ``#eff0f1``. Replaced with ``#404552`` in ``~/.config/qt5ct/colors/breeze_dark.conf``.

N2017-07-13T09:16
-----------------

Retrieving Debian release information (depending on what I want) ...

* ``/etc/debian_version``
* ``/etc/os-release``
* ``lsb_release -c``

N2017-07-10T18:46
-----------------

Assign user to new group and reload assignments without logging out ...

.. code-block:: bash

    $ su - $USER
    $ id        # see the new group
    
Link: https://superuser.com/a/354475

N2017-07-09T08:07
-----------------

**Nmap** will quickly identify Internet services hosted by a network connected machine without even requiring to log in to it. Simply call the following command on another machine connected to the same network ...

.. code-block:: bash

    $ nmap 192.168.1.88
    
Link: `DAH: 3.2.1.1. Network and Processes <https://debian-handbook.info/browse/stable/sect.how-to-migrate.html>`_

N2017-07-06T08:57
-----------------

Use ``apt-show-versions`` to check list of installed packages and available versions. Good way to quickly grep which packages are **not** part of the default release.

Install ...

.. code-block:: bash

    $ sudo apt install apt-show-versions
    
Release is ``stretch`` ...

.. code-block:: bash

    $ apt-show-versions | grep -v stretch
    qt5ct:amd64 0.31-2 installed: No available version in archive
	volnoti:amd64 20161215T1244-1 installed: No available version in archive

N2017-07-03T09:00
-----------------

Configure i3wm to put clients on specific workspaces. Run ``xprop`` in a terminal and click on the client to get ``WM_CLASS``: first part is the **instance**, second part is the **class** ...

.. code-block:: bash

    $ xprop
    [...]
    WM_CLASS(STRING) = "transmission-qt", "transmission"
    
Add the change to ``~/.config/i3/config`` ...

.. code-block:: bash

    # Assign torrent client to workspace 10
    assign [instance="transmission-qt"] 10
    
Link: `Automatically putting clients on specific workspaces <https://i3wm.org/docs/userguide.html#assign_workspace>`_

N2017-07-02T10:14
-----------------

Addon for Firefox: `Text Contrast for Dark Themes <https://addons.mozilla.org/en-US/firefox/addon/text-contrast-for-dark-themes/>`_

Fixs issue with text entry on some websites (white text on white in gmail signin, yahoo search, others) when using the **Breeze Dark** QT theme.

N2017-06-29T12:37
-----------------

Find and replace text with **sed**.

Save back to the original file ...

.. code-block:: bash

    $ sed -i 's/original/new/g' file.txt
    
Save to new_file.txt ...

.. code-block:: bash

    $ sed 's/original/new/g' file.txt > new_file.txt
    
Multiple text patterns and variables ...

.. code-block:: bash

    $ sed "s/$original/$new/g; s/$pattern2/$new_again/g" file.txt > new_file.txt
    
Link: https://askubuntu.com/q/20414

N2017-06-28T15:12
-----------------

Lots of documentation and config samples are available in ``/usr/share/doc`` in gzip'ed format. Non-root user access with the ``zcat`` and ``zless`` commands. Make use of a config sample by redirecting output. Example ...

.. code-block:: bash

    $ zcat /usr/share/doc/dunst/dunstrc.example.gz > ~/.config/dunst/dunstrc

N2017-06-27T09:02
-----------------

Default keyboard layout in Debian is configured in ``/etc/default/keyboard`` and is shared between X and the command line ...

.. code-block:: bash

    $ cat /etc/default/keyboard
    [...]
    XKBMODEL="pc105"
    XKBLAYOUT="us"
    XKBVARIANT=""
    XKBOPTIONS=""

    BACKSPACE="guess"

Modify this file to set a new default keyboard layout, either manually or run ...

.. code-block:: bash

    $ sudo dpkg-reconfigure keyboard-configuration

N2017-06-26T11:26
-----------------

Limit the CPU usage of an application ... I tried using **handbrake-gtk** to convert a video and the application grabbed 100% of all 4 cores, sent system temperature to 98C, and finally crashed the machine.

**[ Fix! ]** Install **cpulimit** and set the limit to 80 (20percent * 4 cores) ...

.. code-block:: bash

    $ sudo cpulimit -e ghb -l 80


N2017-06-25T09:22
-----------------

Firework sounds for upcoming Canada Day!

.. code-block:: bash

    $ sudo apt install sox

Screamer ...

.. code-block:: bash

    $ play -n synth sine 8000 bend 0.5,-1800,5 flanger 0 3 0 20 10 tri 20 quad trim 0 7

Bottle rocket ...

.. code-block:: bash

    $ play -n synth whitenoise 200 fade 0.2 1 1 trim 0 0.5 ; sleep 1 ; play -n synth whitenoise 200 fade 0 1 1 trim 0 1

Links: https://twitter.com/climagic/status/485083242425368579 and https://twitter.com/climagic/status/485069251401629697

N2017-06-24T0:844
-----------------

Retrieve information about hardware using ``sudo dmidecode``, or much of the same information is available to the non-root user in ``/sys/devices/virtual/dmi/id``.

Link: https://unix.stackexchange.com/a/172334

N2017-06-23T10:01
-----------------

Switch from default qwerty to the colemak keyboard layout ...

.. code-block:: bash

    $ setxkbmap -query
    rules:      evdev
    model:      pc105
    layout:     us
    $ setxkbmap us -variant colemak
    $ setxkbmap -query
    rules:      evdev
    model:      pc105
    layout:     us
    variant:    colemak

N2017-06-22T10-36
-----------------

Generate list of packages installed on one machine running Debian for installation on another machine.

List of packages on first machine ...

.. code-block:: bash

    $ sudo dpkg --get-selections | grep -v deinstall > deb-pkg-list.txt

Install packages on the second machine ...

.. code-block:: bash

    $ sudo apt install dselect
    $ sudo dselect update    # update dselect database
    $ sudo dpkg --set-selections < deb-pkg-list.txt
    $ sudo apt dselect-upgrade

N2017-06-21T08:32
-----------------

VLC not playing mkv files on the chromebook. Generates error message ...

.. code-block:: bash

    libvdpau-va-gl: Decoder::Render_h264(): no surfaces left in buffer

**[ Fix! ]** In VLC navigated to ``Tools->Preferences->Input/Codecs`` and for **Hardware-accelerated decoding** switched to ``VA-API video decoder via x11`` instead of using ``VDPAU``. Or set ``avcodec-hw=vaapi_x11`` in ``~/.config/vlc/vlcrc``.

Link: https://askubuntu.com/questions/714363/intel-vaapi-cant-play-mkv-with-vlc

N2017-06-20T09:26
-----------------

Clearing the shell cache ... I originally installed ``glances`` via apt to ``/usr/bin/glances``, then removed, then installed via pip to ``/usr/local/bin/glances``. The command would show in PATH but - without an explicit path defined - would continue to try and execute from ``/usr/bin``.

**[ Fix! ]**  Bash caches commands. Clear the cache of paths to executables using ``hash`` ...

.. code-block:: bash

    $ type glances
    glances is hashed (/usr/bin/glances)
    $ hash -d glances
    $ type glances
    glances is /usr/local/bin/glances

N2017-06-19T09:53
-----------------

Configure menu colours in Grub by creating ``/boot/grub/custom.cfg`` with settings ...

.. code-block:: bash

    set color_normal=white/black
    set menu_color_normal=white/black
    set menu_color_highlight=white/green

N2017-06-18T09:49
-----------------

Stop pulseaudio from respawning after halt (encountered in Ubuntu 16.04) ... When I kill pulseaudio with ``pulseaudio -k`` or ``kill -9 ID`` it immediately restarts ...

.. code-block:: bash

    $ pgrep pulse
    12808 /usr/bin/pulseaudio --start --log-target=syslog

**[ Fix! ]** There is a config file ``/etc/pulse/client.conf`` with ``autospawn = yes`` set by default. I could modify that, but chose instead to create ``~/.config/pulse/client.conf`` and set ``autospawn = no``. It works ... pulseaudio stays dead.

N2017-06-17T09:21
-----------------

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

N2017-06-16T09:50
-----------------

Stop pinned tabs from auto-loading upon Firefox startup. Goto ``about:config`` and set to **true** ...

.. code-block:: bash

    * browser.sessionstore.restore_pinned_tabs_on_demand    default boolean false

N2017-06-15T08:53
-----------------

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

N2017-06-14T21:13
-----------------

Trying to install Debian's ``flashplugin-nonfree`` package consistently fails with the error ....

.. code-block:: bash

    ERROR: wget failed to download http://people.debian.org/~bartm/flashplugin-nonfree/D5C0FC14/fp.24.0.0.221.sha512.amd64.pgp.asc

**[ Fix! ]** Manual install works courtesy of the instructions at https://wiki.debian.org/FlashPlayer#Manual_update

N2017-06-14T09:47
-----------------

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

N2017-06-13T08:47
-----------------

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

N2017-06-12T10:41
-----------------

Local install of Python modules as non-root user. Example ...

.. code-block:: bash

    $ pip3 install exifread
    
... libraries are installed to ``~/.local/lib/python-ver/`` and the bins are placed in ``~/.local/bin/``.

Add ``~/.local/bin`` to user's $PATH.

N2017-06-11T10:20
-----------------

If SSH session is frozen ... Use the key-combo **Enter, Shift + `, .** [Enter, Tilde, Period]  to drop the connection.

N2017-06-10T08:38
-----------------

Microphone problem on Thinkpad x230 running Ubuntu 16.04 ... No sound input and **mic** not detected.

**[ Fix! ]** Get capture device ...                                                          

.. code-block:: bash

	$ arecord -l                                                                         
	card 0: ... device 0: ...                                                            
                                                                                     
... and edit ``/etc/pulse/default.pa`` with ``load-module module-alsa-source device=hw:0,0``.

Kill and respawn pulseaudio ...

.. code-block:: bash
                                                        
	$ pulseaudio -k

N2017-06-09T09:41
-----------------

Restart network service on Ubuntu ... Sometimes after wake-from-suspend the network connection is down and network-manager's wifi ap list fails to refresh.
                                                                                
**[ Fix! ]** Simple systemd way ...                                                   
                                                                                
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

N2017-06-08T09:20
-----------------

Attaching to a wifi network with ``nmcli`` (network-manager cli client) ...

.. code-block:: bash

    $ nmcli radio
    $ nmcli device
    $ nmcli device wifi rescan
    $ nmcli device wifi connect SSID-Name password PASS

N2017-06-07T12:19
-----------------

Disable `Pelican <http://www.circuidipity.com/tag-pelican.html>`_ from auto-generating ``archives.html`` by adding to ``pelicanconf.py`` ...

.. code-block:: bash

    ARCHIVES_SAVE_AS = ''

From `URL Settings <http://docs.getpelican.com/en/latest/settings.html#url-settings>`_: "If you do not want one or more of the default pages to be created ... set the corresponding ``*_SAVE_AS`` setting to '' to prevent the relevant page from being generated."
