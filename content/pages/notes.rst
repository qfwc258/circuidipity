=====
Notes
=====

:slug: notes

2017-06-10T0838
---------------

Microphone problem on Thinkpad x230 running Ubuntu 16.04 ... No sound input and **mic** not detected.

**[ FIX! ]** Get capture device ...                                                          

.. code-block:: bash

	$ arecord -l                                                                         
	card 0: ... device 0: ...                                                            
                                                                                     
... and edit ``/etc/pulse/default.pa`` with ``load-module module-alsa-source device=hw:0,0``.

Kill and respawn pulseaudio ...

.. code-block:: bash
                                                        
	$ pulseaudio -k

2017-06-09T0941
---------------
Restart network service on Ubuntu ... Sometimes after wake-from-suspend the network connection is down and network-manager's wifi ap list fails to refresh.
                                                                                
**[ FIX! ]** Simple systemd way ...                                                   
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo systemctl restart NetworkManager.service                             
                                                                                
If that doesn't work ... Try using ``nmcli`` to stop and start network-manager directly ...
                                                                                
.. code-block:: bash                                                             
                                                                                
    $ sudo nmcli networking off                                                 
    $ sudo nmcli networking on                                                  
                                                                                
Old-fashioned SysV init script method still works on 16.04 ...                
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo /etc/init.d/networking restart                                       
        ... or ...                                                              
    $ sudo /etc/init.d/network-manager restart                                  
                                                                                
Last resort ...                                             
                                                                                
.. code-block:: bash                                                            
                                                                                
    $ sudo ifdown -a  # -a brings down all interfaces                           
    $ sudo ifup -a

2017-06-08T0920
---------------
Attaching to a wifi network with ``nmcli`` (network-manager cli client) ...

.. code-block:: bash

    $ nmcli radio
    $ nmcli device
    $ nmcli device wifi rescan
    $ nmcli device wifi connect SSID-Name password PASS

2017-06-07T1219
---------------
Disable `Pelican <http://www.circuidipity.com/tag-pelican.html>`_ from auto-generating ``archives.html`` by adding to ``pelicanconf.py`` ...

.. code-block:: bash

    ARCHIVES_SAVE_AS = ''

From `URL Settings <http://docs.getpelican.com/en/latest/settings.html#url-settings>`_: "If you do not want one or more of the default pages to be created ... set the corresponding ``*_SAVE_AS`` setting to '' to prevent the relevant page from being generated."
