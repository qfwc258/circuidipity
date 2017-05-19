========================
PHP + Nginx + PostgreSQL
========================

:date: 2015-02-09 18:29:00
:slug: php-nginx-postgresql
:tags: php, nginx, postgres, network, debian, linux
:modified: 2017-05-19 15:48:00

`PROJECT: Home Server #7 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ As a requirement to host web applications like `Tiny Tiny RSS <http://www.circuidipity.com/ttrss.html>`_ on my home server I install **PHP**, the lightweight proxy server **Nginx**, and the **PostgreSQL** database.

Let's go!
=========

**Setup:** `Netbook <http://www.circuidipity.com/laptop-home-server.html>`_ with IP ADDRESS ``192.168.1.88`` running the latest stable release of `Debian <http://www.circuidipity.com/tag-debian.html>`_.

0. PHP
------

Install ...

.. code-block:: bash

    # apt install php php-fpm php-apcu php-curl php-cli php-pgsql php-gd php-mcrypt php-mbstring php-fdomdocument

Improve security by editing ``/etc/php/7.0/fpm/php.ini`` and modifying ``pathinfo`` to ``0`` ...

.. code-block:: bash

    cgi.fix_pathinfo=0                                                              

Restart PHP ...
                                                                                    
.. code-block:: bash

    # systemctl restart php7.0-fpm
    
1. Nginx
--------

Install ...

.. code-block:: bash

    # apt install nginx-common
    # apt install nginx                                                    
    # systemctl start nginx                                                  
                                                                                    
Verify web server is running by opening a browser and navigating to ``http://192.168.1.88``. If you see ``Welcome to nginx!`` the server is installed correctly.

2. Host multiple domains
------------------------

Nginx is capable of serving up multiple web domains or **server blocks** (virtual hosts):

* I create ``/home/USERNAME/www`` to hold block content in subfolders
* Create block configs in ``/etc/nginx/sites-available``
* A block is made active by setting a symbolic link in ``/etc/nginx/sites-enabled`` to its block config

When combined with a `free DDNS service <http://www.circuidipity.com/ddns-openwrt.html>`_ multiple custom domains can be hosted on a home server.

2.1 Document Root
+++++++++++++++++

**Example:** Setup a ``myfoo`` server block to host ``www.myfoo.ca`` using `duckdns.org <http://duckdns.org/>`_ DDNS.

Create a new root directory to hold the contents of ``myfoo`` ...

.. code-block:: bash

    $ mkdir -p /home/USERNAME/www/myfoo

2.2 Index.html
++++++++++++++

Create a sample ``myfoo/index.html`` ...

.. code-block:: bash

    <html>
    <head>
    <title>My Foo Home</title>
    </head>
    <body bgcolor="red" text="white">
    <center><h1>Welcome to More Foo!</h1></center>
    </body>
    </html>

2.3 Server Block
++++++++++++++++

Create a new server block configuration ``/etc/nginx/sites-available/myfoo`` ...

.. code-block:: bash

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

Activate the new server block ...

.. code-block:: bash

    # cd /etc/nginx/sites-enabled
    # ln -s ../sites-available/myfoo
    # systemctl restart nginx

2.4 CNAME
+++++++++

Create a new **CNAME** record at the domain registrar to redirect ``www.myfoo.ca`` to ``myfoo.duckdns.org``.

2.5 Port Forwarding
+++++++++++++++++++

Configure `port forwarding on the home router <http://www.circuidipity.com/20141006.html>`_ to redirect traffic on port 80 to the internal IP address of the nginx server. Repeat the above steps to add more domains. The real limiting factor is the **upload bandwidth** provided by the home ISP (typically a fraction of the download speed).

3. PostgreSQL
-------------

Install ...
                                                                                    
.. code-block:: bash

    # apt install postgresql                                                       
                                                                                    
Launch the PostgreSQL interactive console front-end ``psql`` as ``postgres`` user and set a new password ...                            

.. code-block:: bash

    # su -c psql postgres
    postgres=# \password postgres
    Enter new password: [newpasswd]
    Enter it again: [newpasswd]
    postgres=# \quit
                                                                                    
**Example:** Create new ``user:www-data`` and ``database:mydb`` ... [1]_

.. code-block:: bash                                                               
    
    # su -c psql postgres
    postgres=# CREATE USER "www-data" WITH PASSWORD 'newpasswd';  
    postgres=# CREATE DATABASE mydb WITH OWNER "www-data";                         
    postgres=# GRANT ALL PRIVILEGES ON DATABASE mydb to "www-data";                
    postgres=# \quit
                      
Reload server ...                                                             
                                                                                    
.. code-block:: bash

    # systemctl restart postgresql.service

4. Helpful resources
--------------------

* `How to install the LEMP stack on Ubuntu <https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-14-04>`_
* `Set up Nginx Server Blocks <https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-14-04-lts>`_
* `PostgreSQL and Ubuntu <https://help.ubuntu.com/community/PostgreSQL>`_
* `Practical PostgreSQL database <http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm>`_
* `DDNS and OpenWrt <http://www.circuidipity.com/ddns-openwrt.html>`_

Happy hacking!

Notes
+++++

.. [1] PostgreSQL maintains its own users and passwords, which are separate from the Linux user accounts. It is not required that your PostgreSQL usernames match the Linux usernames. See `Practical PostgreSQL database <http://www.linuxtopia.org/online_books/database_guides/Practical_PostgreSQL_database/c15679_002.htm>`_.
