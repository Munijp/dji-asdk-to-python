=========================
DJI Android SDK to Python
=========================


.. image:: https://img.shields.io/travis/PSBPOSAS/dji-asdk-to-python.svg
        :target: https://travis-ci.org/PSBPOSAS/dji-asdk-to-python

.. image:: https://readthedocs.org/projects/dji-asdk-to-python/badge/?version=latest
        :target: https://dji-asdk-to-python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/PSBPOSAS/dji-asdk-to-python/shield.svg
     :target: https://pyup.io/repos/github/PSBPOSAS/dji-asdk-to-python/
     :alt: Updates



Control your DJI drone compatible with DJI Android SDK through Python


* Free software: BSD license
* Documentation: https://dji-asdk-to-python.readthedocs.io.


Features
--------

* Control your aircraft with virtual sticks
* Perform waypoint missions
* Get real time aircraft video streaming using OpenCV
* Precision landing using Aruco markers


Dependencies
------------

Install from master
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install git+https://github.com/PSBPOSAS/dji-asdk-to-python.git


Usage example
-------------

Check examples here https://github.com/PSBPOSAS/dji-asdk-to-python/tree/master/examples

.. code:: python

    import time
    from dji_asdk_to_python.products.aircraft import Aircraft
    drone = Aircraft("android_device_ip")
    fc = drone.getFlightController()
    fc.startTakeoff()
    time.sleep(10)
    fc.startLanding()

Generate Documentation
----------------------

This wil generate a HTML version of your ``docs/`` and open it in a
browser.

.. code:: bash

    $ make docs



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
