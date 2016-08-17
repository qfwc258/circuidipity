========================
PHP + Nginx + PostgreSQL
========================

:date: 2015-02-09 18:29:00
:slug: php-nginx-postgresql
:tags: server, network, linux
:modified: 2015-08-26 12:48:00

`Home Server Project #6 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ As a requirement to host web applications like `Tiny Tiny RSS <http://www.circuidipity.com/ttrss.html>`_ on my Raspberry Pi I install **PHP**, the lightweight proxy server **Nginx**, and the **PostgreSQL** database.

Let's go!
=========

**Setup:** `Raspberry Pi 2 <http://www.circuidipity.com/raspberry-pi-usb-storage-v4.html>`_ with IP ADDRESS ``192.168.1.88`` running Debian.

0. PHP
======

Install:

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get install php5 php5-fpm php-apc php5-curl php5-cli php5-pgsql php5-gd php5-mcrypt

Improve security by editing ``/etc/php5/fpm/php.ini`` and modifying **pathinfo** to ``0``:                          
                                                                                
.. code-block:: bash

    cgi.fix_pathinfo=0                                                              

Restart PHP:
                                                                                    
.. code-block:: bash

    $ sudo systemctl restart php5-fpm                                           
                                                                                    
1. Nginx
========

Install:

.. code-block:: bash

    $ sudo apt-get install nginx                                                    
    $ sudo systemctl start nginx                                                  
                                                                                    
Verify web server is running by opening a browser and navigating to ``http://192.168.1.88``. If you see ``Welcome to nginx!`` the server is installed correctly.

2. Host multiple domains
========================

Nginx is capable of serving up multiple web domains or **server blocks** (virtual hosts) from the same server:

* I create ``~/html`` to hold block content in subfolders
* Create block configs in ``/etc/nginx/sites-available``
* A block is made active by setting a symbolic link in ``/etc/nginx/sites-enabled`` to its config file

When combined with a `free DDNS service <http://www.circuidipity.com/ddns-openwrt.html>`_ multiple custom domains can be hosted on a home server.

**Example:** Setup a ``myraspberry`` server block to host ``www.myraspberry.ca`` using `duckdns.org <http://duckdns.org/>`_ DDNS.

2.1 CNAME
---------

Create a new **CNAME** record at the domain registrar to redirect ``www.myraspberry.ca`` to ``myraspberry.duckdns.org``.

2.2 Document Root
-----------------

Create a new root directory to hold the contents of ``myraspberry``:

.. code-block:: bash

    $ mkdir -p ~/html/myraspberry

2.3 Index.html
--------------

Create a sample ``~/html/myraspberry/index.html``:

.. code-block:: bash

    <html>
    <head>
    <title>My Raspberry Pi 2 Home</title>
    </head>
    <body bgcolor="red" text="white">
    <center><h1>Welcome to My Pi!</h1></center>
    </body>
    </html>

2.4 Server Block
----------------

Create a new server block configuration ``/etc/nginx/sites-available/myraspberry``:

.. code-block:: bash

    server {
        listen 80; ## listen for ipv4; this line is default and implied

        root /home/USER/html/myraspberry;  ## Replace USER with your username
        index index.html;

        access_log /var/log/nginx/ttrss_access.log;
        error_log /var/log/nginx/ttrss_error.log info;

        server_name myraspberry.*;

        location / {
            index           index.html;
        }
    }

Activate the new server block:

.. code-block:: bash

    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s ../sites-available/myraspberry
    $ sudo systemctl restart nginx

2.5 Port Forwarding
-------------------

Configure `port forwarding on the home router <http://www.circuidipity.com/20141006.html>`_ to redirect traffic on port 80 to the internal IP address of the nginx server. Repeat the above steps to add more domains. The limiting factor is the **upload bandwidth** provided by the home ISP (typically a fraction of the download speed).

3. PostgreSQL
=============

Install:
                                                                                    
.. code-block:: bash

    $ sudo apt-get install postgresql                                                       
                                                                                    
Launch the PostgreSQL interactive console front-end ``psql`` as ``postgres`` user and set a new password:                                 

.. code-block:: bash

    $ sudo -u postgres psql                                               
    postgres=# \password postgres
    Enter new password: [newpasswd]
    Enter it again: [newpasswd]
    postgres=# \quit
                                                                                    
Example: Create new ``user:www-data`` and ``database:mydb``: [1]_

.. code-block:: bash                                                               
    
    $ sudo -u postgres psql                                                                                
    postgres=# CREATE USER "www-data" WITH PASSWORD 'newpasswd';  
    postgres=# CREATE DATABASE mydb WITH OWNER "www-data";                         
    postgres=# GRANT ALL PRIVILEGES ON DATABASE mydb to "www-data";                
    postgres=# \quit
                      
Save any changes and reload server:                                                             
                                                                                    
.. code-block:: bash

    $ sudo systemctl restart postgresql.service

4. Helpful resources
====================

* `How to install the LEMP stack on Ubuntu <https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-14-04>`_
* `Set up Nginx Server Blocks <https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-14-04-lts>`_
* `PostgreSQL and Ubuntu <https://help.ubuntu.com/community/PostgreSQL>`_
* `Practical PostgreSQL database <http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm>`_
* `DDNS and OpenWrt <http://www.circuidipity.com/ddns-openwrt.html>`_

Happy hacking!

Notes
-----

.. [1] PostgreSQL maintains its own users and passwords, which are separate from the Linux user accounts. It is not required that your PostgreSQL usernames match the Linux usernames. See `Practical PostgreSQL database <http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm>`_.
