---
title: "Incremental backups using rsnapshot"
date: "2018-01-20"
publishDate: "2018-01-20"
tags:
  - rsnapshot
  - linux
slug: "rsnapshot"
---

Use the **rsync** powers of [rsnapshot](http://rsnapshot.org/) to make daily, weekly, and monthly backups of data.

I do an [automatic daily backup](https://www.circuidipity.com/backup-over-lan/) of the home directory on my laptop to a [local server](https://www.circuidipity.com/laptop-home-server/). But what if I delete something on Monday, backup the modified directory, and realize on Friday "Doh! I need that!". If I have the item saved on [external storage](https://www.circuidipity.com/encrypt-external-drive/) no problem. Between daily syncs of a backup and periodic manual syncs to a portable hard drive, however, its possible that it might be weeks or months later when I realize I need something I had removed. Might there be a better way to track changes to a home backup?

Yes there is! **Rsnapshot** makes one complete backup, then makes **incremental snapshots** of that full backup that tracks any modifications. It is very resource efficient. A daily snapshot of a 100GB directory that is unchanged might be only 20MB. Good stuff!

## Let's go!

I install `rsnapshot` on my Debian server, make a directory to store snapshots, and make a copy of the default rsnapshot config ...

```bash
$ sudo apt install rsnapshot
$ mkdir -p /path/to/backup/snapshots
$ sudo cp /etc/rsnapshot.conf /etc/rsnapshot.conf.default
```

Modify `/etc/rsnapshot.conf` (important to separate fields with **TABS** not spaces) [^1] and (for example) uncomment the options listed below, plus create a schedule of (6) daily, (4) weekly, and (3) monthly snapshots ...  

```bash
snapshot_root   /path/to/backup/snapshots/

cmd_cp          /bin/cp
cmd_rm          /bin/rm
cmd_rsync       /usr/bin/rsync
cmd_logger      /usr/bin/logger
cmd_du          /usr/bin/du
cmd_rsnapshot_diff      /usr/bin/rsnapshot-diff

retain  daily   6
retain  weekly  4
retain  monthly 3

verbose         2
loglevel        3
logfile /var/log/rsnapshot.log
lockfile        /var/run/rsnapshot.pid

exclude         /home/foo/.cache
exclude         /home/foo/.thumbnails

backup  /home/foo/  localhost/
```

Check for proper syntax and run a snapshot test ...

```bash
$ sudo rsnapshot configtest
$ sudo rsnapshot -t daily
```

If everything checks out OK run the daily snapshot (full backup on first run) ...

```bash
$ sudo rsnapshot daily
```

Check the disk space used by rsnapshot by calling it with the `du` argument ...

```bash
$ rsnapshot du 
```

Make automatic snapshots by modifying the sample cron file provided in `/etc/cron.d/rsnapshot` and running jobs as `root`. Example ...

```bash
# m h  dom mon dow   command
10 3    * * *       root    /usr/bin/rsnapshot daily
10 2    * * 0       root    /usr/bin/rsnapshot weekly
10 1    1 * *       root    /usr/bin/rsnapshot monthly
```

These settings will run a daily snapshot everyday at 03:10, a weekly snapshot every Sunday at 02:10, and a monthly snapshot on the first of every month at 01:10. Make sure to stagger the backups so that rsnapshot does not get snarled trying to do overlapping backups at the same time.

Happy hacking!

#### Notes

[^1]: If using vim with the `expandtab` (replace tabs with whitespace) option, disable it temporarily when editing the config.
