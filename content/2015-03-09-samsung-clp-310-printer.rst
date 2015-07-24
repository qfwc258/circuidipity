=======================
Samsung CLP-310 Printer
=======================

:date: 2015-03-09 18:17:00
:slug: samsung-clp-310-printer
:tags: samsung, printer, ubuntu, linux, network

Connect a **Samsung CLP-310** to server running Ubuntu 14.04 LTS and configure as printer for a home network.

Let's go!
=========
                                
0. CUPS
=======

Attach the Samsung device to server:
 
.. code-block:: bash                                                                
                                                                                    
    $ dmesg -t                                                                      
    [...snip...]
    usb 1-2: new high-speed USB device number 6 using ehci-pci                           
    usb 1-2: New USB device found, idVendor=04e8, idProduct=328e                         
    usb 1-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3                    
    usb 1-2: Product: CLP-310 Series                                                     
    usb 1-2: Manufacturer: Samsung Electronics Co., Ltd.                                 
    usb 1-2: SerialNumber: 149CBAGS200219Y                                               
    usblp 1-2:1.0: usblp0: USB Bidirectional printer dev 6 if 0 alt 0 proto 2 vid 0x04E8 pid 0x328E
    usbcore: registered new interface driver usblp

Install CUPS (print server) and the `recommended driver <https://www.openprinting.org/printer/Samsung/Samsung-CLP-310>`_ ``splix`` and grant (example) ``username`` admin privileges:
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ sudo apt-get install cups cups-bsd printer-driver-splix          
    $ sudo adduser username lp                                                      
    $ sudo adduser username lpadmin                                                 
    $ sudo adduser username scanner

1. Printer config
=================
                                                                                
Modify ``/etc/cups/cupsd.conf`` to listen for connections from any device on the home network. Example for home server at ip address ``192.168.1.88``:                                                     
                                                                                
.. code-block:: bash                                                            
                                                                                
    # Only listen for connections from the local machine.                       
    #Listen localhost:631                                                       
    Listen *:631                                                                
                                                                                
    # Show shared printers on the local network.                                
    Browsing On                                                                 
    BrowseLocalProtocols dnssd                                                  
                                                                                
    # Web interface setting...                                                  
    WebInterface Yes                                                            
                                                                                
    # Restrict access to the server...                                          
    <Location />                                                                
      Order allow,deny                                                          
      Allow 192.168.1.*                                                         
    </Location>                                                                 
                                                                                
    # Restrict access to the admin pages...                                     
    <Location /admin>                                                           
      Order allow,deny                                                          
      Allow 192.168.1.*                                                         
    </Location>                                                                 
                                                                                
Restart CUPS:                                                          
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo service cups restart                                                 
                                                                                
Admin functions available at ``http://192.168.1.88:631/admin``.

Happy hacking!
