=====================================
ThinkPad USB Keyboard with TrackPoint
=====================================

:date: 2017-06-28 08:40:00
:slug: thinkpad-usb-keyboard-trackpoint
:tags: keyboard, linux

A Thinkpad keyboard minus the Thinkpad with the classic Trackpoint + Left/Middle/Right mouse buttons. Its attached to my `Stretchbook <http://www.circuidipity.com/jessiebook-to-stretchbook.html>`_ and I want to change the behaviour of a few keys.

Let's go!
=========

Attach the keyboard ...

.. code-block:: bash

    $ lsusb | grep -i keyboard
    Bus 001 Device 002: ID 17ef:6009 Lenovo ThinkPad Keyboard with TrackPoint

0. Caps_Lock and xmodmap
------------------------

``Caps_Lock`` occupies a prime location and - seeing as I do not carry on many ALL CAPS conversations - the key can be re-purposed for better use. I use `xmodmap <http://www.circuidipity.com/xmodmap.html>`_ to modify the keymap and transform the key into ``BackSpace``.

Retrieve current keymap (and the ``keycode`` for ``Caps_Lock``) ...

.. code-block:: bash

    $ xmodmap -pke
    [...]
    keycode  66 = Caps_Lock NoSymbol Caps_Lock
    [...]
    
Output for ``Caps_Lock`` using ``xev`` ...

.. code-block:: bash

    KeyPress event, serial 32, synthetic NO, window 0x1600001,
        root 0xb4, subw 0x0, time 578277182, (137,-6), root:(781,12),
        state 0x0, keycode 66 (keysym 0xffe5, Caps_Lock), same_screen YES,
        XLookupString gives 0 bytes: 
        XmbLookupString gives 0 bytes: 
         XFilterEvent returns: False

Test a new key modification in the current Xsession ...

.. code-block:: bash
 
    $ xmodmap -e "keycode 66 = BackSpace" && xmodmap -e "clear Lock"

Make the change sticky by adding the keymapping to ``~/.xmodmap`` ...

.. code-block:: bash

    ! Modify Caps_Lock into Backspace                                                  
    keycode 66 = BackSpace                              
    clear Lock

Modify ``~/.xinitrc`` to load keymap at ``startx`` ...

.. code-block:: bash

    if [ -f ~/.xmodmap ]; then
        xmodmap ~/.xmodmap
    fi

... and apply the new settings in the current session ..

.. code-block:: bash

    xmodmap ~/.xmodmap

1. Multimedia keys and xbindkeys
--------------------------------

This keyboard includes multimedia keys. Create keyboard shortcuts for these specialty keys by installing ...

* ``xbindkeys`` - associate keys to shell commands
* ``pulseaudio-utils`` - manage sound with ``pactl``
* ``rhythmbox-plugins`` - (optional) player controls

.. code-block:: bash

    $ sudo apt install xbindkeys pulseaudio-utils rhythmbox-plugins

With ``rhythmbox-plugins`` the ``Fn+{Play,Pause,Previous,Next,Stop}`` controls "just work" with the audio player. I use `xbindkeys <http://www.circuidipity.com/xbindkeysrc.html>`_  to associate new functions to keys.

Retrieve the ``keycodes`` and ``keysyms`` of the volume keys ...

.. code-block:: bash

    $ xmodmap -pke | egrep -i 'volume|mute'
    keycode 121 = XF86AudioMute NoSymbol XF86AudioMute
    keycode 122 = XF86AudioLowerVolume NoSymbol XF86AudioLowerVolume
    keycode 123 = XF86AudioRaiseVolume NoSymbol XF86AudioRaiseVolume
    keycode 198 = XF86AudioMicMute NoSymbol XF86AudioMicMute

I create a `standalone script <http://www.circuidipity.com/pavolume.html>`_ to control PulseAudio volume and associate the new command ``paVolume`` and its options to volume keys in ``~/.xbindkeysrc`` ...

.. code-block:: bash

    # Mute/lower/raise volume                                                
    "paVolume -m"                                                                      
    XF86AudioMute                                                                      
    "paVolume -d"                                                                      
    XF86AudioLowerVolume                                                               
    "paVolume -u"                                                                      
    XF86AudioRaiseVolume

Add command ``xbindkeys`` to ``~/.xinitrc`` to load the new configuration at ``startx`` ...

.. code-block:: bash

    if [ -f ~/.xbindkeysrc ]; then
        xbindkeys
    fi

2. TrackPoint
-------------

Customize pointer settings by installing ``xinput`` ...

.. code-block:: bash

    $ sudo apt install xinput

Discover the ``DEVICE <ID>`` with ``xinput list | grep "TrackPoint" | grep "pointer"`` ...

.. code-block:: bash

    $ xinput list | grep "TrackPoint" | grep "pointer"
    ⎜   ↳ Lite-On Technology Corp. ThinkPad USB Keyboard with TrackPoint    id=13   [slave  pointer  (2)]

Trackpoint is auto-detected but slow. My old method of configuring the pointer was failing under Debian _stable_/stretch (device id=13) ...

.. code-block:: bash

    $ xinput set-prop 13 "Device Accel Constant Deceleration" 0.30
    property 'Device Accel Constant Deceleration' doesn't exist, you need to specify its type and format

... and viewing the device properties with ``xinput list-props 13`` shows the problem; the old ``Device...`` settings have been replaced with ``libinput...``, which is a library to handle input devices. Xorg in the latest Debian has switched away from using ``evdev`` to the ``libinput`` driver ...

.. code-block:: bash
    
    $ dpkg -l | grep xserver-xorg-input
    [...]
    ii  xserver-xorg-input-libinput     0.23.0-2    amd64   X.Org X server -- libinput input driver

Check out which devices are managed by ``libinput`` ...

.. code-block:: bash

    $ grep libinput $HOME/.local/share/xorg/Xorg.0.log

**[ Fix! ]** Modify the "Coordinate Transformation Matrix", a `transformation matrix used to calculate a pointer movement. <https://wiki.ubuntu.com/X/InputCoordinateTransformation>`_

Current setting ... 

.. code-block:: bash

	$ xinput list-props 13 | grep "Coordinate Transformation Matrix"
	Coordinate Transformation Matrix (140): 1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000
    
Experiment a bit with setting a new matrix in row-order. [1]_ I wanted a faster pointer speed and found this configuration to my liking ...

.. code-block:: bash

	$ xinput set-prop 13 "Coordinate Transformation Matrix" 2.600000, 0.000000, 0.000000, 0.000000, 2.600000, 0.000000, 0.000000, 0.000000, 1.000000

I `created a shell script <https://github.com/vonbrownie/homebin/blob/master/keyboardconf>`_ that detects and applies custom settings as per keyboard type. I add the command to `my xinitrc <http://www.circuidipity.com/xinitrc.html>`_ to be run at ``startx`` ...

.. code-block:: bash

    ~/bin/keyboardconf & 
    
Sources: dotfiles/`.xmodmap.thinkpad_usb <https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.thinkpad_usb>`_, dotfiles/`.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_, dotfiles/`.xbindkeysrc.thinkpad_usb <https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.thinkpad_usb>`_, and homebin/`keyboardconf <https://github.com/vonbrownie/homebin/blob/master/keyboardconf>`_

Happy hacking!

Notes
`````

.. [1] `"I don't want any mouse acceleration, but I want to increase the speed of my mouse" <https://unix.stackexchange.com/a/177640>`_ and `InputCoordinateTransformation <https://wiki.ubuntu.com/X/InputCoordinateTransformation>`_
