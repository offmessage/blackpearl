.. _light-hardware:

The Light Sensor
================

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/light.py

**Source code** `blackpearl/things/hardware/inputs/light.py`__

__ source-code_

This module provides a wrapper around the light input. The light sensor measures
two things - unfiltered visible spectrum light and infrared - and uses the two
to calculate a *lux* value. It's the *lux* value that's most interesting for
most projects, as it most closely reflects the light level around the sensor.

The maximum value you'll see from the lux value is 65535, but only if you shine
a super bright LED directly at it. In normal operation expect to peak at about
1,000.

The light has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure::

  {'light': {'channel': 2,
             'visible': 136,
             'infrared': 421,
             'lux': 723,
             },
   }

So if you set your ``listening_for`` to include ``'light'`` your ``.receive()``
will get called every time the light level changes. This will happen a lot, so
be prepared for quite a lot of updates!
