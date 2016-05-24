.. _motion-hardware:

The Motion Detector
===================

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/motion.py

**Source code** `blackpearl/things/hardware/inputs/motion.py`__

__ source-code_

This module provides a wrapper around the motion detector. The motion detector
measures two things - acceleration and magnetic field.

Acceleration is measured in 3 axes, the third of which - ``z`` - is,
if you hold the sensor level and still, acceleration due to gravity.

Magnetic field is also measured in 3 axes. Again, if you hold the sensor still
and flat then the motion module can calculate a compass heading.

The motion has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure::

  {'motion': {'accelerometer': {'x': 214,
                                'y': -601,
                                'z': 16967,
                                },
              'magnetometer': {'x': 622,
                               'y': -457,
                               'z': -1566,
                               },
              'heading': 126,
              }
   }

So if you set your ``listening_for`` to include ``'motion'`` your ``.receive()``
will get called every time the sensor moves or the magnetic field changes. This
happens a lot, so be prepared for tons of updates!

.. note:: So far I've not been able to work out what units the motion is using.
          Usually we would expect metres per second squared for the
          accelerometer and micro Teslas for the magnetic field, but it doesn't
          seem to be either of those in this case.
          
.. warning:: This module is *very very noisy*. It sends constant updates, 
             however still you keep it. You have been warned :)

