=========================
DJI Android SDK to Python
=========================


.. image:: https://img.shields.io/pypi/v/dji-asdk-to-python.svg
        :target: https://pypi.python.org/pypi/dji-asdk-to-python

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
* Get real time aircraft video streaming using OpenCV and GStreamer
* Precision landing using Aruco markers


Dependencies
------------

OpenCV
~~~~~~~~~
.. code:: bash

    # Remove previous OpenCV
    $ sudo apt-get purge libopencv*
    
    # Create and activate virtual environment
    $ ENV_NAME=dji_asdk_to_python_env
    $ cd $HOME && mkdir -p .virtualenvs && cd .virtualenvs
    $ virtualenv $ENV_NAME --python=python3.8
    $ source $ENV_NAME/bin/activate
    $ pip install numpy==1.20.1

    # Build OpenCV (with activated virtual environment)
    $ cd $HOME
    $ git clone https://github.com/opencv/opencv_contrib.git
    $ cd opencv_contrib && git checkout tags/4.5.1 && cd ..

    $ git clone https://github.com/opencv/opencv.git
    $ cd opencv && git checkout tags/4.5.1 && mkdir build && cd build

    $ cmake -D WITH_CUDA=ON \
            -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
            -D PYTHON_EXECUTABLE=/home/$USER/.virtualenvs/$ENV_NAME/bin/python \
            -D WITH_GSTREAMER=ON \
            -D WITH_LIBV4L=ON \
            -D BUILD_opencv_python2=OFF \
            -D BUILD_opencv_python3=ON \
            -D BUILD_TESTS=OFF \
            -D BUILD_PERF_TESTS=OFF \
            -D BUILD_EXAMPLES=OFF \
            -D CMAKE_BUILD_TYPE=RELEASE \
            -D CMAKE_INSTALL_PREFIX=/usr/local ..
    $ make -j4 # use 4 CPU cores
    $ sudo make install
    $ sudo ldconfig

    # Make sure python path exists
    $ cd ~/.virtualenvs/$ENV_NAME/lib/python3.6/site-packages
    $ ln -s /usr/local/lib/python3.8/site-packages/cv2/python-3.8/cv2.cpython-38-aarch64-linux-gnu.so cv2.so
    
    # Check OpenCV install
    $ python -c "import cv2; print(cv2.getBuildInformation());" | grep GStreamer

-------

Install PyPI
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install dji-asdk-to-python


Install from master
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install git+https://github.com/PSBPOSAS/dji-asdk-to-python.git

Install specific release example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install git+https://github.com/PSBPOSAS/dji-asdk-to-python.git@v0.1.1

Uninstall
---------

.. code:: bash

    $ pip uninstall dji-asdk-to-python

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
