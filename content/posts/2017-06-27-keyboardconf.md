---
title: "Detect and configure keyboards"
date: "2017-06-27"
publishDate: "2017-06-27"
tags:
  - keyboard
  - shell
  - programming
  - linux
slug: "keyboardconf"
aliases:
  - /keyboardconf.html
---

I have two keyboards I am interested in modifying with custom hotkey actions (via [xbindkeys](http://www.circuidipity.com/xbindkeysrc)) and remapping keys (via [xmodmap](http://www.circuidipity.com/xmodmap)). So for my laptop's keyboard I created [.xbindkeysrc.chromebook](https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.chromebook) and [.xmodmap.chromebook](https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.chromebook), my [Thinkpad USB Keyboard + Trackpoint](http://www.circuidipity.com/thinkpad-usb-keyboard-trackpoint) uses [.xbindkeysrc.thinkpad_usb](https://github.com/vonbrownie/dotfiles/blob/master/.xbindkeysrc.thinkpad_usb) and [.xmodmap.thinkpad_usb](https://github.com/vonbrownie/dotfiles/blob/master/.xmodmap.thinkpad_usb), and I create `~/.xbindkeysrc` and `~/.xmodmap` symlinks to the relevant config for the keyboard in use.

Now that the laptop is my primary machine, I may be using either keyboard on the same machine depending on location: the built-in keyboard when away; connecting to the USB keyboard and external display when at home. Old method of symlinking won't work if I am switching which keyboard I use.

**[ FIX! ]** :penguin: [$HOME Slash Bin](http://www.circuidipity.com/homebin/) :: I created the [keyboardconf](https://github.com/vonbrownie/homebin/blob/master/keyboardconf) shell script to detect attached keyboards and load appropriate modifications. Priority is assigned to the external Thinkpad keyboard and, failing to detect that device, the program falls back to setting up the built-in keyboard. Scripting this detection makes it easy for me to add more keyboard types in the future!

Program is in my [~/bin](http://www.circuidipity.com/homebin) and I add the command to [~/.xinitrc](https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc) to run at `startx` ...

```bash
~/bin/keyboardconf &
```

Happy hacking!
