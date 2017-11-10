---
title: Notes
slug: notes
menu:
  main:
    weight: 50
---

### 2017-10-28T1701

Enable **periodic TRIM** on SSD drives. Create a weekly TRIM job in `/etc/cron.weekly/trim` ...

```bash
#!/bin/sh
# trim all mounted file systems which support it
/usr/bin/fstrim --all
```

Make the file executable and test ...

```bash
$ sudo chmod 755 /etc/cron.weekly/trim
$ sudo /etc/cron.weekly/trim                # check the program runs without errors
$ sudo run-parts --test /etc/cron.weekly    # checks that cron can run the script
    /etc/cron.weekly/trim                   # this should be output of run-parts
```

Links: [Proper way to trim ssd in void linux](https://forum.voidlinux.eu/t/ssd-proper-way-to-trim-ssd-in-void-linux/749) and [HOWTO configure periodic trim](https://www.digitalocean.com/community/tutorials/how-to-configure-periodic-trim-for-ssd-storage-on-linux-servers)

### 2017-10-25T2126

Crappy font rendering in firefox. **[ Fix! ]** ...

```bash
$ mkdir ~/.config/fontconfig
$ cp /etc/fonts/fonts.conf ~/.config/fontconfig/fonts.conf
```

Edit `fonts.conf` ...

```bash
<!--
    Fix crappy font rendering in firefox
-->
    <match target="pattern">
        <test name="family" qual="any">
            <string>Helvetica</string>
        </test>
        <edit name="family" mode="assign" binding="same">
            <string>sans-serif</string>
        </edit>
    </match>
```

Restart firefox and the jagged helvetica font has been replaced by the default sans-serif ... which can be seen by running ...

```bash
$ fc-match Helvetica
DejaVuSans.ttf: "DejaVu Sans" "Book"
```

Link: https://forum.voidlinux.eu/t/bad-font-rendering-in-firefox-for-helvetica/2748/5

### 2017-10-21T1315

Using [runit](http://smarden.org/runit/) init ... To stop an enabled service from starting automatically at boot, create a file named `down` in the service directory ...

```bash
sudo touch /etc/sv/*service_name*/down
```

### 2017-10-07T1116

> Act without doing;  
> work without effort.  
> Think of the small as large  
> and the few as many.  
> Confront the difficult  
> while it is still easy;  
> accomplish the great task  
> by a series of small acts.  
>
> The Master never reaches for the great;  
> thus she achieves greatness.  
> When she runs into a difficulty,  
> she stops and gives herself to it.  
> She doesn't cling to her own comfort;  
> thus problems are no problem for her.  

-- Lao Tzu, *Tao Te Ching, Ch 63*

### 2017-09-28T1203

Pulseaudio for Arch Linux ... set [default sink](https://wiki.archlinux.org/index.php/PulseAudio/Examples).

Set the default output source ...

```bash
$ pacmd list-sinks | grep -e 'name:' -e 'index'
  * index: 0                                   
        name: <alsa_output.pci-0000_00_1b.0.analog-stereo>
```

To set it as the system wide default, add the following to `/etc/pulse/default.pa` ...

```bash
set-default-sink alsa_output.pci-0000_00_1b.0.analog-stereo
```

Restart pulseaudio with `pulseaudio -k` (kills and restarts).

The default sink can be referred as `@DEFAULT_SINK@` in commands, for example ...

```bash
pactl set-sink-volume @DEFAULT_SINK@ +5%
```

### 2017-09-17T1150

> Since the late 1980s, scientists have been tracking a whale who sings at a sonic frequency higher than any other whale of its species: at 52 hertz, just above the lowest note on a tuba. It sings songs no one answers. Internet societies have been following it for years like sad Ahabs, transposing their own feelings on to it, believing they understand it. Alone in their bedrooms they hunt this whale they believe to be lonely just like them. Talk to scientists and they will say other whales can probably hear it, maybe it’s deaf, maybe the whale’s song is the result of a genetic mutation. But it doesn’t matter: the lonely people have taken this whale as their totem. I’ve followed it for years.

Link: https://www.theguardian.com/global/2017/sep/17/choosing-to-be-on-your-own

### 2017-08-30T2055

**Extend an LVM logical volume and filesystem:** the quick and automatic way ... If you are growing the LV you can do this while the filesystem is mounted ...

```bash
sudo lvresize --resizefs --size +100G /dev/vg/home
    Size of logical volume vg/home changed from 238.42 GiB (61035 extents) to 338.42 GiB (86635 extents).
    Logical volume vg/home successfully resized.
    resize2fs 1.43.4 (31-Jan-2017)
    Filesystem at /dev/mapper/vg-home is mounted on /home; on-line resizing required
    old_desc_blocks = 30, new_desc_blocks = 43
    The filesystem on /dev/mapper/vg-home is now 88714240 (4k) blocks long.
```

Link: https://www.systutorials.com/5621/extending-a-mounted-ext4-file-system-on-lvm-in-linux/

### 2017-08-23T2205

**Disable system beep** on a Thinkpad ...

```bash
sudo rmmod pcspkr
```

Permanently ... edit `/etc/inputrc` to disable in console ...

```bash
set bell-style none
```

... add to`.xinitrc` ...

```bash
xset b off
```

NOTE: this did *not* work ... adding `blacklist pcspkr` to (add/create) `/etc/modprobe.d/blacklist`.

### 2017-08-05T1840

Fresh install of [Tiny Tiny RSS](https://tt-rss.org/) allows a single URL path to be set. I want multiple URLs to support both local and remote access.

**[ Fix! ]** Disable URL checks by adding to `config.php` ...

```bash
define('_SKIP_SELF_URL_PATH_CHECKS', true);
```

Link: [Access by local + domain IP](https://discourse.tt-rss.org/t/after-todays-upgrade-6-7-2017/353/11?u=conrad784)

### 2017-07-21T1033

Enable forward search in Bash history. `CTRL-R` enables reverse incremental searches through the Bash shell history and `CTRL-S` runs forward searches. However `CTRL-S` collides with XON/XOFF flow control in terminal and disables that feature in history.

**[ Fix! ]** Disable XON/XOFF in `$HOME/.bashrc` ...

```bash
stty -ixon
```

Hitting `CTRL-S` by mistake in vim no longer disables output to the terminal.

Link: [Unable to forward search Bash history similarly as with CTRL-r](https://stackoverflow.com/questions/791765/unable-to-forward-search-bash-history-similarly-as-with-ctrl-r)

### 2017-07-20T1039

A simple [GIMP](http://www.gimp.org) recipe for play at making 8-bit pixel images:

* Open image and select `Colors > Brightness-Contrast > Contrast` to increase contrast
* `Image > Scale Image > 10%  Interpolation: None`
* `Image > Scale Image > 400%  Interpolation: None`

Manipulate the scale image settings to increase/decrease pixelation to satisfaction.

### 2017-07-17T0941

[Linuxlogo](http://www.deater.net/weave/vmwprod/linux_logo/) provides Tux, the Debian swirl, and other distro logos that can be displayed - along with system information - at the console login prompt ...

```bash
sudo apt-get install linuxlogo
sudo cp /etc/issue /etc/issue.bak
sudo sh -c 'linux_logo -L debian -F ".: Greetings, Carbon-Based Biped :.\n\n#O Version #V\nCompiled #C\n#H \\l" > /etc/issue'
```

### 2017-07-14T1538

Correct the 'stripping effect' in QT applications using the **Breeze Dark** theme. Example: Transmission-qt would show file listings in alternating background colours, with every other line rendered in light background and foreground colours.

**[ Fix! ]** Offending colour is `#eff0f1`. Replaced with `#404552` in `~/.config/qt5ct/colors/breeze_dark.conf`.

### 2017-07-13T0916

Retrieving Debian release information (depending on what I want) ...

* `/etc/debian_version`
* `/etc/os-release`
* `lsb_release -c`

### 2017-07-10T1846

Assign user to new group and reload assignments without logging out ...

```bash
su - $USER
id        # see the new group
```

Link: https://superuser.com/a/354475

### 2017-07-09T0807

**Nmap** will quickly identify Internet services hosted by a network connected machine without even requiring to log in to it. Simply call the following command on another machine connected to the same network ...

```bash
nmap 192.168.1.88
```

Link: [DAH: 3.2.1.1. Network and Processes](https://debian-handbook.info/browse/stable/sect.how-to-migrate.html)

### 2017-07-06T0857

Use `apt-show-versions` to check list of installed packages and available versions. Good way to quickly grep which packages are **not** part of the default release.

Install ...

```bash
sudo apt install apt-show-versions
```

Release is `stretch` ...

```bash
apt-show-versions | grep -v stretch
  qt5ct:amd64 0.31-2 installed: No available version in archive
  volnoti:amd64 20161215T1244-1 installed: No available version in archive
```

### 2017-07-03T0900

Configure i3wm to put clients on specific workspaces. Run `xprop` in a terminal and click on the client to get `WM_CLASS`: first part is the **instance**, second part is the **class** ...

```bash
xprop
  [...]
  WM_CLASS(STRING) = "transmission-qt", "transmission"
```

Add the change to `~/.config/i3/config` ...

```bash
# Assign torrent client to workspace 10
assign [instance="transmission-qt"] 10
```

Link: [Automatically putting clients on specific workspaces](https://i3wm.org/docs/userguide.html#assign_workspace)

### 2017-07-02T1014

Addon for Firefox: [Text Contrast for Dark Themes](https://addons.mozilla.org/en-US/firefox/addon/text-contrast-for-dark-themes/)

Fixs issue with text entry on some websites (white text on white in gmail signin, yahoo search, others) when using the **Breeze Dark** QT theme.

### 2017-06-29T1237

Find and replace text with **sed**.

Save back to the original file ...

```bash
sed -i 's/original/new/g' file.txt
```

Save to new_file.txt ...

```bash
sed 's/original/new/g' file.txt > new_file.txt
```

Multiple text patterns and variables ...

```bash
sed "s/$original/$new/g; s/$pattern2/$new_again/g" file.txt > new_file.txt
```

Link: https://askubuntu.com/q/20414

### 2017-06-28T1512

Lots of documentation and config samples are available in `/usr/share/doc` in gzip'ed format. Non-root user access with the `zcat` and `zless` commands. Make use of a config sample by redirecting output. Example ...

```bash
zcat /usr/share/doc/dunst/dunstrc.example.gz > ~/.config/dunst/dunstrc
```

### 2017-06-27T0902

Default keyboard layout in Debian is configured in `/etc/default/keyboard` and is shared between X and the command line ...

```bash
cat /etc/default/keyboard
  [...]
  XKBMODEL="pc105"
  XKBLAYOUT="us"
  XKBVARIANT=""
  XKBOPTIONS=""
  BACKSPACE="guess"
```

Modify this file to set a new default keyboard layout, either manually or run ...

```bash
sudo dpkg-reconfigure keyboard-configuration
```

### 2017-06-26T1126

Limit the CPU usage of an application ... I tried using **handbrake-gtk** to convert a video and the application grabbed 100% of all 4 cores, sent system temperature to 98C, and finally crashed the machine.

**[ Fix! ]** Install **cpulimit** and set the limit to 80 (20percent * 4 cores) ...

```bash
sudo cpulimit -e ghb -l 80
```

### 2017-06-25T0922

Firework sounds for upcoming Canada Day!

```bash
sudo apt install sox
```

Screamer ...

```bash
play -n synth sine 8000 bend 0.5,-1800,5 flanger 0 3 0 20 10 tri 20 quad trim 0 7
```

Bottle rocket ...

```bash
play -n synth whitenoise 200 fade 0.2 1 1 trim 0 0.5 ; sleep 1 ; play -n synth whitenoise 200 fade 0 1 1 trim 0 1
```

Links: https://twitter.com/climagic/status/485083242425368579 and https://twitter.com/climagic/status/485069251401629697

### 2017-06-24T0844

Retrieve information about hardware using `sudo dmidecode`, or much of the same information is available to the non-root user in `/sys/devices/virtual/dmi/id`.

Link: https://unix.stackexchange.com/a/172334

### 2017-06-23T1001

Switch from default qwerty to the colemak keyboard layout ...

```bash
setxkbmap -query
  rules:      evdev
  model:      pc105
  layout:     us
setxkbmap us -variant colemak
setxkbmap -query
  rules:      evdev
  model:      pc105
  layout:     us
  variant:    colemak
```

### 2017-06-22T1036

Generate list of packages installed on one machine running Debian for installation on another machine.

List of packages on first machine ...

```bash
sudo dpkg --get-selections | grep -v deinstall > deb-pkg-list.txt
```

Install packages on the second machine ...

```bash
sudo apt install dselect
sudo dselect update    # update dselect database
sudo dpkg --set-selections < deb-pkg-list.txt
sudo apt dselect-upgrade
```

### N2017-06-21T0832

VLC not playing mkv files on the chromebook. Generates error message ...

```bash
libvdpau-va-gl: Decoder::Render_h264(): no surfaces left in buffer
```

**[ Fix! ]** In VLC navigated to `Tools->Preferences->Input/Codecs` and for **Hardware-accelerated decoding** switched to `VA-API video decoder via x11` instead of using `VDPAU`. Or set `avcodec-hw=vaapi_x11` in `~/.config/vlc/vlcrc`.

Link: https://askubuntu.com/questions/714363/intel-vaapi-cant-play-mkv-with-vlc

### 2017-06-20T0926

Clearing the shell cache ... I originally installed `glances` via apt to `/usr/bin/glances`, then removed, then installed via pip to `/usr/local/bin/glances`. The command would show in PATH but - without an explicit path defined - would continue to try and execute from `/usr/bin`.

**[ Fix! ]**  Bash caches commands. Clear the cache of paths to executables using `hash` ...

```bash
type glances
  glances is hashed (/usr/bin/glances)
hash -d glances
type glances
  glances is /usr/local/bin/glances
```

### 2017-06-19T0953

Configure menu colours in Grub by creating `/boot/grub/custom.cfg` with settings ...

```bash
set color_normal=white/black
set menu_color_normal=white/black
set menu_color_highlight=white/green
```

### 2017-06-18T0949

Stop pulseaudio from respawning after halt (encountered in Ubuntu 16.04) ... When I kill pulseaudio with `pulseaudio -k` or `kill -9 ID` it immediately restarts ...

```bash
pgrep pulse
  12808 /usr/bin/pulseaudio --start --log-target=syslog
```

**[ Fix! ]** There is a config file `/etc/pulse/client.conf` with `autospawn = yes` set by default. I could modify that, but chose instead to create `~/.config/pulse/client.conf` and set `autospawn = no`. It works ... pulseaudio stays dead.

### 2017-06-17T0921

Start a new project in Git and host on Github (after setting up a default config in `~/.gitconfig`) ...

```bash
mkdir new_project
cd new_project
touch .gitignore
touch README.rst      # rst will allow github to auto-detect and configure as a project homepage
git init
git add README.rst    #... or 'git add .' to add all files recursively
git status
git commit -a -m 'first commit'   # '-a' option auto-adds all files being tracked and commits them
git log               # to view commit history
```

Connect with Github ...

```bash
git remote add origin https://github.com/vonbrownie/sitrep.git  # connect my local repo to github for first time
git remote -v  # confirm local knows about remote
git push -u origin master
```

... and to pull in (download) changes from Github master ...

```bash
git pull origin master
```

### 2017-06-16T0950

Stop pinned tabs from auto-loading upon Firefox startup. Goto `about:config` and set to **true** ...

```bash
* browser.sessionstore.restore_pinned_tabs_on_demand    default boolean false
```

### 2017-06-15T0853

Debian *stretch*/stable `xbacklight` is acting up ...

```bash
xbacklight -dec 10
  No outputs have backlight property
```

I **can** write to the file directly to increase/decreae display brightness ...

```bash
cat /sys/class/backlight/intel_backlight/max_brightness 
  937
sudo sh -c 'echo 500 > /sys/class/backlight/intel_backlight/brightness'
sudo sh -c 'echo 937 > /sys/class/backlight/intel_backlight/brightness'
```

... or use `xrandr` ...

```bash
xrandr --output eDP-1 --brightness 0.5
```

This is [a known issue.](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=833508)

**[ Fix! ]** Roll-back from `xserver-xorg-core` to `xserver-xorg-video-intel`.

Create `/etc/X11/xorg.conf.d/10-video-intel.conf` containing ...

```bash
Section "Device"
    Identifier "Intel"
	Driver "intel"
EndSection
```

### 2017-06-14T2113

Trying to install Debian's `flashplugin-nonfree` package consistently fails with the error ....

```bash
ERROR: wget failed to download http://people.debian.org/~bartm/flashplugin-nonfree/D5C0FC14/fp.24.0.0.221.sha512.amd64.pgp.asc
```

**[ Fix! ]** Manual install works courtesy of the instructions at https://wiki.debian.org/FlashPlayer#Manual_update

### 2017-06-14T0947

Setup colour scheme for vim. As per [Giles](http://www.gilesorr.com/blog/) recommendation I use [tir_black.](http://www.vim.org/scripts/script.php?script_id=2777) Place in `~/.vim/colors`.

Set as default colour scheme in `init.vim` ...

```bash
colorscheme tir_black
```

Colour scheme works when neovim runs in terminal. Does *not* work inside tmux. Tmux is not seeing the 256 color palette ...

```bash
tput colors
  8
```

**[ Fix! ]** Add to `~/.tmux.conf` ...

```bash
set -g default-terminal "rxvt-unicode-256color"
```

**Note:** Kill all existing tmux sessions. It is not enough simply to start a fresh session. Helpful! http://stackoverflow.com/a/25940093

Launch a new tmux session. Neovim colours work OK!

```bash
echo $TERM
  rxvt-unicode-256color
tput colors
  256
```

### 2017-06-13T0847

Created a Debian _stretch_ virtualbox guest but `virtualbox-guest-{dkms,utils,x11}` packages no longer available ... but there *are* pkgs in [sid](https://tracker.debian.org/pkg/virtualbox).

**[ Fix! ]** Install the _sid_ pkgs. Setup **apt-pinning** in `/etc/apt/preferences` ...

```bash
Package: *
Pin: release n=stretch
Pin-Priority: 900

Package: *
Pin: release a=unstable
Pin-Priority: 300
```

Add unstable to `sources.list` ...

```bash
deb http://deb.debian.org/debian/ unstable main contrib non-free
```

Update and install ...

```bash
sudo apt -t unstable install virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
sudo adduser dwa vboxsf
```

### 2017-06-12T1041

Local install of Python modules as non-root user. Example ...

```bash
pip3 install exifread
```

... libraries are installed to `~/.local/lib/python-ver/` and the bins are placed in `~/.local/bin/`.

Add `~/.local/bin` to user's $PATH.

### 2017-06-11T1020

If SSH session is frozen ... Use the key-combo **Enter, Shift + `, .** [Enter, Tilde, Period]  to drop the connection.

### 2017-06-10T0838

Microphone problem on Thinkpad x230 running Ubuntu 16.04 ... No sound input and **mic** not detected.

**[ Fix! ]** Get capture device ...                                                          

```bash
arecord -l                                                                         
  card 0: ... device 0: ...                                                            
```

... and edit `/etc/pulse/default.pa` with `load-module module-alsa-source device=hw:0,0`.

Kill and respawn pulseaudio with `pulseaudio -k`.

### 2017-06-09T0941

Restart network service on Ubuntu ... Sometimes after wake-from-suspend the network connection is down and network-manager's wifi ap list fails to refresh.
                                                                                
**[ Fix! ]** Simple systemd way ...                                                   
                                                                                
```bash                                                            
sudo systemctl restart NetworkManager.service                             
```

If that doesn't work ... Try using `nmcli` to stop and start network-manager directly ...
                                                                                
```bash
sudo nmcli networking off                                                 
sudo nmcli networking on                                                  
```

Old-fashioned SysV init script method still works on 16.04 ...                
                                                                                
```bash
sudo /etc/init.d/networking restart                                       
    ... or ...                                                              
sudo /etc/init.d/network-manager restart                                  
```

Last resort ...                                             
                                                                                
```bash
sudo ifdown -a  # -a brings down all interfaces                           
sudo ifup -a
```

### 2017-06-08T0920

Attaching to a wifi network with `nmcli` (network-manager cli client) ...

```bash
nmcli radio
nmcli device
nmcli device wifi rescan
nmcli device wifi connect SSID-Name password PASS
```

### 2017-06-07T1219

Disable [Pelican](http://www.circuidipity.com/tag-pelican.html) from auto-generating `archives.html` by adding to `pelicanconf.py` ...

```bash
ARCHIVES_SAVE_AS = ''
```

From [URL Settings](http://docs.getpelican.com/en/latest/settings.html#url-settings): "If you do not want one or more of the default pages to be created ... set the corresponding `*_SAVE_AS` setting to '' to prevent the relevant page from being generated."
