.. touch-hardware:

The Touch
=========

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/touch.py

**Source code** `blackpearl/things/hardware/inputs/touch.py`__

__ source-code_

This module provides a wrapper around the touch keypad. The touch has 4 numbered
buttons (numbered from 1 to 4 on the device itself). Every time a button is
pressed or released an update is sent out - each button is ``True`` when pressed
and ``False`` when not. The touch is capable of tracking each button
individually, so each button value will change independently.

The touch has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure (in this example both
buttons 1 and 3 are currently pressed)::

  {'touch': {'buttons': {'1': True,
                         '2': False,
                         '3': True,
                         '4': False,
                         }
             }
   }

So if you set your ``listening_for`` to include ``'touch'`` your ``.receive()``
will get called every time someone presses or releases a button.
