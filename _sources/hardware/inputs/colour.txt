.. _colour-hardware:

The Colour Sensor
=================

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/colour.py

**Source code** `blackpearl/things/hardware/inputs/colour.py`__

__ source-code_

This module provides a wrapper around the colour input. The colour measures the
light levels in 4 ways - through a red filter, through a green filter, through
a blue filter and with no filter at all.

In the raw data the maximum value of each of the above is 44,032, but that sort
of number will only be returned under very bright conditions. Normal light
levels you should expect a maximum on the clear channel of around 2,000.

The **blackpearl** python module takes this data and also provides a handy
calculated value. By dividing each of the red, green and blue channels by the
value returned by the unfilterd sensor we can calculate a traditional RGB value
that can be used on the web or passed to the rainbow module.

This is done as follows::
  
  rgb = [(red*255)/clear, (green*255)/clear, (blue*255)/clear,]
  
The colour has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure::

  {'colour': {'rgb': [82,72,157,],
              'hex': '#52479d',
              'raw': {'red': 441,
                      'green': 385,
                      'blue': 834,
                      'clear': 1361,
                      }
              }
              
So if you set your ``listening_for`` to include ``'colour'`` your ``.receive()``
will get called every time the colour changes (if you wave the colour sensor
around this will happen *a lot*!)

.. _colour-hardware-examples:

Complete examples
-----------------

The following examples use the colour sensor:

 * :doc:`/examples/example_3`
 
