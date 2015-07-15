=====================================
ThinkPad USB Keyboard with TrackPoint
=====================================

:date: 2015-07-15 16:14:00
:slug: thinkpad-usb-keyboard-trackpoint
:tags: debian, linux

An external ThinkPad keyboard minus the ThinkPad with the classic TrackPoint + Left/Middle/Right mouse buttons. Its attached to my Debian desktop and I want to change the behaviour of a few keys using ``xmodmap`` and ``xbindkeys``.

Let's go!
=========

Attach the keyboard:

.. code-block:: bash

    $ lsusb | grep -i keyboard
    Bus 001 Device 002: ID 17ef:6009 Lenovo ThinkPad Keyboard with TrackPoint

0. Caps_Lock and xmodmap
========================

``Caps_Lock`` occupies a prime location and - seeing as I do not carry on many ALL CAPS conversations - the key can be repurposed for better use. I use ``xmodmap`` to modify the keymap and transform the key into ``BackSpace``.

Retrieve current keymap (and the ``keycode`` for ``Caps_Lock``):

.. code-block:: bash

    $ xmodmap -pke
    [...]
    keycode  66 = Caps_Lock NoSymbol Caps_Lock
    [...]
    
Output for ``Caps_Lock`` using ``xev``:

.. code-block:: bash

    KeyPress event, serial 32, synthetic NO, window 0x1600001,
        root 0xb4, subw 0x0, time 578277182, (137,-6), root:(781,12),
        state 0x0, keycode 66 (keysym 0xffe5, Caps_Lock), same_screen YES,
        XLookupString gives 0 bytes: 
        XmbLookupString gives 0 bytes: 
         XFilterEvent returns: False

Making ``Caps_Lock`` into ``BackSpace`` is a 3-part process: **remap** the key, remove the **lock** on the key, and make it a **repeating** key.

Test a new key modification in the current Xsession:

.. code-block:: bash
 
    $ xmodmap -e "keycode 66 = BackSpace" && xmodmap -e "clear Lock" && xset r 66                                                                        

Make the change sticky by adding the keymapping to ``~/.xmodmap``:

.. code-block:: bash

    ! Modify Caps_Lock into Backspace                                                  
    keycode 66 = BackSpace                              
    clear Lock

Modify ``~/.xinitrc`` to load keymap at ``startx``:

.. code-block:: bash

    xmodmap ~/.xmodmap && xset r 66                                   

Sources: `.xmodmap.usb-thinkpad <https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.usb-thinkpad>`_, `.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_

1. Multimedia keys and xbindkeys
================================

This keyboard includes mediaplayer+volume keys. Create keyboard shortcuts for these multimedia keys by installing:

* ``xbindkeys`` - associate keys to shell commands
* ``pulseaudio-utils`` - manage sound with ``pactl``
* ``rhythmbox-plugins`` - (optional) player controls

.. code-block:: bash

    $ sudo apt-get install xbindkeys pulseaudio-utils rhythmbox-plugins

With ``rhythmbox-plugins`` the ``Fn+{Play,Pause,Previous,Next,Stop}`` controls "just work" with the audio player. I use ``xbindkeys`` to associate new functions to keys.

Retrieve the ``keycodes`` and ``keysyms`` of the volume keys:

.. code-block:: bash

    $ xmodmap -pke | egrep -i 'volume|mute'
    keycode 121 = XF86AudioMute NoSymbol XF86AudioMute
    keycode 122 = XF86AudioLowerVolume NoSymbol XF86AudioLowerVolume
    keycode 123 = XF86AudioRaiseVolume NoSymbol XF86AudioRaiseVolume
    keycode 198 = XF86AudioMicMute NoSymbol XF86AudioMicMute

I create a `standalone script <http://www.circuidipity.com/pavolume.html>`_ to control PulseAudio volume and associate the new command ``paVolume`` and its options to volume keys in ``~/.xbindkeysrc``:

.. code-block:: bash

    # Mute/lower/raise volume                                                
    "paVolume -m"                                                                      
    XF86AudioMute                                                                      
    "paVolume -d"                                                                      
    XF86AudioLowerVolume                                                               
    "paVolume -u"                                                                      
    XF86AudioRaiseVolume

Add command ``xbindkeys`` to ``~/.xinitrc`` to load the new configuration at ``startx``.

Sources: `.xbindkeysrc.usb-thinkpad <https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.usb-thinkpad>`_, `paVolume <https://github.com/vonbrownie/homebin/blob/master/paVolume>`_

2. TrackPoint
=============

TrackPoint is auto-detected but slow. Customize pointer settings by installing ``xinput``:

.. code-block:: bash

    $ sudo apt-get install xinput

Discover ``DEVICE <ID>`` with ``xinput list | grep pointer`` and ``<ID> PROPERTIES`` with ``xinput list-props <ID>``. TrackPoint sensitivity is modified using the ``Device Accel Constant Deceleration`` property:

.. code-block:: bash

    $ xinput list | grep pointer
    ⎡ Virtual core pointer                          id=2    [master pointer  (3)]
    ⎜   ↳ Virtual core XTEST pointer                id=4    [slave  pointer  (2)]
    ⎜   ↳ Lite-On Technology Corp. ThinkPad USB Keyboard with TrackPoint    id=10   [slave  pointer  (2)]
    $ xinput list-props 10 | grep "Device Accel Constant Deceleration"
            Device Accel Constant Deceleration (251):       1.000000

Test a new setting with ``xinput set-prop ID "Device Accel Constant Deceleration" SETTING``. Example:

.. code-block:: bash

    $ xinput set-prop 10 "Device Accel Constant Deceleration" 0.50

Make the change sticky by adding the command to ``~/.xinitrc``.

Happy hacking!
