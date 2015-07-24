===============================================================
Tie a balloon on your website and head for the clouds of Amazon
===============================================================

:date: 2011-11-26 01:23:00
:tags: blog, network, linux
:slug: host-website-on-amazon-s3

Last week I packed up the handwritten html pages, images, and bits hosted on my home netbook server and moved up into the *cloud*.

`Amazon Simple Storage Service <http://aws.amazon.com/s3/>`_ (S3) added the capability of `hosting a static website <http://www.allthingsdistributed.com/2011/02/website_amazon_s3.html>`_ (a website built on files as opposed to a database) and made it very cheap to get started and very easy to scale up bandwidth and storage as required. 

This is how I did it in 5 steps ...

Step 0 — Sign up for Amazon Web Services (AWS) Free Usage Tier
==============================================================

AWS has created a `free 12-month introductory offer <http://aws.amazon.com/free/>`_ to try out their various services. Amazon S3 includes 5 GB storage, 20,000 Get Requests and 2,000 Put Requests for hosting your website. You `pay for anything <http://aws.amazon.com/s3/#pricing>`_ that exceeds those limits.

Step 1 — Create an Amazon S3 website-enabled bucket
===================================================

S3 uses *buckets* (think folders) that act as containers for your static files. `Create a new website-enabled bucket <http://docs.amazonwebservices.com/AmazonS3/latest/dev/index.html?HostingWebsiteOnS3Setup.html>`_ to hold your website files.


Make sure when creating the S3 bucket to give it the name *www.YOURWEBSITE.TLD*. For example, this website uses an S3 bucket with the name ``www.circuidipity.com``.

The endpoint address for your newly-created S3 bucket will be http://www.YOURWEBSITE.TLD.s3-website-location.amazonaws.com (my endpoint is http://www.circuidipity.com.s3-website-us-east-1.amazonaws.com).
    
Step 2 - Set public permissions on S3 bucket
============================================

At this stage your website-enabled bucket and contents are only viewable over the web by their owner ... you. 

Add a *bucket policy* to make your files `publicly available <http://docs.amazonwebservices.com/AmazonS3/latest/dev/index.html?HostingWebsiteOnS3Setup.html>`_. In the AWS Management Console, right-click on your website bucket and select ``Properties->Permissions->Edit bucket policy`` and create a new policy ...

.. code-block:: bash

    {
	    "Version": "2008-10-17",
	    "Statement": [
		    {
			    "Sid": "PublicReadForGetBucketObjects",
			    "Effect": "Allow",
			    "Principal": {
				    "AWS": "*"
			    },
			    "Action": "s3:GetObject",
			    "Resource": "arn:aws:s3:::<strong>your_website_bucket_name</strong>/*"
		    }
	    ]
    }

Now any files placed in your bucket will be world-readable.

Step 3 — Upload website files
=============================

Start your website by creating 2 files ...  ``index.html`` and a custom 404 error document ``doesnotexist.html``. Use the AWS Management Console to upload the files into your S3 bucket and test by browsing to http://YOURBUCKET.s3-location.amazonaws.com/ .

For uploading multiple files in one great swoop I ran across `s3cmd <http://s3tools.org/s3cmd>`_ ... a cool Linux command line utility for managing S3 storage. A package is available for Debian ``sudo apt-get install s3cmd``.

Before configuring ``s3cmd`` to grant access to your website's S3 bucket you require your ``Access Key ID`` and ``Secret Access Key``. Navigate to https://aws-portal.amazon.com and the ``-> Security Credentials -> Access Keys`` tab and make note of your Amazon S3 keys.

Now run ...

.. code-block:: bash

    $ s3cmd --configure    # configuration saved to '/home/<em>user</em>/.s3cfg'

``s3cmd`` has lots of options ... but especially cool is the `sync <http://s3tools.org/s3cmd-sync>`_ command. Its similar to ``rsync`` and uses ``md5`` checksum and filesize to compare files between localhost and your remote S3 bucket and only transfer files that have changed.

For my own website I run ...

.. code-block:: bash

    $ s3cmd sync --dry-run output/ s3://www.circuidipity.com/   # first I test it out ... nothing is transferred
    $ s3cmd sync output/ s3://www.circuidipity.com/

Step 4 - Configure DNS
======================

To transform *s3-website-location.amazonaws.com* into *www.YOURWEBSITE.com* you need to `create a CNAME at your DNS provider <http://docs.amazonwebservices.com/AmazonS3/latest/dev/index.html?VirtualHosting.html>`_ that maps ``www`` to your S3 bucket ... in my case DNS is provided by GoDaddy and I map ``www`` to www.circuidipity.com.s3-website-us-east-1.amazonaws.com.

*s3-website-us-east-1.amazonaws.com* is for accessing the website feature. If you just want S3 you can use *s3.amazonaws.com*.

Allow a bit of time for your changes to propagate through the global network of DNS servers ... check your modifications by running ``host`` (cool little DNS hookup utility) ...

.. code-block:: bash

    $ host www.circuidipity.com
    www.circuidipity.com is an alias for www.circuidipity.com.s3-website-us-east-1.amazonaws.com.
    www.circuidipity.com.s3-website-us-east-1.amazonaws.com is an alias for s3-website-us-east-1.amazonaws.com.
    s3-website-us-east-1.amazonaws.com has address 207.171.163.149

So ``CNAME www`` is working ... *dy-naaa-MITE!* But a ``CNAME`` cannot point to a *naked domain* (circuidipity.com).

There are a few different ways to do a *naked domain redirect*. I chose to use a free service provided by `wwwizer.com <http://wwwizer.com/>`_ ... simply point your ``A record`` (on GoDaddy and other registrars sometimes represented by the ``@`` symbol) to *174.129.25.170* and it will be redirected to the `same domain with www placed in front <http://wwwizer.com/naked-domain-redirect>`_.
