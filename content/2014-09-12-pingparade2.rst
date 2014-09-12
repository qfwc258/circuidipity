======================
Ping Parade #2 -- Keys
======================

:slug: pingparade2
:tags: network, debian, linux
:template: article-project-pingparade

**Create cryptographic keys and disable password logins to make remote machines more secure.**

.. image:: images/pingparade2-0.png
    :alt: OpenSSH
    :width: 960px
    :height: 500px

**OpenSSH** is a toolkit for securing communication with Unix-like remote machines and services and supports authenticating users with a public and private **key pair**. Michael Lucas, author of `OpenSSH Mastery <https://www.michaelwlucas.com/nonfiction/ssh-mastery>`_, describes the risk of passwords in SSH:

    For the last few years, a network of compromised machines dubbed the "Hail Mary Cloud" has scanned the Internet for SSH servers. When a member of this cloud finds an SSH server, it lets the other machines in the network know about it. The cloud then methodically tries possible usernames and passwords. One host on the network tries a few times, then another, then another. Blocking individual IP addresses is not a useful defense, because each address is used only a few times.

    Any one attempt has low odds of guessing successfully. The attempts are constant. They never end. Eventually [some automated attacker] will get lucky and break into your server. It might be tomorrow, or next year, but it _will_ happen. To stop these types of attacks, you can either use packet filtering to block public access to your SSH server, or you can eliminate passwords on your servers. User keys let you eliminate passwords.

This is how to configure SSH key authentication between a `home server <http://www.circuidipity.com/pingparade1.html>`_ and a client such as a laptop that are both running **Debian Linux**.

Step 0 - Install                                             
================

**On the server:**                                                                
               
* install ``openssh-server`` and create an SSH configuration in the home directory of users who requires access to the system ...

.. code-block:: bash                                                                
                                                                                    
    $ sudo apt-get install openssh-server                                           
    $ mkdir ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
                                                                                    
* collect key fingerprints from the server...                                                      
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ ssh-keygen -lf /etc/ssh/ssh_host_dsa_key.pub >> ~/.ssh/keys.txt               
    $ ssh-keygen -lf /etc/ssh/ssh_host_ecdsa_key.pub >> ~/.ssh/keys.txt             
    $ ssh-keygen -lf /etc/ssh/ssh_host_rsa_key.pub >> ~/.ssh/keys.txt               
                                                                                    
... and give ``keys.txt`` to users to compare signature when connecting for the first time            
                                                                                    
* *optional:* edit ``/etc/ssh/sshd_config`` adding specific users to be granted system access (**disabling** all others by default) ...

.. code-block:: bash
                                                                                    
  AllowUsers USERNAME1 USERNAME2

Save and restart SSH with the new config by running ``sudo service ssh restart``                           
                                                                                    
**On the client:**                                                                

* install ``openssh-client`` and create the SSH folder in the user home directory ...

.. code-block:: bash                                                                
                                                                                    
  $ sudo apt-get install openssh-client                                             
  $ mkdir ~/.ssh && chmod 700 ~/.ssh                                                
                                                                                    
* *optional:* create an entry in ``~/.ssh/config`` with the login options for a server - for example ...                              
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    Host tyrell                                                                     
    HostName 192.168.1.88                                                        
    Port 23456                                                                      
    User gaff                                                                       
     
Step 1 - Generate keys                                                                   
======================

**On the client:**                                                            
                                                                                
* generate keys by running ``ssh-keygen -t rsa -C "$(whoami)@$(hostname)-$(date -I)"`` and supply a passphrase     
                                                                                
* upload the public key to the server and append it to ``~/.ssh/authorized_keys`` ...             
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ cat ~/.ssh/id_rsa.pub | ssh SERVER "cat >> ~/.ssh/authorized_keys"        

Step 2 - Test
=============

**On the client:**

Graphical display managers like ``gdm`` will automatically check a user account for SSH keys upon login. A pop-up box will prompt for the passphrase and the key will be added to the desktop session.

If logging into a console, tell SSH that you have keys by running ``ssh-add`` ...

.. code-block:: bash

    $ ssh-add
    $ Enter passphrase for /home/gaff/.ssh/id_rsa:
    Identity added: /home/gaff/.ssh/id_rsa (/home/gaff/.ssh/id_rsa)

All SSH sessions launched from this console will access this user key stored in memory. Make sure to test the connection before disabling password logins ...

.. code-block:: bash

    $ ssh 192.168.1.88
    Last login: Thu Sep 11 23:46:28 2014 from kambei.lan
    $ uname -n
    tyrell

No request to enter a passphrase indicates SSH key authentication is properly configured.    

Step 3 - Disable password logins                                                
================================

**On the server:**                                                               
                                                                                
* edit ``/etc/ssh/sshd_config`` ...                                                
                                                                                
.. code-block:: bash                                                            
                                                                                
    PubkeyAuthentication yes                                                    
    ChallengeResponseAuthentication no                                          
    PasswordAuthentication no                                                   
    UsePAM no                                                                   
                                                                                
... and restart the SSH server ``sudo service ssh restart``                                               
                                  
Step 4 - Key management                                                     
=======================

`Keychain <http://www.funtoo.org/Keychain>`_ is an OpenSSH key manager. From the Debian package description:

    When keychain is run, it checks for a running ssh-agent, otherwise it starts one. It saves the ssh-agent environment variables to ``~/.keychain/$HOSTNAME-sh``, so that subsequent logins and non-interactive shells such as cron jobs can source the file and make passwordless ssh connections.  In addition, when keychain runs, it verifies that the key files specified on the command-line are known to ssh-agent, otherwise it loads them, prompting you for a password if necessary.

**On the client:**                                                            
                                                                                
* install ``sudo apt-get install keychain``                                             
                                                                                
* configure ``~/.bashrc`` ...                                                           
                                                                                
.. code-block:: bash                                                            
                                                                                
    # setup keychain - ssh-agent management                                     
    keychain ~/.ssh/id_rsa                                                      
    . ~/.keychain/$HOSTNAME-sh                                                  
                                                                                
* flush all cached keys from memory with ``keychain --clear``                   
                                                                                
* if using `tmux <http://www.circuidipity.com/tmux.html>`_ enable persistent SSH key management across sessions by editing ``~/.tmux.conf`` ...                                                   
                                                                                
.. code-block:: bash                                                            
                                                                                
    set-option -g update-environment "DISPLAY SSH_ASKPASS SSH_AUTH_SOCK SSH_AGENT_PID SSH_CONNECTION WINDOWID XAUTHORITY"

Happy hacking!
