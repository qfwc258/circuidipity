====================
Locale configuration
====================

:date: 2014-03-17 01:23:00
:slug: locale-config
:tags: shell, debian, linux

**Locales** are used to define language settings in Linux.                      
                                                                                
Default locale                                                                      
++++++++++++++                                                                      
                                                                                    
Current setting for the default locale is stored in ``/etc/default/locale``.    
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ locale                                                                        
    LANG=                                                                           
    LANGUAGE=                                                                       
    LC_CTYPE="POSIX"                                                                
    LC_NUMERIC="POSIX"                                                              
    LC_TIME="POSIX"                                                                 
    LC_COLLATE="POSIX"                                                              
    LC_MONETARY="POSIX"                                                             
    LC_MESSAGES="POSIX"                                                             
    LC_PAPER="POSIX"                                                                
    LC_NAME="POSIX"                                                                 
    LC_ADDRESS="POSIX"                                                              
    LC_TELEPHONE="POSIX"                                                            
    LC_MEASUREMENT="POSIX"                                                          
    LC_IDENTIFICATION="POSIX"                                                       
    LC_ALL=                                                                         
                                                                                    
Locales available                                                                   
+++++++++++++++++                                                                   
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ locale -a                                                                     
    C                                                                               
    C.UTF-8                                                                         
    POSIX                                                                           
                                                                                    
Generate locales                                                                    
++++++++++++++++                                                                    
                                                                                    
A list of locales to be built is stored in ``/etc/locale.gen``. Edit this file by [un]commenting the entries to [enable]disable locales and run ``sudo update-gen``, or select which locales to build from an interactive menu by running ...
                                                                                    
.. code-block:: bash                                                                
                                                                                    
    $ sudo dpkg-reconfigure locales                                                 
                                                                                    
Set default locale                                                                          
++++++++++++++++++

.. code-block:: bash                                                                
                                                                                    
    $ sudo update-locale LANG=en_CA.UTF-8 LANGUAGE=en_CA:en                         
                                                                                    
... and reboot.                                                                     
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ locale                                                                    
    LANG=en_CA.UTF-8                                                            
    LANGUAGE=en_CA:en                                                           
    LC_CTYPE="en_CA.UTF-8"                                                      
    LC_NUMERIC="en_CA.UTF-8"                                                    
    LC_TIME="en_CA.UTF-8"                                                       
    LC_COLLATE="en_CA.UTF-8"                                                    
    LC_MONETARY="en_CA.UTF-8"                                                   
    LC_MESSAGES="en_CA.UTF-8"                                                   
    LC_PAPER="en_CA.UTF-8"                                                      
    LC_NAME="en_CA.UTF-8"                                                       
    LC_ADDRESS="en_CA.UTF-8"                                                    
    LC_TELEPHONE="en_CA.UTF-8"                                                  
    LC_MEASUREMENT="en_CA.UTF-8"                                                
    LC_IDENTIFICATION="en_CA.UTF-8"                                             
    LC_ALL=                                           
