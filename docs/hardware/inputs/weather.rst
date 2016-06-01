.. _weather-hardware:

The Weather Sensor
==================

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/weather.py

**Source code** `blackpearl/things/hardware/inputs/weather.py`__

__ source-code_

This module provides a wrapper around the weather sensor. The weather sensor
measures two things - temperature and barometric pressure. Temperature is
returned in Celsius (to two decimal places) and pressure is returned in
hectoPascals/millibars (to two decimal places).

The weather has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure::

  {'weather': {'channel': 2,
               'temperature': 23.45,
               'pressure': 1013.25,
               },
   }

So if you set your ``listening_for`` to include ``'weather'`` your ``.receive()``
will get called every time the temperature or pressure changes. Because of the
sensitivity of both sensors this happens a lot, so be prepared for lots of
updates!

.. warning:: This module is *very very noisy*. It sends constant updates. 
             You have been warned :)

