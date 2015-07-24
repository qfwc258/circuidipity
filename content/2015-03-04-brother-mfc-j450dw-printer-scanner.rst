=============================================
Brother MFC-J450DW All-In-One Printer/Scanner
=============================================

:date: 2015-03-04 20:40:00
:slug: brother-mfc-j450dw-printer-scanner
:tags: brother, printer, scanner, ubuntu, linux, network

Connect a **Brother MFC-J450DW** to server running Ubuntu 14.04 LTS and configure as printer+scanner for a home network.

Let's go!
=========
                                
0. CUPS + SANE
==============

Attach the Brother device to server:
 
.. code-block:: bash                                                                
                                                                                    
    $ dmesg -t                                                                      
    [...snip...]                                                                    
    usb 5-1: new high-speed USB device number 4 using ehci-pci                      
    usb 5-1: New USB device found, idVendor=04f9, idProduct=02fa                    
    usb 5-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3               
    usb 5-1: Product: MFC-J450DW                                                    
    usb 5-1: Manufacturer: Brother                                                  
    usb 5-1: SerialNumber: BROH4F240529                                             
    usblp 5-1:1.0: usblp0: USB Bidirectional printer dev 4 if 0 alt 0 proto 2 vid 0x04F9 pid 0x02FA
    usbcore: registered new interface driver usblp                                  

Install CUPS (printer) and SANE (scanner) packages and grant (example) ``username`` admin privileges:
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ sudo apt-get install cups cups-bsd sane-utils libsane-extras                  
    $ sudo adduser username lp                                                      
    $ sudo adduser username lpadmin                                                 
    $ sudo adduser username scanner

1. Brother drivers
==================

Download the **Driver Install Tool** from `Brother MFC-J450DW Downloads <http://support.brother.com/g/b/downloadtop.aspx?c=us&lang=en&prod=mfcj450dw_us>`_ and install drivers:

.. code-block:: bash                                                                
                                                                                    
    $ gunzip linux-brprinter-installer-*.gz                                         
    $ sudo su                                                                       
    # bash linux-brprinter-installer-2.0.0-1                                        
    Input model name ->MFC-J450DW                                                   
                                                                                    
    You are going to install following packages.                                    
        mfcj450dwlpr-3.0.0-1.i386.deb                                               
        mfcj450dwcupswrapper-3.0.0-1.i386.deb                                       
        brscan4-0.4.2-1.i386.deb                                                    
        brscan-skey-0.2.4-1.i386.deb                                                
    OK? [y/N] ->y                                                               
    [...snip...]                                                                
    Will you specify the Device URI? [Y/n] ->Y                                  
                                                                                
    0: ipps                                                                     
    1: https                                                                    
    2: http                                                                     
    3: ipp14                                                                    
    4: lpd                                                                      
    5: ipp                                                                      
    6: socket                                                                   
    7: usb://Brother/MFC-J450DW?serial=BROH4F240529                             
    8: smb                                                                      
    9 (I): Specify IP address.                                                  
    10 (A): Auto. (usb://Brother/MFC-J450DW?serial=BROH4F240529)                
                                                                                
    select the number of destination Device URI. ->10

    lpadmin -p MFCJ450DW -v usb://Brother/MFC-J450DW?serial=BROH4F240529 -E     
    Test Print? [y/N] ->y                                                       
                                                                                
                                                                                
    lpadmin -p MFCJ450DW -v usb://Brother/MFC-J450DW?serial=BROH4F240529 -E     
    Test Print? [y/N] ->y                                                       
                                                                                
    wait 5s.                                                                    
    lpr -P MFCJ450DW /usr/share/cups/data/testprint                             
    You are going to install following packages.                                
        brscan4-0.4.2-1.i386.deb                                                
    [...snip...]                                                                
    Do you agree? [Y/n] ->Y                                                     
                                                                                
    You are going to install following packages.                                
        brscan-skey-0.2.4-1.i386.deb                                            
    [...snip...]                                                                
    Do you agree? [Y/n] ->Y                                                     
    [...snip...]                                                                
    Hit Enter/Return key.                                                       
                                                                                
**Problem:** Scanner stuck in low-res mode using Linux scanner clients. **Simple-scan** would not scan above 300dpi and would throw constant error messages. **Xsane** would not scan at all and throw ``out of memory`` errors. Turns out the Brother installer downloaded and installed an outdated, buggy scanner driver - ``brscan4-0.4.2-1.i386.deb`` - when a newer ``brscan4-0.4.3-*.i386.deb`` driver exists.

**Fix:** Remove the buggy driver and manually install the updated package:

.. code-block:: bash                                                            
                                                                                
    $ sudo service saned stop                                                   
    $ sudo dpkg -P brscan4                                                      
    $ sudo dpkg -i brscan4-0.4.3-0.i386.deb                                     
    $ sudo service saned start                                                  
                                                                                
Source: `Problems when scanning via SANE <http://technik.blogs.nde.ag/2013/12/06/brother-dcp-j925dw-problems-when-scanning-via-sane/>`_

2. Printer config
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

3. Scanner config
=================

On the server
-------------
                                                                     
Detect attached device using ``sane-find-scanner`` and ``scanimage`` (I find that if one fails discovery the other usually works):                                                                    
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sane-find-scanner                                                         
    found USB scanner (vendor=0x04f9 [Brother], product=0x02fa [MFC-J450DW]) at libusb:005:00
    $ scanimage -L                                                              
    device `brother4:bus1;dev1' is a Brother MFC-J450DW USB scanner             
                                                                                
Modify ``/etc/default/saned`` to run SANE as server:                                    
                                                                                
.. code-block:: bash                                                            
                                                                                
    RUN=yes                                                                     
                                                                                
Modify ``/etc/sane.d/saned.conf`` to share the scanner over the network:                                 
                                                                                
.. code-block:: bash                                                            
                                                                                
    ## Access list                                                              
    192.168.1.0/24                                                              
                                                                                
Add entry for Brother scanners to ``/lib/udev/rules.d/40-libsane.rules`` at the point in file just before the bit ``# The following rule will disable...``:

.. code-block:: bash                                        
                                                                                
    # Brother scanners                                                          
    ATTRS{idVendor}=="04f9", ENV{libsane_matched}="yes"                         
                                                                                
    # The following rule will disable...                                        
                                                                                
Reboot server (simply restarting the ``udev`` and ``saned`` services fails to work):                   
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo reboot                                                               
                                                                                
Run a test:                                                                         
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ scanimage --format=tiff > test.tiff

On the client
-------------

Modify ``/etc/sane.d/net.conf`` to point your device towards the server ip address:                                                    
                                                                                
.. code-block:: bash                                                            
                                                                                
    connect_timeout = 60                                                        
    ## saned hosts                                                              
    192.168.1.88                                                                
                                                                                
Run a test using ``simple-scan`` included by default in Ubuntu.

Happy hacking!
