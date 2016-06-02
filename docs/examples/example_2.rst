.. _example2:
    
Example 2: Matching colours
===========================

.. note:: This project uses the colour sensor and the rainbow, which come with
          the Large Starter kit.

This is a very simple example, but it shows how the colour sensor can be used
to identify the colours it sees, and can be used as the starting point for a
sock sorter (or similar, but that's what I need to get my drawers in order!)

Step by step example
--------------------

This example can be found in
`blackpearl/examples/example_3.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/example_3.py>`_,
but it's also included here in its entirety for reference::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Colour
  from blackpearl.things import Rainbow
  
  
  class ColourMatcher(Module):
      hardware_required = [Colour, Rainbow,]
      listening_for = ['colour']
    
      def receive(self, message):
          colour = message['colour']['rgb']
          self.rainbow.reset()
          r = colour[0]
          g = colour[1]
          b = colour[2]
          self.rainbow.set_all(r, g, b)
          self.rainbow.update()
        
  
  class MyProject(Project):
      required_modules = [ColourMatcher, ]
    
  
  if __name__ == '__main__':
      MyProject()  
  
As with the all of our projects the first thing we need to do is import all the
necessary bits and bobs. For this one they are the basic ``Project``, the basic
``Module`` plus the ``Rainbow`` and ``Colour`` *things*::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Colour
  from blackpearl.things import Rainbow

As before we define our own module, using **blackpearl**'s **Module** class as
our base class::

  class ColourMatcher(Module):
  
Instead of listening for button presses from the touch, this time we're looking
out for changes to the colour values from the colour sensor, so we change the
``listening_for``. And this time we need the ``Colour`` and ``Rainbow`` bits
of hardware for our project to work, so we put them in our ``hardware_required``
list::

      listening_for = ['colour',]
      hardware_required = [Colour, Rainbow,]

As always all of the real work is done in the ``.receive()`` method. This time
we want to do something every time the colour that the sensor can see changes.

This time our ``.receive()`` method is only called when there is a change to the
colour, because we're only listening for messages from the colour sensor
(which we defined in our ``listening_for``).

.. note:: The format of the message that the colour sends is documented on the
          :ref:`Colour's page <colour-hardware>`.

::

      def receive(self, message):
          colour = message['colour']['rgb']
  
This one is really simple. Because the colour sensor returns a list of red, 
green and blue values in the form that the rainbow accepts all we have to do
is pass them back in to the rainbow's ``.set_all()`` method (and remember to
call the ``.update()`` method too)::
  
          self.rainbow.reset()
          r = colour[0]
          g = colour[1]
          b = colour[2]
          self.rainbow.set_all(r, g, b)
          self.rainbow.update()

As before, the rest of the script is the bit that makes the whole thing run::

  class MyProject(Project):
      required_modules = [Thermometer,]
  
  if __name__ == '__main__':
      MyProject()
  
Now our project will run from within our virtual environment as follows::

  cd /home/pi/projects/blackpearl
  source venv/bin/activate
  python blackpearl/examples/example_3.py
  
Making the code neater
----------------------

As with :doc:`Example 2 </examples/example_2>` we can use Python's positional
arguments to neaten this up  even more::
  
      def receive(self, message):
          colour = message['colour']['rgb']
          self.rainbow.reset()
          self.rainbow.set_all(*colour)
          self.rainbow.update()
  