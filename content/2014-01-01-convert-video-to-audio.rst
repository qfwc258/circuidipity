==================================
Convert video file(s) to MP3 audio
==================================

:date: 2014-01-01 01:23:00
:tags: shell, programming, github, linux
:slug: convert-video-to-audio

A simple script I made to convert downloaded YouTube videos to MP3s ...

.. code-block:: bash

    MP3="-acodec libmp3lame -aq 0 -ac 2 -ar 44100"

    for f in "$@"
    do
        ffmpeg -i "$f" $MP3 "$(echo $f | sed 's/....$/.mp3/')"
    done

Requires ``ffmpeg`` and ``libmp3lame0``.

Source: `v2a <https://github.com/vonbrownie/linux-home-bin/blob/master/v2a>`_
