---
title: "Command line tools: youtube-dl"
date: "2015-07-12"
publishDate: "2014-04-01"
tags:
  - shell
  - linux
slug: "youtube-dl"
aliases:
  - /youtube-dl.html
---

Download videos using the command line program [youtube-dl](http://rg3.github.io/youtube-dl/) from a whole bunch of online video sites. It can also convert videos into audio files (courtesy of `ffmpeg`).

On Debian, install (`ffmpeg` requires [deb-multimedia](http://www.deb-multimedia.org/)) ...
                                                                                    
```bash                                                                
sudo apt-get install youtube-dl rtmpdump ffmpeg
```

Basic usage ...

```bash
youtube-dl https://www.youtube.com/watch?v=SOMEiD
```

... will download the best quality copy (default) of the specified video hosted on YouTube to the current directory.

To enable audio extraction with a few desirable pre-configured options I create a new `youtube-dl-audio` alias in `~/.bashrc` ...

```bash
alias youtube-dl-audio='youtube-dl $1 --output "$HOME/audio/%(title)s-%(upload_date)s.%(ext)s" --restrict-filenames --extract-audio --audio-format "mp3" --audio-quality "0"'
```

... using these options ...

`--output "$HOME/audio/%(title)s-%(upload_date)s.%(ext)s`
: save file to *$HOME/audio/* and rename file using template *%(title)s-%(upload_date)s.%(ext)s*

`--restrict-filenames`
: removes spaces and non-alphanumeric characters from filename

`--extract-audio` and `--audio-format "mp3"`
: create an *mp3* audio file and delete the video (or add the `-k` option to save video)

`--audio-quality "0"`
: set a value between 0-9 (lower equals better) for VBR or assign a specific bitrate (default is 5|128K)

Reload the config and extract audio from an online video ...

```bash
source ~/.bashrc
youtube-dl-audio https://www.youtube.com/watch?v=SOMEiD
```

See `man youtube-dl` for more possibilities!

**Update**

:penguin: [$HOME Slash Bin](http://www.circuidipity.com/homebin/) :: I skipped the alterations to `.bashrc` and created a shell script: [yt-audio](https://github.com/vonbrownie/homebin/blob/master/yt-audio) 

Happy hacking!
