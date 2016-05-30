.. _rainbow-hardware:

The Rainbow
===========

.. _rainbow-hardware-works:

How it works
------------

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

.. _rainbow-hardware-methods:

Supported methods
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
   red, and all the numbers between create a different colour). This method
   returns an list of the form ``[r, g, b,]``. It *does not* act on the rainbow
   directly (in other words, you need to pass the return value from this method
   to ``.set_all()`` or ``.set_pixel()``).
   
.. _rainbow-hardware-snippets:

Example snippets
----------------

.. note:: Each of these code snippets assumes you have an instance of the
          ``Rainbow`` class called ``rainbow``. In your modules this would be
          achieved by listing ``Rainbow`` in your ``hardware_required`` and then 
          setting ``rainbow = self.rainbow`` in your ``.receive()`` method.

To set all 5 LEDs to red you would use the following code::
  
  rainbow.set_all(255, 0, 0)
  rainbow.update()
  
To set the first LED red, the second green, the third blue, the fourth red and
the fifth green you would use the following code::
  
  rainbow.set_pixel(0, 255, 0, 0)
  rainbow.set_pixel(1, 0, 255, 0)
  rainbow.set_pixel(2, 0, 0, 255)
  rainbow.set_pixel(3, 255, 0, 0)
  rainbow.set_pixel(4, 0, 255, 0)
  rainbow.update()
  
.. _rainbow-hardware-examples:

Complete examples
-----------------

The following examples use the Rainbow:

 * :doc:`/gettingstarted`
 * :doc:`/examples/example_1`
 * :doc:`/examples/example_2`
 * :doc:`/examples/example_3`
