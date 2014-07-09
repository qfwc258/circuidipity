==========================================
Increase RAM available to Raspberry Pi CPU
==========================================

:slug: pi-memory-split
:tags: raspberry pi, raspbian, linux

**Raspberry Pi Model B Rev 2** has 512MB RAM that is partitioned between the CPU and the GPU. If the Pi is working as a headless server or the Pi desktop is being accessed via `VNC <http://www.raspberrypi.org/documentation/remote-access/vnc/>`_ (which doesn't utilize the GPU) the *memory split* between the two processors can be altered to assign more memory to the CPU for running applications. 

.. note::

    The **Pi Camera Module** requires a minimum of 128MB RAM assigned to the GPU.

Default GPU memory on Raspbian is set to 64MB and the minimum recommended to ensure proper operation is 16MB. To modify GPU memory to 16MB either:

1) edit ``/boot/config.txt`` and set ``gpu_mem=16``; or
2) run ``sudo raspi-config`` and select **"8 Advanced Options -> A3 Memory Split"** and modify **64** to **16**

Save the change, reboot the Pi, and enjoy the CPU memory boost!

Source: `RPiconfig <http://elinux.org/RPi_config.txt>`_
