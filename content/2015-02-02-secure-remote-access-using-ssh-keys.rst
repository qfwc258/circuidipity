===================================
Secure remote access using SSH keys
===================================

:date: 2015-02-02 00:05:00
:slug: secure-remote-access-using-ssh-keys
:tags: ssh, crypto, network, debian, linux, raspberry pi
:modified: 2015-07-05 16:02:00

`Raspberry Pi Home Server Hack #1 .: <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ Create **cryptographic keys** and disable password logins to make remote machines more secure.

Let's go!
=========

**Server** is a `Raspberry Pi 2 <http://www.circuidipity.com/tag-raspberry-pi.html>`_ running `Debian <http://www.circuidipity.com/raspberry-pi-usb-storage-v4.html>`_ configured for SSH logins (``login:pi/ip_address:192.168.1.88``) from a Debian **client** device.

0. Install
==========

On the server
-------------

Install ``openssh-server`` and create an SSH configuration in the home directory of users who requires access to the system:

.. code-block:: bash                                                                
                                                                                    
    $ sudo apt-get install openssh-server                                           
    $ mkdir ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
                                                                                    
Collect key fingerprints:                                                      
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ ssh-keygen -lf /etc/ssh/ssh_host_dsa_key.pub >> ~/.ssh/keys.txt               
    $ ssh-keygen -lf /etc/ssh/ssh_host_ecdsa_key.pub >> ~/.ssh/keys.txt             
    $ ssh-keygen -lf /etc/ssh/ssh_host_rsa_key.pub >> ~/.ssh/keys.txt               
                                                                                    
... and give ``keys.txt`` to users to compare signature when connecting for the first time.            
                                                                                    
On the client
-------------

Install ``openssh-client`` and create the SSH folder in ``home``:

.. code-block:: bash                                                                
                                                                                    
  $ sudo apt-get install openssh-client                                             
  $ mkdir ~/.ssh && chmod 700 ~/.ssh                                                
                                                                                    
Create ``~/.ssh/config`` to hold **aliases** with the login options for a server (example):                          

.. code-block:: bash                                                                
                                                                                    
    Host raspberry.lan                                                                   
    HostName 192.168.1.88                                                        
    Port 22                                                                      
    User pi

Test SSH password login to the server:

.. code-block:: bash

    $ ssh raspberry.lan
    pi@192.168.1.88's password: 
    Last login: Thu Feb 19 18:07:48 2015 from chromebook.lan
    $

**Optional:** Use `Dynamic DNS (DDNS) <http://www.circuidipity.com/ddns-openwrt.html>`_ for configuring access to the server from anywhere in the world.

1. Keys
=======

On the client
-------------
                                                                                
Generate SSH keys:
  
.. code-block:: bash

    $ ssh-keygen -t rsa -C "$(whoami)@$(hostname)-$(date -I)" 
                                                                                
Upload the **public key** to the server and append to ``~/.ssh/authorized_keys``: 
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ cat ~/.ssh/id_rsa.pub | ssh raspberry.lan "cat >> ~/.ssh/authorized_keys"        

Graphical display managers like ``gdm`` will automatically check a user account for SSH keys upon login. A pop-up box will prompt for the passphrase and the key will be added to the desktop session.

If logging into a console, tell SSH that you have keys by running ``ssh-add``:

.. code-block:: bash

    $ ssh-add
    $ Enter passphrase for /home/pi/.ssh/id_rsa:
    Identity added: /home/pi/.ssh/id_rsa (/home/pi/.ssh/id_rsa)

All SSH sessions launched from this console will access this user key stored in memory. Make sure to test the connection before disabling password logins:

.. code-block:: bash

    $ ssh raspberry.lan
    Last login: Thu Feb 19 18:22:42 2015 from chromebook.lan
    $

No request for passphrase indicates SSH key authentication is properly configured.    

2. Disable password logins 
==========================

On the server
-------------
                                                                                
Make the following modifications in ``/etc/ssh/sshd_config``:                                         
                                                                                
.. code-block:: bash                                                            
                                                                                
    PubkeyAuthentication yes                                                    
    ChallengeResponseAuthentication no                                          
    PasswordAuthentication no                                                   
    UsePAM no                                                                   
                                                                                
Restart SSH:

.. code-block:: bash

    $ sudo systemctl restart ssh

3. Key management
=================

`Keychain <http://www.funtoo.org/Keychain>`_ is an OpenSSH key manager. From the package description:

    When keychain is run, it checks for a running ssh-agent, otherwise it starts one. It saves the ssh-agent environment variables to ``~/.keychain/$HOSTNAME-sh``, so that subsequent logins and non-interactive shells such as cron jobs can source the file and make passwordless ssh connections.  In addition, when keychain runs, it verifies that the key files specified on the command-line are known to ssh-agent, otherwise it loads them, prompting you for a password if necessary.

On the client
-------------
                                                                                
Install:
  
.. code-block:: bash

    $ sudo apt-get install keychain                                             
                                                                                
Configure ``~/.bashrc``:                                                           
                                                                                
.. code-block:: bash                                                            
                                                                                
    # setup keychain - ssh-agent management                                     
    keychain ~/.ssh/id_rsa                                                      
    . ~/.keychain/$HOSTNAME-sh                                                  
                                                                                
Flush all cached keys from memory:
  
.. code-block:: bash

    $ keychain --clear                  
                                                                                
**Optional:** if using `tmux <http://www.circuidipity.com/tmux.html>`_ enable persistent SSH key management across sessions by editing ``~/.tmux.conf``: 
                                                                                
.. code-block:: bash                                                            
                                                                                
    set-option -g update-environment "DISPLAY SSH_ASKPASS SSH_AUTH_SOCK SSH_AGENT_PID SSH_CONNECTION WINDOWID XAUTHORITY"

Happy hacking!
