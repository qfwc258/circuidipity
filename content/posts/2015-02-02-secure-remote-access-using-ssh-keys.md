---
title: "Secure remote access using SSH keys"
date: "2017-05-06"
publishDate: "2015-02-02"
tags:
  - ssh
  - crypto
  - linux
slug: "secure-remote-access-using-ssh-keys"
aliases:
  - /secure-remote-access-using-ssh-keys.html
---

:penguin: [Home Server](http://www.circuidipity.com/home-server/) :: Create cryptographic keys and **disable password logins** to make remote machines more secure.

## Let's go!

**Server** is a [netbook](http://www.circuidipity.com/laptop-home-server.html) running Debian configured for SSH logins from a Linux **client**.

## 0. Install

### On the server

Install `openssh-server` and create an SSH configuration in the home directory of users who requires access to the system ...

```bash                                                                
sudo apt install openssh-server                                           
mkdir ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
```

Collect key fingerprints ...
                                                                                    
```bash
ssh-keygen -lf /etc/ssh/ssh_host_dsa_key.pub >> ~/.ssh/keys.txt               
ssh-keygen -lf /etc/ssh/ssh_host_ecdsa_key.pub >> ~/.ssh/keys.txt             
ssh-keygen -lf /etc/ssh/ssh_host_rsa_key.pub >> ~/.ssh/keys.txt               
```

... and give `keys.txt` to users to compare signature when connecting for the first time.            
                                                                                    
### On the client

Install `openssh-client` and create the SSH folder in `$HOME` ...

```bash                                                                
sudo apt install openssh-client                                             
mkdir ~/.ssh && chmod 700 ~/.ssh                                                
```

Create `~/.ssh/config` to hold **aliases** with the login options for a server. Example ...

```bash                                                                
Host netbook.lan
HostName 192.168.1.88                                                   
Port 22                                                                      
User foo
```

**Test** SSH password login to the server ...

```bash
ssh netbook.lan
    foo@192.168.1.88's password: 
    Last login: Thu Feb 19 18:07:48 2015 from chromebook.lan
```

**Optional:** Use [Dynamic DNS (DDNS)](http://www.circuidipity.com/ddns-openwrt.html) to configure access to a home server from outside the local area network (LAN).

## 1. Keys

### On the client
                                                                                
Generate SSH keys ...
  
```bash
ssh-keygen -t rsa -C "$(whoami)@$(hostname)-$(date -I)" 
```

Upload the **public key** to the server and append to `~/.ssh/authorized_keys` ...
                                                                                
```bash                                                            
cat ~/.ssh/id_rsa.pub | ssh netbook.lan "cat >> ~/.ssh/authorized_keys"        
```

Graphical display managers like `gdm` will automatically check a user account for SSH keys upon login. A pop-up box will prompt for the passphrase and the key will be added to the desktop session.

If logging into a console, tell SSH that you have keys by running `ssh-add` ...

```bash
ssh-add
    Enter passphrase for /home/foo/.ssh/id_rsa:
    Identity added: /home/foo/.ssh/id_rsa (/home/foo/.ssh/id_rsa)
```

All SSH sessions launched from this console will access this user key stored in memory. Make sure to test the connection before disabling password logins ...

```bash
ssh netbook.lan
    Last login: Thu Feb 19 18:22:42 2015 from chromebook.lan
```

No request for passphrase indicates SSH key authentication is properly configured.    

## 2. Disable password logins 

### On the server
                                                                                
Make the following modifications in `/etc/ssh/sshd_config` ...                                         
                                                                                
```bash                                                            
PermitRootLogin no
PubkeyAuthentication yes                                                    
ChallengeResponseAuthentication no                                          
PasswordAuthentication no                                                   
UsePAM no                                                                   
```

Restart SSH ...

```bash
sudo systemctl restart ssh
```

## 3. Key management

[Keychain](http://www.funtoo.org/Keychain) is an OpenSSH key manager. From the package description ...

> When keychain is run, it checks for a running ssh-agent, otherwise it starts one. It saves the ssh-agent environment variables to `~/.keychain/$HOSTNAME-sh`, so that subsequent logins and non-interactive shells such as cron jobs can source the file and make passwordless ssh connections.  In addition, when keychain runs, it verifies that the key files specified on the command-line are known to ssh-agent, otherwise it loads them, prompting you for a password if necessary.

### On the client
                                                                                
Install ...
  
```bash
sudo apt install keychain                                             
```

Configure `~/.bashrc` ...                                                     
                                                                                
```bash                                                            
# setup keychain - ssh-agent management                                     
keychain ~/.ssh/id_rsa                                                      
. ~/.keychain/$HOSTNAME-sh                                                  
```

Flush all cached keys from memory ...
  
```bash
keychain --clear                  
```

**Optional:** If using [tmux](http://www.circuidipity.com/tmux.html) enable persistent SSH key management across sessions by editing `~/.tmux.conf` ... 
                                                                                
```bash
set-option -g update-environment "DISPLAY SSH_ASKPASS SSH_AUTH_SOCK SSH_AGENT_PID SSH_CONNECTION WINDOWID XAUTHORITY"
```

Happy hacking!
