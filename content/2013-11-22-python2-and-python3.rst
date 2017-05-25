===========================================================
Python2 and Python3 co-existing in harmony using Virtualenv
===========================================================

:tags: python, programming, debian, linux
:slug: python2-and-python3
:modified: 2014-02-03 01:23:00

On my laptop Python is pre-installed:

.. code-block:: bash

    $ python -V
    Python 2.7.5+

`Hacking Secret Ciphers with Python <http://inventwithpython.com/hacking/index.html>`_ looks to be a good resource for beginners to get started with Python programming. This free book uses Python3 but Debian defaults to Python2. No problem. Multiple versions of Python can co-exist on the same computer thanks to *virtual isolated python environments* created using `Virtualenv <https://pypi.python.org/pypi/virtualenv>`_. That allows me to use Python3 for certain projects - like the exercises in *Ciphers* - but continue using Python2 as the system default.

Install the Debian package for ``virtualenv`` and create a directory to hold multiple virtual environments:

.. code-block:: bash

    $ sudo apt-get install python-virtualenv
    $ mkdir $HOME/virtualenvs
    $ cd $HOME/virtualenvs

Now we can create and activate a new sandboxed Python3 environment:

.. code-block:: bash

        $ virtualenv --python=/usr/bin/python3 --no-site-packages secret_ciphers       
        Running virtualenv with interpreter /usr/bin/python3                           
        Using base prefix '/usr'                                                       
        New python executable in secret_ciphers/bin/python3                            
        Also creating executable in secret_ciphers/bin/python                          
        Installing Setuptools........done.                                             
        Installing Pip...............done.                                             
                                                                               
                                                                               
Enter the newly-created sandbox with ``activate`` and install additional Python package using ``pip``:

.. code-block:: bash                                                                    
                                                                               
        [~]$ source secret_ciphers/bin/activate                                        
        (secret_ciphers)[~]$ python -V                                                    
        Python 3.3.3                                                                   
        (secret_ciphers)[~]$ pip install PACKAGENAME                                                

Run ``deactivate`` to exit the sandbox and return to the default system Python. Delete an inactive sandbox with a simple ``rm -rf SANDBOX``. 
