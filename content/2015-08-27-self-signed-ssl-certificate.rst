====================================
Create a self-signed SSL certificate
====================================

:date: 2015-08-27 19:25:00
:slug: self-signed-ssl-certificate
:tags: network, debian, linux

Secure web access to services hosted on a `Raspberry Pi home server <http://www.circuidipity.com/raspberry-pi-home-server.html>`_.

**What's up:** I am running `Tiny Tiny RSS <http://www.circuidipity.com/ttrss.html>`_ (ttrss) and `Nginx <http://www.circuidipity.com/php-nginx-postgresql.html>`_ on a Debian-powered Pi and want to divert HTTP traffic from port 80 to HTTPS login and access news feeds on port 443. Rather than obtain an SSL certificate from a certificate authority (CA) its a simple matter to create one for personal use. 

Install ``openssl`` and generate a certificate for Nginx:

.. code-block:: bash

    $ sudo apt-get install openssl
    $ sudo mkdir /etc/nginx/ssl
    $ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.crt

Create a new server block in ``/etc/nginx/sites-available``: 

.. code-block:: bash

    server {
        listen 80; ## listen for ipv4; this line is default and implied
        server_name rss.myraspberrypi.ca;
        return 301 https://$host$request_uri;  ## redirect all non-https traffic to https 
    }

    server {
        listen 443 ssl;
        server_name rss.myraspberrypi.ca;
        ssl_certificate /etc/nginx/ssl/server.crt;
        ssl_certificate_key /etc/nginx/ssl/server.key;
        [...]

Activate the block by creating a symlink in ``/etc/nginx/sites-enabled`` and restart server:

.. code-block:: bash

    $ sudo systemctl restart nginx
    
Configure `port forwarding on the router <http://www.circuidipity.com/20141006.html>`_ and (optional) `setup a subdomain <https://wiki.gandi.net/en/dns/zone/subdomain>`_ with a hosting/domain provider.

Note the first time navigating to the new HTTPS address the (Firefox) browser warns "This Connection is Untrusted" (which is to be expected since its a self-signed certificate vs CA verification).

Happy hacking!

Sources: `Create an SSL certificate on Nginx for Ubuntu <https://www.digitalocean.com/community/tutorials/how-to-create-an-ssl-certificate-on-nginx-for-ubuntu-14-04>`_; `Rewrite HTTP requests to HTTPS <https://serverfault.com/questions/67316/in-nginx-how-can-i-rewrite-all-http-requests-to-https-while-maintaining-sub-dom>`_; `Nginx server_names <http://nginx.org/en/docs/http/server_names.html>`_
