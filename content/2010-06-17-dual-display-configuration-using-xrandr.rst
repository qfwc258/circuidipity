=================================================
Big screen little screen virtual screen and xrandr
==================================================

:date: 2010-06-17 01:23:00
:tags: linux
:slug: big-screen-little-screen-virtual-screen-dual-display-configuration-using-xrandr

Sometimes *less is more*. But sometimes less is just... well... *less*. I love my `little netbook <http://www.circuidipity.com/debian-linux-on-the-asus-eeepc-1001p.html>`_ . But when you have parked yourself somewhere and made yourself comfortable with an espresso and a banana... and portability is no longer a factor... the 10" screen can be a mite limiting.

But that VGA port on the side is there for a reason. Enter ``xrandr``.

This nifty command line tool is useful for setting screen size, orientation, mirroring outputs or... my interest... adding an external display and pairing it with my netbook's built-in LCD to create a single *virtual* desktop. This allows applications to be launched on either display, windows dragged from one display to the next, and window borders will respect the dimensions of whatever display they reside on when maximized.

No modifications are necessary to ``xorg.conf``. External displays can be hot-plugged to the host and a running X server can be modified by using xrandr + desired options in a terminal.

For a dual-display configuration using *Nvidia* graphics ... give `Twinview <http://www.circuidipity.com/twinview.html>`_ a go.

To setup my desired dual-display layout ... I use:

* `Asus EEEPC 1001P-MU17 <http://www.circuidipity.com/debian-linux-on-the-asus-eeepc-1001p.html>`_ netbook with 10.1" LCD at 1024x600 powered by Intel GMA 3150 integrated video

* Acer AL2216W 22" LCD at 1680x1050 resolution

* `Debian <http://www.circuidipity.com/install-debian-linux-squeeze.html>`_ with a ``2.6.32-15 kernel``, ``xrandr v1.3.2``, and the `Fluxbox <http://fluxbox.org/>`_ window manager

Running xrandr without any options will dump the state of the outputs, show existing modes for each of them, with a '+' after the preferred mode and a '*' after the current mode.

Using my setup as an example... connecting my 22" LCD to my netbook's VGA-port but leaving the external display powered off outputs:

.. code-block:: bash

    $ xrandr
    Screen 0: minimum 320 x 200, current 1024 x 600, maximum 4096 x 4096
    VGA1 connected (normal left inverted right x axis y axis)
        1680x1050      60.0 + 
        1280x1024      75.0     60.0
        1440x900       75.0     59.9 
        1280x960       60.0
        1360x765       59.8
        1152x864       75.0
        1280x720       60.0
        1024x768       75.1     70.1     60.0
        832x624        74.6
        800x600        72.2     75.0     60.3     56.2
        640x480        72.8     75.0     66.7     60.0
        720x400        70.1
    LVDS1 connected 1024x600+0+0 (normal left inverted right x axis y axis) 220mm x 129mm
        1024x600       60.0*+   65.0
        800x600        60.3 
        640x480        59.9

``Xrandr`` correctly detects my attached external display ``VGA1`` and my netbook's LCD ``LVDS1`` running at its optimum setting. For the purposes of using the dual-displays to create a virtual desktop... recent work on *Kernel Mode Setting* ``KMS`` and the latest Intel chips/drivers like the GMA 3150 allow a larger virtual display size (4096x4096) *but* the chip has hardware limitations when the display area exceeds 2048 pixels (horizontally or vertically).

`Known issues and possible workarounds <https://bugzilla.redhat.com/show_bug.cgi?id=497069>`_ when running a dual-display virtual desktop include limited and crash-prone 3D acceleration and Xvideo fails (black or empty video window). In the case of Xvideo... I experimented with the various ``-vo`` settings of ``mplayer`` and found that running ``mplayer -vo gl`` bypassed the problem.

Now to create my dual-display virtual desktop with my external display on the left and my netbook on the right I run ...

.. code-block:: bash

    $ xrandr --output LVDS1 --auto --output VGA1 --auto --left-of LVDS1

Using ``--auto`` prompts xrandr to select the optimum resolution for each display. Any supported resolution may also be set by using the ``--mode resolution`` option. If the external display is to the right of the netbook I would change ``--left-of`` to ``--right-of`` ... in addition you arrange the displays in a top or bottom layout.

If you would rather *mirror* (clone) the netbook's display on the external device (perhaps for using a projector connected to the VGA-port) ...

.. code-block:: bash

    $ xrandr --output LVDS1 --mode 800x600 --output VGA1 --mode 800x600 --same-as LVDS1

There are many other options and details described in ``man xrandr`` ... I also found http://www.thinkwiki.org/wiki/Xorg_RandR_1.2 and http://wiki.debian.org/XStrikeForce/HowToRandR12 helpful.

To preserve my xrandr configuration strings for future use... I added aliases to ``~/.bashrc`` ...

.. code-block:: bash

    alias dsply2clone='xrandr --output LVDS1 --mode 800x600 --output VGA1 --mode 800x600 --same-as LVDS1'
    alias dsply2left='xrandr --output LVDS1 --auto --output VGA1 --auto --left-of LVDS1'
    alias dsply2right='xrandr --output LVDS1 --auto --output VGA1 --auto --right-of LVDS1'

I was really impressed how setting up a dual-display configuration in xrandr "just worked" running on recent hardware and Debian. Can't believe I never tried it sooner. I like it!
