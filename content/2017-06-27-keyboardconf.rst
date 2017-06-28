==============================
Detect and configure keyboards
==============================

:date: 2017-06-27 23:30:00
:slug: keyboardconf
:tags: keyboard, shell, programming, homebin, linux

I have two keyboards I am interested in modifying with custom hotkey actions (via `xbindkeys <http://www.circuidipity.com/xbindkeysrc.html>`_) and remapping keys (via `xmodmap <http://www.circuidipity.com/xmodmap.html>`_). So for my `Stretchbook's <http://www.circuidipity.com/jessiebook-to-stretchbook.html>`_ keyboard I created `.xbindkeysrc.chromebook <https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.chromebook>`_ and `.xmodmap.chromebook <https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.chromebook>`_, my `Thinkpad USB Keyboard + Trackpoint <http://www.circuidipity.com/thinkpad-usb-keyboard-trackpoint.html>`_ uses `.xbindkeysrc.thinkpad_usb <https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.thinkpad_usb>`_ and `.xmodmap.thinkpad_usb <https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.thinkpad_usb>`_, and I would create ``~/.xbindkeysrc`` and ``~/.xmodmap`` symlinks to the relevant config for the keyboard in use.

Now that Stretchbook is my primary machine, I may be using either keyboard on the same machine depending on location: the built-in keyboard when away; connecting to the USB keyboard and external display when at home. Old method of symlinking won't work if I am switching which keyboard I use.

**[ FIX! ]** I created the `keyboardconf <https://github.com/vonbrownie/homebin/blob/master/keyboardconf>`_ shell script to detect attached keyboards and load appropriate modifications. Priority is assigned to the external Thinkpad keyboard and, failing to detect that device, the program falls back to setting up the built-in keyboard. Scripting this detection makes it easy for me to add more keyboard types in the future!

Program is in my `~/bin <http://www.circuidipity.com/homebin.html>`_ and I add the command to `~/.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_ to run at ``startx`` ...

.. code-block:: bash

	~/bin/keyboardconf &

Sources: homebin/`keyboardconf <https://github.com/vonbrownie/homebin/blob/master/keyboardconf>`_, dotfiles/`.xbindkeysrc.chromebook <https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.chromebook>`_, dotfiles/`.xmodmap.chromebook <https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.chromebook>`_, dotfiles/`.xbindkeysrc.thinkpad_usb <https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.thinkpad_usb>`_, dotfiles/`.xmodmap.thinkpad_usb <https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.thinkpad_usb>`_, and dotfiles/`.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_

Happy hacking!
