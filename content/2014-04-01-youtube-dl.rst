==============================
Command line tools: youtube-dl
==============================

:date: 2014-04-01 01:10:00
:slug: youtube-dl
:tags: shell, tools, linux, programming
:modified: 2015-07-12 19:10:00

`youtube-dl <http://rg3.github.io/youtube-dl/>`_ is a cool command-line program for downloading videos from a whole bunch of online video sites. It can also convert videos into audio files (courtesy of ``ffmpeg``).                                  

**Install:** On Debian (``ffmpeg`` requires `deb-multimedia <http://www.deb-multimedia.org/>`_) ...
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ sudo apt-get install youtube-dl rtmpdump ffmpeg

Basic usage ...

.. code-block:: bash

    $ youtube-dl https://www.youtube.com/watch?v=SOMEiD

... will download the best quality copy (default) of the specified video hosted on YouTube to the current directory.

To enable audio extraction with a few desirable pre-configured options I create a new ``youtube-dl-audio`` alias in ``~/.bashrc``:

.. code-block:: bash                                                                
                                                                                    
    alias youtube-dl-audio='youtube-dl $1 --output "$HOME/audio/%(title)s-%(upload_date)s.%(ext)s" --restrict-filenames --extract-audio --audio-format "mp3" --audio-quality "0"'

... using these options:

``--output "$HOME/audio/%(title)s-%(upload_date)s.%(ext)s``
    save file to *$HOME/audio/* and rename file using template *%(title)s-%(upload_date)s.%(ext)s*
``--restrict-filenames``
    removes spaces and non-alphanumeric characters from filename
``--extract-audio`` and ``--audio-format "mp3"``
    create an *mp3* audio file and delete the video (or add the ``-k`` option to save video)
``--audio-quality "0"``
    set a value between 0-9 (lower equals better) for VBR or assign a specific bitrate (default is 5|128K)

Reload the config and extract audio from an online video ...

.. code-block:: bash

    $ source ~/.bashrc
    $ youtube-dl-audio https://www.youtube.com/watch?v=SOMEiD

See ``man youtube-dl`` for more possibilities!

**Update**

I skipped the alterations to ``.bashrc`` and created a shell script: `yt-audio <https://github.com/vonbrownie/homebin/blob/master/yt-audio>`_ 

Happy hacking!
