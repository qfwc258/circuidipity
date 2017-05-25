=================================
Verify a PGP signature with GnuPG
=================================

:date: 2015-07-19 11:33:00
:slug: verify-pgp-signature-gnupg
:tags: pgp, crypto, debian, linux

Using a **PGP private/public keypair** to create a **digital signature** for a file certifies its integrity. Adding a signature to software available for download heightens confidence that everything is OK!

Let's go!
=========

A developer signs a package with their private key and the receiver verifies the signature with the public key. If the package has been modified or corrupted in transmission the verification will fail.

0. Download
============

**GnuPG** is used to verify PGP signatures:

.. code-block:: bash

    $ sudo apt-get install gnupg                                                                
                                                                                     
**Example:** I download a `Debian Jessie for Raspberry Pi 2 <http://sjoerd.luon.net/posts/2015/02/debian-jessie-on-rpi2/>`_ image and its signature:

.. code-block:: bash

    $ wget https://images.collabora.co.uk/rpi2/jessie-rpi2-20150705.img.gz                 
    $ wget https://images.collabora.co.uk/rpi2/jessie-rpi2-20150705.img.gz.asc             

1. Import
=========

Method 0
--------

If the location of the developer's public key is known, I can directly import the key into my keyring (``~/.gnupg/pubring.gpg``):

.. code-block:: bash

    $ gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 0xC2300F7B
                                                                                         
Method 1
--------

Identify the public key used to generate the signature:

.. code-block:: bash
                                                
    $ gpg --verify jessie-rpi2-20150705.img.gz.asc             
    gpg: Signature made Sun 05 Jul 2015 09:06:01 AM EDT using RSA key ID C2300F7B   
    gpg: Can't check signature: public key not found                                     
                                                                                     
Public key is ``0xC2300F7B``. Run a key search [1]_ and import:

.. code-block:: bash
                                          
    $ gpg --search 0xC2300F7B                                                            
    gpg: keyring `/home/dwa/.gnupg/secring.gpg' created                                  
    gpg: searching for "0xC2300F7B" from hkp server keys.gnupg.net                       
    (1)     Sjoerd Simons <sjoerd@luon.net>                                              
            Sjoerd Simons <sjoerd@debian.org>                                            
            Antonius Gerardus Johannes Simons <sjoerd@luon.net>                          
                4096 bit RSA key C2300F7B, created: 2014-04-25                             
    Keys 1-1 of 1 for "0xC2300F7B".  Enter number(s), N)ext, or Q)uit > 1                
    gpg: requesting key C2300F7B from hkp server keys.gnupg.net                          
    gpg: key C2300F7B: public key "Sjoerd Simons <sjoerd@luon.net>" imported             
    gpg: no ultimately trusted keys found                                                
    gpg: Total number processed: 1                                                       
    gpg:               imported: 1  (RSA: 1)                                             

2. Verify
=========
                                                                                     
List keys in my keyring:

.. code-block:: bash
                                                               
    $ gpg --list-keys                                                                    
    /home/dwa/.gnupg/pubring.gpg                                                         
    ----------------------------                                                         
    pub   4096R/C2300F7B 2014-04-25                                                      
    uid                  Sjoerd Simons <sjoerd@luon.net>                                 
    uid                  Sjoerd Simons <sjoerd@debian.org>                               
    uid                  Antonius Gerardus Johannes Simons <sjoerd@luon.net>             
    sub   4096R/92545E8E 2014-04-25                                                      
                                                                                     
Verify package signature:

.. code-block:: bash
                                                          
    $ gpg --verify jessie-rpi2-20150705.img.gz.asc jessie-rpi2-20150705.img.gz        
    gpg: Signature made Sun 05 Jul 2015 09:06:01 AM EDT using RSA key ID C2300F7B   
    gpg: Good signature from "Sjoerd Simons <sjoerd@luon.net>"                      
    gpg:                 aka "Sjoerd Simons <sjoerd@debian.org>"                    
    gpg:                 aka "Antonius Gerardus Johannes Simons <sjoerd@luon.net>"  
    gpg: WARNING: This key is not certified with a trusted signature!               
    gpg:          There is no indication that the signature belongs to the owner.   
    Primary key fingerprint: 2870 A31B EA9D BCF2 7472  3108 C274 DB64 C230 0F7B  

The warning about **key is not certified with a trusted signature** means GnuPG verified that key made that signature but can't guarantee that key really belongs to the developer. It's up to me to decide how much confidence to place in the authenticity of the key.

Happy hacking!
   
Notes
-----

.. [1] Auto-generated ``~/.gnupg/gpg.conf`` defaults to searching ``keyserver hkp://keys.gnupg.net`` which redirects to the `SKS Keyservers pool <https://sks-keyservers.net/>`_.
