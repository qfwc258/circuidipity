=========================
Jessiebook to Stretchbook
=========================

:date: 2017-06-19 10:20:00
:slug: jessiebook-to-stretchbook
:tags: chromebook, debian, linux

With the release of **Debian 9 "Stretch"** my `C720 Chromebook has transitioned from a Jessiebook <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_ to a Stretchbook! 

I posted a `visual screenshot tour <http://www.circuidipity.com/minimal-debian.html>`_ installing the Debian _stable_ release. I use Debian's **minimal network install image** to create a console-only base configuration that can be customized for various tasks and `alternate desktops <http://www.circuidipity.com/i3-tiling-window-manager.html>`_. 

`Earlier steps <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_ taken to setup the Jessiebook still apply with two exceptions. First, ``xbacklight`` is acting up ...

.. code-block:: bash

	$ xbacklight -dec 10
	No outputs have backlight property

I **can** write to the file directly to increase/decrease the brightness of the display ...

.. code-block:: bash

	$ cat /sys/class/backlight/intel_backlight/max_brightness 
	937
	$ sudo sh -c 'echo 500 > /sys/class/backlight/intel_backlight/brightness'
	$ sudo sh -c 'echo 937 > /sys/class/backlight/intel_backlight/brightness'

... or use ``xrandr`` ...

.. code-block:: bash

	$ xrandr --output eDP-1 --brightness 0.5

This is `a known issue. <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=833508>`_

**[ Fix! ]** Roll-back from ``xserver-xorg-core`` to ``xserver-xorg-video-intel``. Create ``/etc/X11/xorg.conf.d/10-video-intel.conf`` containing ...

.. code-block:: bash

	Section "Device"
		Identifier "Intel"
		Driver "intel"
	EndSection

Second, the issues with the **ath9k** driver appear resolved and I leave the wireless alone. No further config tweaks required.

Happy hacking!
