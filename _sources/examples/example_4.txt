.. _example4:
    
Example 4: Mighty Mover
=======================

.. note:: This project uses the motors and the slider, which come with
          the Mega Treasure Chest.

This is the beginnings of a remote controlled vehicle. You'll need to attach
the motors and wheels to the orange plate that came in the Mega Treasure Chest.
The best way to see instructions for this is in Pimoroni's own
`Update 47 video <https://www.youtube.com/watch?v=kwXr0Sf1s9k>`_, but it's
fairly simple: just pop the wheels onto the motor shafts and use the short
screws to attach the motors to the orange plate in the locations that are marked
out with motor sized rectangles.

Once the motors are attached wire them up to the dock along with a slider, and
put the slider as close to the middle as you can, before firing up this script.

By pushing the slider up (so more lights come on) the vehicle will go forward.
Pushing it down will make it go backwards. The further you push it the faster
the motors go.

This is a simple example that we'll expand on, but it shows not only how to
wire up the motors, but how to access a piece of hardware when there is more
than one of the same type attached.

Step by step example
--------------------

This example can be found in
`blackpearl/examples/example_4.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/example_4.py>`_,
but it's also included here in its entirety for reference::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Motor
  from blackpearl.things import Slider
  
  
  class Mover(Module):
      listening_for = ['slider',]
      hardware_required = [Slider, Motor, Motor,]
    
      def receive(self, message):
          value = message['slider']['value']
          if value == 0:
              v = -63
          elif value == 1000:
              v = 63
          else:
              v = (value - 500)//8
        
          self.motor1.set_speed(v)
          self.motor2.set_speed(v * -1)
  
  
  class MyProject(Project):
      required_modules = [Mover,]
    
  
  if __name__ == '__main__':
      MyProject()  
  
As with the all of our projects the first thing we need to do is import all the
necessary bits and bobs. For this one they are the basic ``Project``, the basic
``Module`` plus the ``Motor`` and ``Slider`` *things*::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Motor
  from blackpearl.things import Slider

As before we define our own module, using **blackpearl**'s **Module** class as
our base class::

  class Mover(Module):
  
We're ``listening_for`` messages from the slider, and we need the slider and
**two** motors for this to work. The important bit here is that we need to
include the ``Motor`` class **twice** in the ``hardware_required`` list,
because we want two of them::

      listening_for = ['slider',]
      hardware_required = [Slider, Motor, Motor,]

Our ``.receive()`` is called with messages from the ``slider``.

.. note:: The format of the message that the slider sends is documented on the
          :ref:`Slider's page <slider-hardware>`.

The slider returns a value in the range 0 to 1000.

::

      def receive(self, message):
          colour = message['slider']['value']
  
We know that if the slider sends a zero we want full speed in reverse (``-63``)
and if it sends 1,000 we want full speed ahead (``+63``)::
  
            if value == 0:
                v = -63
            elif value == 1000:
                v = 63
  
At the moment the value we get from the slider is between 0 and 1,000. We've
dealt with the two extremenes, 0 and 1,000; now we want to convert any other
number to be between -63 and +63, so that it matches the values that motors expect.
To do this we subtract 500 (so it's now between -500 and +500) and then divide
by 8 (so it's between -62.5 and +62.5.

However, we know that the motors only take whole numbers as their speed. We can
convert our number to a whole number in one of two ways - we can pass it through
``int()``, which will strip off the decimal part (``int(62.5) == 62``) or we 
can use Python's ``//`` operator.

Remember how ``%`` gave us the remainder? Well, ``//`` is the other half of
that - it gives us the integer part of **x divided by y**. In other words,
where ``5 % 2`` is 1, because 1 is the remainder of 5 divided by 2, ``5 // 2``
is 2, because that 2 goes into 5 twice. In the example we use ``//`` to get
our new speed between -62 and +62::
  
          else:
              v = (value - 500)//8
  
Now that we've got our speed we want to send that speed to the motors. Because
we have two of them they've been magically named ``motor1`` and ``motor2``. And
because they are on opposite sides of the vehicle we need to set one of them to
the reverse of the other. So we set the speed like so::
  
          self.motor1.set_speed(v)
          self.motor2.set_speed(v * -1)
  
As before, the rest of the script is the bit that makes the whole thing run::

  class MyProject(Project):
      required_modules = [Mover,]
  
  if __name__ == '__main__':
      MyProject()
  
Now our project will run from within our virtual environment as follows::

  cd /home/pi/projects/blackpearl
  source venv/bin/activate
  python blackpearl/examples/example_4.py
  
  