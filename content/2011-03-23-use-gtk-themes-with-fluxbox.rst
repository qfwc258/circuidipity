============================
Use GTK+ themes with Fluxbox
============================

:date: 2011-03-23 01:23:00
:tags: fluxbox, linux
:slug: use-gtk-themes-with-fluxbox

Pick a theme for *Fluxbox* that has a compatible GTK+ counterpart and apply a clean consistent look across applications.

I like using the `Finery Dark <http://customize.org/fluxbox/themes/77548>`_ theme. It has a `matching GTK theme <http://gnome-look.org/content/show.php/FineryThemes?content=124694>`_ that can also be used to style QT applications.

Fluxbox
=======

Download *Finery Dark*, untar the package and place the theme folder in ``~/.fluxbox/styles`` (create the ``styles`` folder if necessary). Right-click on the Fluxbox desktop and select ``Styles->Finery Dark``.

GTK
===

Download the Finery Dark *GTK* matching theme, untar the package and place the theme folder in ``~/.themes`` (create folder if necessary).

GTK themes require an *engine* to run. Download the ``murrine`` engine to run Finery Dark and some GUI apps (thanks `Dan <a href="http://identi.ca/allsystemsarego>`_ for sugesting ``gtk-chtheme``) to make switching between themes easier ...

.. code-block:: bash

    $ sudo apt-get install gtk2-engines gtk2-engines-murrine gtk-chtheme qt4-qtconfig
    $ gtk-chtheme

Select your newly-installed Finery Dark theme.

QT
==

Apply a GTK theme to all your QT4-based applications by running ``qtconfig``. Select the ``Appearance`` tab and modify ``Select GUI Style`` from ``Desktop Settings (default)`` to ``GTK+``.

Done! Looking good Fluxbox (... and GTK ... and QT ...)!
