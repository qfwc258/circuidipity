=====================================
Dual display configuration in Lubuntu
=====================================

:date: 2014-11-10 15:11:00
:slug: dual-display-lubuntu
:tags: graphics, lxde, lubuntu, ubuntu, linux, lenovo, thinkpad

**Scenario:** I connect my **Thinkpad X201** running Lubuntu and **LXDE** (resolution: ``1280x800``) to an external display (resolution: ``1920x1200``) to create: 1) a combined desktop; 2) with **lxpanel** top aligned and stretched across both displays; 3) and a different wallpaper on each display.

Let's go!
=========

0. Xrandr
---------

Output information about connected display devices and supported resolutions using **Xrandr**:

.. code-block:: bash

    $ xrandr
    Screen 0: minimum 320 x 200, current 3200 x 1200, maximum 32767 x 32767
    LVDS1 connected 1280x800+0+0 (normal left inverted right x axis y axis) 261mm x 163mm
        1280x800       60.0*+   50.1  
        1024x768       60.0  
        800x600        60.3     56.2  
        640x480        59.9  
    VGA1 connected primary 1920x1200+1280+0 (normal left inverted right x axis y axis) 593mm x 371mm
        1920x1200      60.0*+
        1680x1050      60.0  
        1400x1050      60.0  
        1280x1024      75.0     60.0  
        1440x900       59.9  
        1280x960       60.0  
        1152x864       75.0  
        1024x768       75.1     70.1     60.0  
        832x624        74.6  
        800x600        72.2     75.0     60.3     56.2  
        640x480        75.0     72.8     66.7     60.0  
        720x400        70.1  
    HDMI1 disconnected (normal left inverted right x axis y axis)
    DP1 disconnected (normal left inverted right x axis y axis)
    VIRTUAL1 disconnected (normal left inverted right x axis y axis)

1. dualDisplay
--------------

Create a `dualDisplay <https://github.com/vonbrownie/linux-home-bin/blob/master/dualDisplay>`_ shell script to generate a combined desktop (with external monitor set as primary display and positioned to the right of laptop display):

.. code-block:: bash

    #!/bin/bash
    first_dsply=$(xrandr | grep " connected" | awk 'FNR == 1 {print $1}')
    second_dsply=$(xrandr | grep " connected" | awk 'FNR == 2 {print $1}')
    conf_dsply="xrandr --output $first_dsply --auto --output $second_dsply --primary"

    if [[ -n $second_dsply ]]
    then
        $conf_dsply --auto --right-of $first_dsply
    fi

Save the script to ``~/bin`` or ``/usr/local/bin`` and ``chmod 755 dualDisplay`` to make it executable.

Sources: `dualDisplay <https://github.com/vonbrownie/linux-home-bin/blob/master/dualDisplay>`_ and its companion `Library.sh <https://github.com/vonbrownie/linux-home-bin/blob/master/Library.sh>`_ (github.com/vonbrownie)

2. Autostart
------------

Add ``dualDisplay`` to ``~/.config/lxsession/Lubuntu/autostart`` to run script at login.

3. Wallpaper
------------

Desktop wallpapers are controlled by **PCManFM** by default in Lubuntu. To configure a different wallpaper for each display... navigate to ``~/.config/pcmanfm/lubuntu`` and modify the ``wallpaper`` setting in ``desktop-items-*.conf``:

* laptop display is ``desktop-items-0.conf``:

.. code-block:: bash

    wallpaper=/path/to/laptop-wallpaper.jpg

* external display is ``desktop-items-1.conf``:

.. code-block:: bash

    wallpaper0=/path/to/external-wallpaper.jpg

Save all changes and logout. LXDE will now auto-detect at login if a second display is attached and make the necessary adjustments.

Happy hacking!
