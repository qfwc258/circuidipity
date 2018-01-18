---
title: "PHP + Nginx + PostgreSQL"
date: "2018-01-18"
publishDate: "2015-02-09"
tags:
  - php
  - nginx
  - postgres
  - network
  - debian
  - linux
slug: "php-nginx-postgresql"
---

:penguin: [Home Server](http://www.circuidipity.com/home-server/) :: As a requirement to host web applications like [Tiny Tiny RSS](http://www.circuidipity.com/ttrss.html) on my home server I install **PHP**, the lightweight proxy server **Nginx**, and the **PostgreSQL** database.

## Let's go!

**Setup:** [Netbook](http://www.circuidipity.com/laptop-home-server.html) with IP ADDRESS `192.168.1.88` running the latest stable release of Debian.

## 0. PHP

Install ...

```bash
$ sudo apt install php php-fpm php-apcu php-curl php-cli php-pgsql php-gd php-mcrypt php-mbstring php-fdomdocument php-intl
```

Improve security by editing `/etc/php/*/fpm/php.ini` and modifying `pathinfo` to `0` ...

```bash
cgi.fix_pathinfo=0                                                              
```

Restart PHP ...
                                                                                    
```bash
$ sudo systemctl restart php7.0-fpm
```

## 1. Nginx

Installing the above PHP packages will pull in apache packages that are not required. Remove ...

```bash
$ sudo apt --purge remove *apache*
```

Install ...

```bash
$ sudo apt install nginx-common
$ sudo apt install nginx                                                    
$ sudo systemctl start nginx                                                  
```

Verify web server is running by opening a browser and navigating to `http://192.168.1.88`. If you see `Welcome to nginx!` the server is installed correctly.

## 2. Host multiple domains

Nginx is capable of serving up multiple web domains or **server blocks** (virtual hosts):

* For (username `foo`) I create `/home/foo/www` to hold block content in subfolders
* Create block configs in `/etc/nginx/sites-available`
* A block is made active by setting a symbolic link in `/etc/nginx/sites-enabled` to its block config

**Example:** Setup a `ttrss` server block to host an RSS feed reader at `http://ttrss.lan`. 

Create a new root directory to hold the contents of `ttrss` in the home directory ...

```bash
$ mkdir -p /home/foo/www/ttrss
```

Create a sample `ttrss/index.html` ...

```bash
<html>
<head>
<title>My RSS Reader</title>
</head>
<body bgcolor="red" text="white">
<center><h1>Coming soon -- The future home of the Tiny Tiny RSS Reader!</h1></center>
</body>
</html>
```

Create a new server block configuration `/etc/nginx/sites-available/ttrss` ...

```bash
server {
        listen 80;
        listen [::]:80;

        root /home/foo/www/ttrss;
        index index.html;

        access_log /var/log/nginx/ttrss_access.log;
        error_log /var/log/nginx/ttrss_error.log info;

        server_name ttrss.*;

        location / {
            index           index.html;
        }
}
```

Activate the new server block ...

```bash
$ cd /etc/nginx/sites-enabled
$ sudo ln -s ../sites-available/ttrss
$ sudo systemctl restart nginx
```

#### 2.1 Add hostname to HOSTS

On the Linux client device, modify `/etc/hosts` by adding the `ttrss.lan` address ...

```bash
192.168.1.88    ttrss.lan
```

... then navigate to `http://ttrss.lan`` to see the new webpage.

## 3. PostgreSQL

Install ...
                                                                                    
```bash
$ sudo apt install postgresql postgresql-contrib
$ sudo systemctl start postgresql
```

Launch the PostgreSQL interactive console front-end `psql` as the `postgres` user and set a new password ...                            

```bash
$ sudo -u postgres psql postgres
postgres=# \password postgres
Enter new password: [newpasswd]
Enter it again: [newpasswd]
postgres=# \quit
```

**Example:** Create a new username `www-data` and database `ttrss` ... [^1]

```bash                                                               
$ sudo -u postgres psql postgres
postgres=# CREATE USER "www-data" WITH PASSWORD 'newpasswd';  
postgres=# CREATE DATABASE ttrss WITH OWNER "www-data";                         
postgres=# GRANT ALL PRIVILEGES ON DATABASE ttrss to "www-data";                
postgres=# \quit
```

Reload server and check status ...                                                             
                                                                                    
```bash
$ sudo systemctl restart postgresql
$ systemctl status postgresql
```

## 4. Helpful resources

* [How to install the LEMP stack on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-14-04)
* [Set up Nginx Server Blocks](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-14-04-lts)
* [PostgreSQL and Ubuntu](https://help.ubuntu.com/community/PostgreSQL)
* [Practical PostgreSQL database](http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm)

Happy hacking!

#### Notes

[^1]: PostgreSQL maintains its own users and passwords, which are separate from the Linux user accounts. It is not required that your PostgreSQL usernames match the Linux usernames. However, the default setup for PostgreSQL is to give access to system users (e.g. postgres, www-data). See [Practical PostgreSQL database](http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm).
