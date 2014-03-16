=========================================================
Hosting multiple domains from one IP address using Apache
=========================================================

:tags: web, network, linux, debian
:slug: hosting-multiple-domains-from-one-ip-address-using-apache

Creating *virtual hosts* in Apache makes it possible to host multiple websites from a single IP address.

My old netbook has discovered new life as a `Linux home server <http://www.circuidipity.com/linux-home-server.html>`_. A combination of `name-based virtual hosting <http://httpd.apache.org/docs/2.0/vhosts/name-based.html>`_ in Apache + Debian ``squeeze`` allows me to host multiple websites running behind a single static IP address I obtained from my ISP.

This is my setup ...

Step 0 - Install Apache
=======================

.. code-block:: bash

    $ sudo apt-get install apache2
    $ /etc/init.d/apache2 start

Confirm the web server is up-and-running by navigating to `localhost <http://localhost/>`_ ... You should now see:

.. code-block:: bash

    It works!

    This is the default web page for this server.

    The web server software is running but no content has been added, yet.

Apache's default page is located at ``/var/www/index.html``. Enabling Apache to host multiple domains requires giving each website:

* its own directory to hold files
  
* a virtual host configuration

Step 1 - Website directory
==========================

Create a directory for the website and grant ownership to USERNAME ...

.. code:: bash

    $ sudo mkdir /var/www/SITENAME
    $ sudo chown USERNAME:USERNAME /var/www/SITENAME

Step 2 - Virtual host
=====================

Create a new virtual host configuration for the website by copying Apache's ``default`` configuration to the new sitename ...

.. code-block:: bash

    $ sudo cd /etc/apache2/sites-available/
    $ sudo cp default SITENAME

Edit the newly-created configuration to match the new website settings ...

.. code-block:: bash

    <VirtualHost *:80>
    ServerName SITENAME
        ServerAlias *.SITENAME
        ServerAdmin admin@SITENAME

        DocumentRoot /var/www/SITENAME
        <Directory />
            Options FollowSymLinks
            AllowOverride None
        </Directory&gt>
        <Directory /var/www/SITENAME/>

Enable the new site in Apache ...

.. code-block:: bash

    $ sudo a2ensite SITENAME
    $ sudo /etc/init.d/apache2 restart

If you want to be able to view the website on the same localhost it is being served from ... modify ``/etc/hosts`` by adding a *testing* domain to the localhost address ...

.. code-block:: bash

    127.0.1.1       test.*sitename*

... and another ... and another ...

Copy the steps for each additional website ... giving each site a unique name and virtual host configuration.

Step 3 - Extra: Web-enabled user directory
==========================================

Create a folder in a user's home directory with contents made available over the web ...

.. code-block:: bash

    $ mkdir /home/USERNAME/public_html

Configure Apache to allow outside access to the folder by editing ``/etc/apache2/mods-available/userdir.conf`` ...

.. code-block:: bash

    <IfModule mod_userdir.c>
    UserDir public_html
    UserDir disabled root
    UserDir enabled USERNAME

Enable the ``userdir`` module and reload Apache ...

.. code-block:: bash

    $ sudo a2enmod userdir
    $ sudo /etc/init.d/apache2 restart

Navigate to http://localhost/~USERNAME_ to view the contents of ``/home/USERNAME/public_html`` ... Outside your LAN a user would travel to http://YOUR_IP_ADDRESS/~USERNAME.
