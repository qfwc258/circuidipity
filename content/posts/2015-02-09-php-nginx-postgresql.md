---
title: "PHP + Nginx + PostgreSQL"
date: "2017-05-19"
publishDate: "2015-02-09"
tags:
  - php
  - nginx
  - postgres
  - network
  - debian
  - linux
slug: "php-nginx-postgresql"
aliases:
  - /php-nginx-postgresql.html
---

:penguin: [Home Server](http://www.circuidipity.com/home-server/) :: As a requirement to host web applications like [Tiny Tiny RSS](http://www.circuidipity.com/ttrss.html) on my home server I install **PHP**, the lightweight proxy server **Nginx**, and the **PostgreSQL** database.

## Let's go!

**Setup:** [Netbook](http://www.circuidipity.com/laptop-home-server.html) with IP ADDRESS `192.168.1.88` running the latest stable release of Debian.

## 0. PHP

Install ...

```bash
sudo apt install php php-fpm php-apcu php-curl php-cli php-pgsql php-gd php-mcrypt php-mbstring php-fdomdocument
```

Improve security by editing `/etc/php/7.0/fpm/php.ini` and modifying `pathinfo` to `0` ...

```bash
cgi.fix_pathinfo=0                                                              
```

Restart PHP ...
                                                                                    
```bash
sudo systemctl restart php7.0-fpm
```

## 1. Nginx

Install ...

```bash
sudo apt install nginx-common
sudo apt install nginx                                                    
sudo systemctl start nginx                                                  
```

Verify web server is running by opening a browser and navigating to `http://192.168.1.88`. If you see `Welcome to nginx!` the server is installed correctly.

## 2. Host multiple domains

Nginx is capable of serving up multiple web domains or **server blocks** (virtual hosts):

* I create `/home/USERNAME/www` to hold block content in subfolders
* Create block configs in `/etc/nginx/sites-available`
* A block is made active by setting a symbolic link in `/etc/nginx/sites-enabled` to its block config

When combined with a [free DDNS service](http://www.circuidipity.com/ddns-openwrt.html) multiple custom domains can be hosted on a home server.

### 2.1 Document Root

**Example:** Setup a `myfoo` server block to host `www.myfoo.ca` using [duckdns.org](http://duckdns.org/) DDNS.

Create a new root directory to hold the contents of `myfoo` ...

```bash
mkdir -p /home/USERNAME/www/myfoo
```

### 2.2 Index.html

Create a sample `myfoo/index.html` ...

```bash
<html>
<head>
<title>My Foo Home</title>
</head>
<body bgcolor="red" text="white">
<center><h1>Welcome to More Foo!</h1></center>
</body>
</html>
```

### 2.3 Server Block

Create a new server block configuration `/etc/nginx/sites-available/myfoo` ...

```bash
server {
        listen 80;
        listen [::]:80;

        root /home/USERNAME/www/myfoo;
        index index.html;

        access_log /var/log/nginx/myfoo_access.log;
        error_log /var/log/nginx/myfoo_error.log info;

        server_name myfoo.*;

        location / {
            index           index.html;
        }
}
```

Activate the new server block ...

```bash
sudo cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/myfoo
sudo systemctl restart nginx
```

### 2.4 CNAME

Create a new **CNAME** record at the domain registrar to redirect `www.myfoo.ca` to `myfoo.duckdns.org`.

### 2.5 Port Forwarding

Configure [port forwarding on the home router](http://www.circuidipity.com/20141006.html) to redirect traffic on port 80 to the internal IP address of the nginx server. Repeat the above steps to add more domains. The real limiting factor is the **upload bandwidth** provided by the home ISP (typically a fraction of the download speed).

## 3. PostgreSQL

Install ...
                                                                                    
```bash
sudo apt install postgresql                                                       
```

Launch the PostgreSQL interactive console front-end `psql` as `postgres` user and set a new password ...                            

```bash
su -c psql postgres
postgres=# \password postgres
Enter new password: [newpasswd]
Enter it again: [newpasswd]
postgres=# \quit
```

**Example:** Create new `user:www-data` and `database:mydb` ... [^1]

```bash                                                               
su -c psql postgres
postgres=# CREATE USER "www-data" WITH PASSWORD 'newpasswd';  
postgres=# CREATE DATABASE mydb WITH OWNER "www-data";                         
postgres=# GRANT ALL PRIVILEGES ON DATABASE mydb to "www-data";                
postgres=# \quit
```

Reload server ...                                                             
                                                                                    
```bash
sudo systemctl restart postgresql.service
```

## 4. Helpful resources

* [How to install the LEMP stack on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-14-04)
* [Set up Nginx Server Blocks](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-14-04-lts)
* [PostgreSQL and Ubuntu](https://help.ubuntu.com/community/PostgreSQL)
* [Practical PostgreSQL database](http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm)
* [DDNS and OpenWrt](http://www.circuidipity.com/ddns-openwrt.html)

Happy hacking!

#### Notes

[^1]: PostgreSQL maintains its own users and passwords, which are separate from the Linux user accounts. It is not required that your PostgreSQL usernames match the Linux usernames. See [Practical PostgreSQL database](http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm).
