.. _dial-hardware:

The Dial
========

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/dial.py

**Source code** `blackpearl/things/hardware/inputs/dial.py`__

__ source-code_

This module provides a wrapper around the dial input. The dial and slider are
analogous, as both return a value between 0 and 1023 as they are changed.

Due to fuzziness around the extremes **blackpearl** caps the returned values.
Any value returned by the dial less than 5 is sent out in the message as zero,
and any value returned by the dial greater than 1000 is sent out as 1000. That
way your code can be sure when the dial is at its minimum or maximum value.

The dial has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure::

  {'dial': {'value': 934}}
  
So if you set your ``listening_for`` to include ``'dial'`` your ``.receive()``
will get called every time the dial moves.