.. _slider-hardware:

The Slider
==========

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/slider.py

**Source code** `blackpearl/things/hardware/inputs/slider.py`__

__ source-code_

This module provides a wrapper around the slider input. The slider and dial are
analogous, as both return a value between 0 and 1023 as they are changed.

Due to fuzziness around the extremes **blackpearl** caps the returned values.
Any value returned by the slider less than 5 is sent out in the message as zero,
and any value returned by the slider greater than 1000 is sent out as 1000. That
way your code can be sure when the slider is at its minimum or maximum value.

The slider has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure::

  {'slider': {'channel': 2,
              'value': 934,
              },
   }
  
So if you set your ``listening_for`` to include ``'slider'`` your ``.receive()``
will get called every time the slider moves.

.. _slider-hardware-examples:

Complete examples
-----------------

The following examples use the slider:

 * :doc:`/examples/mightymover`
