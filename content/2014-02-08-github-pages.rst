===========================
Host a blog on GitHub Pages
===========================

:date: 2014-02-08 01:23:00
:slug: github-pages
:tags: pelican, blog, python, git, debian, linux
:modified: 2016-12-30 14:11:00

`GitHub Pages <http://pages.github.com/>`_ is a free web hosting service for projects composed of static files (i.e no database). Combine a **Pages repository** with **git** version control and a **static site generator** like `Pelican <http://www.circuidipity.com/pelican.html>`_ and you have one awesome toolset to build a website.

This is how I configured GitHub Pages to host `Circuidipity <http://www.circuidipity.com>`_.

Let's go!
=========

0. Install git
--------------

**Debian:** Install ``git`` package and write global configuration variables for ``USERNAME`` in ``~/.gitconfig`` ...

.. code-block:: bash

    $ sudo apt install git git-doc                                          
    $ git config --global user.name "USERNAME"                                  
    $ git config --global user.email USERNAME.EMAIL@example.com                        
    $ git config --global core.editor EDITOR  # I use 'vim'                                     
    $ git config --global merge.tool vimdiff                                    

1. Create git repository
------------------------

Inside my ``pelican``-powered blog project I create 2 new files: ``.gitignore`` and ``README.rst``.

The ``.gitignore`` file does exactly what the name implies ... it instructs ``git`` which files and directories not to bother tracking in version control. For example I do not want to track ...

.. code-block:: bash

    *.pid
    *.pyc
    output/

**For GitHub:** Create a ``README.rst`` and GitHub will auto-detect and configure it as the project homepage when blog contents are uploaded to the remote repository. 

Now I create my local repository, add the items I want to track, and execute my first commit ...

.. code-block:: bash

    $ git init                                                                      
    $ git add README.rst                                                            
    $ git add .gitignore
    $ git add Makefile
    $ git add content/
    $ git add pelicanconf.py
    $ git add publishconf.py
    $ git status                                                                    
    $ git commit -a -m "first commit"  # '-a' adds all files that are being tracked and commits them 
    $ git log  # to view commit history 

2. Create GitHub repository
---------------------------

`Sign up <https://help.github.com/articles/signing-up-for-a-new-github-account>`_ for a free account on GitHub and `create a new empty repository <https://help.github.com/articles/creating-a-new-repository>`_ to hold the blog contents.

Next I connect my local ``.git`` repository to my GitHub remote repository ...
                                            
.. code-block:: bash

    $ git remote add origin https://github.com/vonbrownie/circuidipity.git
    $ git remote -v  # confirm local knows about remote 
    $ git push -u origin master

3. Configure Pelican to use GitHub Pages
----------------------------------------

GitHub offers 2 types of `Pages <https://help.github.com/articles/user-organization-and-project-pages>`_ ... **User Pages** and **Project Pages**. Each GitHub account can host a single User Page and an unlimited amount of Project Pages. Basically they are identical to the end-user and differ only in their configuration.

I chose to make my blog a Project Page and the contents are hosted in the ``gh-pages`` branch of my GitHub project repository. Pelican makes it easy to create and configure ``gh-pages`` using the `ghp-import <https://github.com/davisp/ghp-import>`_ Python script ... which I install via ``pip`` ...

.. code-block:: bash

    $ pip install ghp-import

Finally I publish my blog by pushing the files up to GitHub ...

.. code-block:: bash

    $ make github

GitHub Pages is now hosting the site at ``http://USERNAME.github.io/REPOSITORY``.

4. Custom domain name
---------------------

Awesome! But I want to use my own custom domain name ... not ``REPOSITORY``.

GitHub enables `custom domains <https://help.github.com/articles/setting-up-a-custom-domain-with-pages>`_ by allowing users to create a ``CNAME`` file with their domain address that resides in the root directory of ``gh-pages``. Inside my Pelican project folder I create a new ``extra`` directory containing a single-line ``CNAME`` file with my domain address ``www.circuidipity.com``.

Next I edit ``pelicanconf.py`` to recognize ``CNAME`` and place the file in ``gh-pages`` when I upload my files ...

.. code-block:: py

    # Static paths will be copied without parsing their contents                    
    STATIC_PATHS = ['images', 'extra']                                              
                                                                                
    # Shift the installed location of a file                                        
    EXTRA_PATH_METADATA = {                                                         
        'extra/CNAME': {'path': 'CNAME'},                                       
    }

Upload my changes to GitHub ...

.. code-block:: bash

    $ make github

4.1 Domain Registrar
--------------------

Now the **domain name registrar** needs to be configured to point to the new GitHub address. `Gandi <https://www.gandi.net/>`_ is my registrar and while the details will vary between domain services the steps are basically the same to redirect a custom domain. 

My objective is for the GitHub Pages repository to resolve to ``www.circuidipity.com`` and for ``circuidipity.com`` to redirect to the ``www`` address.

Using Gandi as an example I will create new ``CNAME`` and ``A`` records:

* click on domain name to access admin page and near the bottom select option ``Edit the zone``
* create new ``zone file`` for editing by selecting ``Create a new version``
* modify/add ``CNAME`` ``www`` record with value ``USERNAME.github.io.``
* modify/add ``A`` record to `permanently redirect <https://wiki.gandi.net/en/domains/management/domain-as-website/forwarding>`_ the top level domain to ``www`` using the Gandi redirect service address ``217.70.184.38``
* click ``Use this version`` to save all changes and wait a few hours for the DNS modifications to propagate around the world

It is possible to skip web redirection and set the A record value to point directly to a `GitHub address <https://help.github.com/articles/setting-up-a-custom-domain-with-pages>`_ but at the loss of dynamic traffic management.

5. Custom 404
-------------

Configuring a custom domain allows the option of using a `custom 404 page <https://help.github.com/articles/custom-404-pages>`_. Simply create a ``404.html`` file in the ``gh-pages`` root.

Happy hacking!
