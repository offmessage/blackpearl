.. _joystick-hardware:

The Joystick
============

.. _source-code: https://github.com/offmessage/blackpearl/blob/master/blackpearl/things/hardware/inputs/joystick.py

**Source code** `blackpearl/things/hardware/inputs/joystick.py`__

__ source-code_

This module provides a wrapper around the joystick input. The joystick measures
the position of the stick in 2 axes (x and y), and each ranges from 0 to 1023.
If you hold the joystick with the USB port towards you x runs from 0 (fully left)
to 1023 (fully right) and y runs from 0 (fully down) to 1023 (fully up). In
theory the joystick should centre at ``512,512`` but in reality both x and y
are likely to be anywhere between approximately 460 and 560.

As well as the x and y values there is also the button (which you activate by
pressing down on the joystick's cap until it clicks). This is passed through as
either ``True`` (pressed) or ``False`` (not pressed). Every time it changes
(i.e. the button is either pressed or released) an update is sent through.

The joystick has no special methods of its own - it is a pure input device.

By default it broadcasts the following data structure::

  {'joystick': {'channel': 2, 
                'coordinates': {'x': 512,
                                'y': 512,
                                },
                'button': False,
                },
   }
              
So if you set your ``listening_for`` to include ``'joystick'`` your ``.receive()``
will get called every time the joystick moves or the button is pressed.
