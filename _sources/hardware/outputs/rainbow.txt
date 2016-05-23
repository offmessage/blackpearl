.. rainbow-hardware:

The Rainbow
===========

The rainbow has 5 LEDs (numbered 0 to 4). Each one can be
individually set to an RGB value, where each of red, green and blue is between
0 and 255. This module provides a convenience ``.set_all(r, g, b)`` method that
allows you to set all 5 LEDs at once, or you can set each individually using
the ``.set_pixel(posn, r, g, b)`` where ``posn`` is in the range 0 to 4.

The LED numbered 0 is the one closest to the USB port, while 4 is the furthest.

.. note:: Because you can set each LED individually you have to call the
          ``.update()`` method for your changes to take effect. This means that
          you can spend some time crafting your values before sending them all
          off at once rather than have them change one at a time as you build
          stuff up.

Important methods
-----------------

.. function:: .set_all(r, g, b)
   
   This method sets all 5 LEDs to the same rgb value. Remember to call 
   ``.update()`` after you've called this method.
   
.. function:: .set_pixel(position, r, g, b)
   
   This method sets an individual LED at the position specified to the rgb
   value provided. Remember that computers count from zero, so ``position`` must
   be in the range 0 to 4. Once you've set the values of all of the LEDs as you
   require remember to call ``.update()``.
   
.. function:: .update()
   
   Sends the current values to the rainbow.
   
.. function:: .reset()
   
   Turn off all the LEDs.
   
.. function:: Rainbow.hue(value)
   
   ``value`` must be between 0 and 1. Converts the value to an rgb value. (If
   I'm honest I simply copied the maths from the rockpool Javascript library. I
   don't actually know what this does, other than both zero and one are pure
   red, and all the numbers between create a different colour).
   
