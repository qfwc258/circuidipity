========================
PHP + Nginx + PostgreSQL
========================

:date: 2015-02-09 18:29:00
:slug: php-nginx-postgresql
:tags: networks, web, ubuntu, linux
:modified: 2015-03-01 19:48:00

`Raspberry Pi Home Server Hack #6 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ As a requirement to host web applications like `Tiny Tiny RSS <http://www.circuidipity.com/ttrss.html>`_ on my Raspberry Pi I install **PHP**, the lightweight web server **Nginx**, and the **PostgreSQL** database.

Let's go!
=========

**Server** is a `Raspberry Pi 2 <http://www.circuidipity.com/run-a-raspberry-pi-2-from-external-usb-storage.html>`_ running Ubuntu 14.04 LTS located at ip address ``192.168.1.88``.

0. PHP
======

Install:

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get install php5 php5-fpm php-apc php5-curl php5-cli php5-pgsql php5-gd php5-mcrypt

To improve security edit ``/etc/php5/fpm/php.ini`` and change **pathinfo** to ``0``:                          
                                                                                
.. code-block:: bash

    cgi.fix_pathinfo=0                                                              

Restart PHP:
                                                                                    
.. code-block:: bash

    $ sudo service php5-fpm restart                                             
                                                                                    
1. Nginx
========

Install:

.. code-block:: bash

    $ sudo apt-get install nginx                                                    
    $ sudo service nginx start                                                  
                                                                                    
To verify that the web server is running, open a browser and navigate to (example) ``http://192.168.1.88``. If you see ``Welcome to nginx!`` the server is installed correctly.

2. Host multiple domains
========================

Nginx is capable of serving up multiple web domains or **server blocks** (virtual hosts) from the same server:

* block content is placed in subfolders located in ``/usr/share/nginx/html``
* configuration in ``/etc/nginx/sites-available``
* a server block is made active by setting a symbolic link in ``/etc/nginx/sites-enabled`` to its config file

When combined with a `free DDNS service <http://www.circuidipity.com/ddns-openwrt.html>`_ (I like `duckdns.org <http://duckdns.org/>`_) multiple custom domains can be hosted on a home server.

Example: create a sample ``my2pi`` server block to host ``www.my2pi.com``:

2.1 CNAME
---------

Create a new **CNAME** record at the domain registrar to redirect ``www.my2pi.com`` to ``my2pi.duckdns.org``.

2.2 Document Root
-----------------

Create a new root directory to hold the contents of ``my2pi``:

.. code-block:: bash

    $ sudo mkdir /usr/share/nginx/html/my2pi
    $ sudo chown -R $USER.$USER /usr/share/nginx/html/my2pi

2.3 Index.html
--------------

Create a sample ``/usr/share/nginx/html/my2pi/index.html``:

.. code-block:: bash

    <html>
    <head>
    <title>My Pi 2 Home</title>
    </head>
    <body bgcolor="white" text="black">
    <center><h1>Welcome to My Pi 2 Home!</h1></center>
    </body>
    </html>

2.4 Server Block
----------------

I use ``/etc/nginx/sites-available/default`` as a template for the new ``my2pi`` configuration:

.. code-block:: bash

    $ cd /etc/nginx/sites-available
    $ sudo cp default my2pi

Modify these lines for the custom domain:

.. code-block:: bash

    listen 80;

    root /usr/share/nginx/html/my2pi;                                           
    index index.html index.htm;

    server_name www.my2pi.com; 

Activate the new server block:

.. code-block:: bash

    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s ../sites-available/my2pi
    $ sudo service nginx restart

2.5 Port Forwarding
-------------------

Configure `port forwarding on the home router <http://www.circuidipity.com/20141006.html>`_ to redirect traffic on port 80 to the internal IP address of the nginx server. Point your browser to ``www.my2pi.com``. Success (hopefully)!

Repeat the above steps to add more domains. The limiting factor is the **upload bandwidth** provided by the home ISP (typically a fraction of the download speed).

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
                                                                                    
Example: To create a new user ``www-data`` [1]_ and database ``mydb``:

.. code-block:: bash                                                               
    
    $ sudo -u postgres psql                                                                                
    postgres=# CREATE USER "www-data" WITH PASSWORD 'newpasswd';  
    postgres=# CREATE DATABASE mydb WITH OWNER "www-data";                         
    postgres=# GRANT ALL PRIVILEGES ON DATABASE mydb to "www-data";                
    postgres=# \quit
                      
Save any changes and reload the database server:                                                             
                                                                                    
.. code-block:: bash

    $ sudo service postgresql reload

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
