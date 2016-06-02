.. _motor-hardware:

The Motor
=========

.. _motor-hardware-works:

How it works
------------

The motor is the simplest of the hardware outputs. It takes a single input of
between -63 and +63, and sets the speed of the motor accordingly (with -63
being maximum speed in one direction, and +63 being maximum speed in the other).

.. _motor-hardware-methods:

Supported methods
-----------------

The module supports the following operations:

.. function:: .stop()
   
   Stops the motor.
   
.. function:: .set_speed(speed)
   
   Sets the speed of the motor. ``speed`` must be in the range **-63** to 
   **+63**. ``builtins.ValueError`` is raised if speed is outside that range.
   

.. _motor-hardware-examples:

Complete examples
-----------------

The following examples use the motors:

 * :doc:`/examples/mightymover`
