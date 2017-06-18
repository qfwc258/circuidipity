=================================
Verify a PGP signature with GnuPG
=================================

:date: 2017-06-10 09:00:00
:slug: verify-pgp-signature-gnupg
:tags: gpg, crypto, shell, debian, linux
:modified: 2017-06-18 11:45:00

I setup `GNU Privacy Guard <https://www.gnupg.org/>`_ (**GnuPG** or **GPG**) - a free software implementation of OpenPGP - and use the utility to verify the PGP signatures of files.

Let's go!
=========

Using a **PGP private/public keypair** to create a **digital signature** for a file certifies its integrity. A developer signs a package with their private key and the receiver verifies the signature with the public key. If the package has been modified or corrupted in transmission the verification will fail.

0. Install GnuPG
----------------

.. code-block:: bash

	$ sudo apt install gnupg dirmngr
	$ gpg --version
	gpg (GnuPG) 2.1.18
	libgcrypt 1.7.6-beta
	[...]

First time invoking ``gpg --list-keys`` with an empty **keyring** generates a config directory in $HOME ...

.. code-block:: bash

    $ gpg --list-keys
    gpg: directory '/home/dwa/.gnupg' created
    [...]

Default config files are ``~/.gnupg/gpg.conf`` and ``~/.gnupg/dirmngr.conf``.

1. Keyserver
------------

Many keys are stored on a **keyserver**. I choose the `recommended sks keyserver pool <https://riseup.net/en/security/message-security/openpgp/best-practices#selecting-a-keyserver-and-configuring-your-machine-to-refresh-your-keyring>`_. Download the **sks-keyservers.net CA** and verify the certificate ... [1]_

.. code-block:: bash

    $ wget https://sks-keyservers.net/sks-keyservers.netCA.pem -P ~/.gnupg/
    $ cd ~/.gnupg
    $ openssl verify -trusted sks-keyservers.netCA.pem -check_ss_sig sks-keyservers.netCA.pem
    sks-keyservers.netCA.pem: OK
    $ openssl x509 -in sks-keyservers.netCA.pem -noout -text | grep "X509v3 Subject Key Identifier" -A1 | tail -n1
        E4:C3:2A:09:14:67:D8:4D:52:12:4E:93:3C:13:E8:A0:8D:DA:B6:F3

... and compare with the `key identifier recorded at sks-keyservers.net. <https://sks-keyservers.net/verify_tls.php>`_

Add the keyserver and the CA to ``~/.gnupg/dirmngr.conf`` ...

.. code-block:: bash

    keyserver hkps://hkps.pool.sks-keyservers.net
    hkp-cacert ~/.gnupg/sks-keyservers.netCA.pem

Link: `OpenPGP Best Practices <https://riseup.net/en/security/message-security/openpgp/best-practices>`_

2. Verify a PGP signature
-------------------------

`Verifying authenticity of Debian installer images: <https://www.debian.org/CD/verify>`_ "Cryptographically strong checksum algorithms (SHA256 and SHA512) are available for every release ... To ensure that the checksums files themselves are correct, use GnuPG to verify them against the accompanying signature files."

**Example:** Download the (unofficial with firmware) **minimal network installer** and the signed checksum files ...

.. code-block:: bash

    $ wget https://cdimage.debian.org/mirror/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/iso-cd/firmware-9.0.0-amd64-netinst.iso
    $ wget https://cdimage.debian.org/mirror/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/iso-cd/SHA512SUMS.sign
    $ wget https://cdimage.debian.org/mirror/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/iso-cd/SHA512SUMS

Display the signing key ...

.. code-block:: bash

    $ gpg --verify SHA512SUMS.sign SHA512SUMS
    gpg: Signature made Sun 07 May 2017 02:28:21 PM EDT
    gpg:                using RSA key DA87E80D6294BE9B
    gpg: Can't check signature: No public key

Show details of the key on the keyserver ...

.. code-block:: bash

    $ gpg --search-keys DA87E80D6294BE9B
    gpg: data source: https://gozer.rediris.es:443
    (1) Debian CD signing key <debian-cd@lists.debian.org>
      4096 bit RSA key DA87E80D6294BE9B, created: 2011-01-05
      Keys 1-1 of 1 for "DA87E80D6294BE9B".  Enter number(s), N)ext, or Q)uit > n

Import the key from the keyserver ...

.. code-block:: bash

    $ gpg --recv-keys DA87E80D6294BE9B
    gpg: key DA87E80D6294BE9B: public key "Debian CD signing key <debian-cd@lists.debian.org>" imported
    gpg: no ultimately trusted keys found
    gpg: Total number processed: 1
    gpg:               imported: 1

Display the keyring containing our new key ...

.. code-block:: bash

    $ gpg --list-keys
    /home/dwa/.gnupg/pubring.kbx
    ----------------------------
    pub   rsa4096 2011-01-05 [SC]
        DF9B9C49EAA9298432589D76DA87E80D6294BE9B
        uid           [ unknown] Debian CD signing key <debian-cd@lists.debian.org>
        sub   rsa4096 2011-01-05 [E]

After importing the signing key ...

.. code-block:: bash

    $ gpg --verify SHA512SUMS.sign SHA512SUMS
    gpg: Signature made Sun 07 May 2017 02:28:21 PM EDT
    gpg:                using RSA key DA87E80D6294BE9B
    gpg: Good signature from "Debian CD signing key <debian-cd@lists.debian.org>" [unknown]
    gpg: WARNING: This key is not certified with a trusted signature!
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: DF9B 9C49 EAA9 2984 3258  9D76 DA87 E80D 6294 BE9B

The warning about ``key is not certified with a trusted signature`` means GnuPG verified the key matches the signature but cannot guarantee the key really belongs to the developer. It is up to me to decide how much confidence to place in the authenticity of the key.

For this Debian-provided signature file I compare the ``Primary key fingerprint`` line to the key fingerprints recorded on `the Debian website. <https://www.debian.org/CD/verify>`_ Looks good! [2]_

3. Verify file integrity
------------------------

.. code-block:: bash

    $ sha512sum --ignore-missing --check SHA512SUMS
    firmware-9.0.0-amd64-netinst.iso: OK

Happy hacking!

Notes
`````
.. [1] Verifying `keyserver pool certificate. <https://github.com/riseupnet/riseup_help/issues/145>`_
.. [2] `DO NOT TRUST ANYTHING SHORTER THAN THE FINGERPRINTS. <https://lkml.org/lkml/2016/8/15/445>`_
