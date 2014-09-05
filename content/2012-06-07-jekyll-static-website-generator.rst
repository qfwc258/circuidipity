=====================================
Great fun getting started with Jekyll
=====================================

:tags: network, web, linux, debian
:slugs: jekyll-static-website-generator

I discovered a cool tool named *Jekyll* that I am now using to generate my website. From the `README <https://github.com/mojombo/jekyll#readme>`_ ...

    Jekyll is a simple, blog aware, static site generator. It takes a template directory (representing the raw form of a website), runs it through Textile or Markdown and Liquid converters, and spits out a complete, static website suitable for serving with Apache or your favorite web server.

I find the idea of creating a static website very appealing. Some of the advantages:

* everything is stored as plain text files ... easy to edit, backup and move around
* cheap and easy to host ... I make use of Amazon S3 and its ability to `host static webpages <http://www.circuidipity.com/host-website-on-amazon-s3.html>`_
* easy to maintain and scale ... at the end of the day its straight HTML

.. note::

    Another possible (free for non-commercial use) hosting option is `GitHub <https://github.com/>`_. Jekyll is the default page generator for the site (and was created by GitHub co-founder Tom Preston-Werner).

The traditional disadvantage to using static pages for a blog has been the lack of dynamic elements - hosting feeds, user comments - but JavaScript for things like the Twitter widget to provide real-time updates and out-sourced services like Disqus to provide comments can work around the old limitations.

Jekyll hits a sweet spot for me. At one end is writing hand-crafted HTML and at the other is database-driven solutions like Wordpress serving up a full-load burrito. Each is most excellent in its own way but Jekyll offers the power of static combined with the use of YAML, Liquid templating, more human-friendly Markdown syntax, and the ability to craft simple programming logic to make writing for the web easier to do and maintain over time.

Getting Started
===============

Jekyll is powered by the `Ruby <http://www.ruby-lang.org/en/>`_ programming language. You don't need to know Ruby to get started and if the default configuration of Jekyll does what you want you can merrily go off and write your posts without touching the language. But Jekyll can be extended by `downloading plugins <https://github.com/mojombo/jekyll/wiki/Plugins>`_ or rolling your own. Having an opportunity to play with Jekyll for the last week I believe it will be good entry-point for myself to learn programming in general and Ruby in particular.

Last week I `installed Ruby using RVM <http://www.circuidipity.com/install-ruby-on-debian-wheezy-using-rvm.html>`_ and after your Ruby environment is properly configured its a simple matter to `install Jekyll <https://github.com/mojombo/jekyll/wiki/install>`_. Note that Jekyll is a *rendering* engine. Pre-configuration is left in user hands. The documentation quickly guides you through creating default directories and files and its possible to have something up and running in minutes. 

YAML, Liquid, and Markdown
==========================

*YAML* and *Liquid* templating are new to me. `YAML <http://yaml.org/>`_ "is a human friendly data serialization standard for all programming languages". Its presence in a document header signals Jekyll to go to work on the contents and it holds variables that can be used in templates and Jekyll functions. This post - for example - has the following YAML header ...

.. code-block:: bash

    ---
    layout: post
    title: Great fun getting started with Jekyll
    location: Toronto
    modified: 2012-06-07
    ---

Variables *layout* and *title* are included by default in Jekyll and can be used to set a template for the document and generate a page title (and more).

I also can create my own variables. The entry *location: Toronto* sets a variable that is used in `Liquid <http://liquidmarkup.org/>`_ to add my location to the posting date ...

.. code-block:: bash

    {% raw %}
    {{ page.date | date_to_long_string }} in {{ page.location }}
    {% endraw %}

I then create a layout template named *post.html* and insert this piece of code ...

.. code-block:: bash

    {% raw %}
    ---
    layout: default
    ---

    <div id="post">

            <div id="page-date">
                    {{ page.date | date_to_long_string }} in {{ page.location }}
            </div>

            <div id="page-title">
                    <h1>{{ page.title }}</h1>
            </div>

            {{ content }}
    {% endraw %}

Any modifications I make to this document will ripple across all documents that call on *layout: post*. Cool!

`Markdown <http://daringfireball.net/projects/markdown/syntax>`_ "allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML)". So - for example - web links ...

.. code-block:: html

    <a href="http://daringfireball.net/projects/markdown/syntax">Markdown</a>

... can be written as ...

.. code-block:: html

    [Markdown](http://daringfireball.net/projects/markdown/syntax)

Other examples ...

.. code-block:: html

    <h1>Header 1</h1>
    <h2>Header 2</h2>

    # Header 1
    ## Header 2

    <em>italic</em>
    <strong>emphasis</strong>

    *italic*
    **emphasis**

Markdown syntax co-exists peacefully with HTML tags inside the same document leaving you free to mix and match as you please. I use it to format my regular text files as well. It is a very natural way to write.

Next step
=========

Starting fresh not only with Jekyll but also YAML, Liquid, plus picking up a dash of CSS to style it ... the width and breadth of documentation available can be a bit overwhelming. I found `Jekyll - 7 Tips & Tricks <http://www.kinnetica.com/2011/04/17/jekyll-tips-and-tricks/>`_ to be a good "next step" after Jekyll is up-and-running.
