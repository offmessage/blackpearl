.. _example4:
    
Example 4: The Simple Stopwatch
===============================

.. note:: This project uses the number display and touch keypad, which come with
          the Mega Treasure Chest.

This is the first pass at a stopwatch. We'll make more sophisticated ones later
but this one will do the trick for now. It records time to the nearest 1/100th
of a second, and displays it on the number display. Pressing button 1 on the
touch keypad starts and stops the timer. Button 2 pauses (and restarts) it. And
button 4 resets it.

Perfect for timing how long it takes your little brother to get to the bottom
of the garden (and how long he can stay there!)

This is the first of our examples to use some of **blackpearl**'s software
components - in this case, the ``Stopwatch`` *thing*. It's also the first
example that listens for more than one message.

Step by step example
--------------------

This example can be found in
`blackpearl/examples/example_5.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/example_5.py>`_,
but it's also included here in its entirety for reference::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Number
  from blackpearl.things import Stopwatch
  from blackpearl.things import Touch
  
  
  class MyStopwatch(Module):
      
      hardware_required = [Number, Touch,]
      software_required = [Stopwatch,]
      listening_for = ['stopwatch', 'touch',]
      
      def setup(self):
          self.number.set_number(0.0, precision='00')
          self.number.update()
        
      def receive(self, message):
          if 'stopwatch' in message:
              tm = message['stopwatch']['time']
              self.number.set_number(tm, precision='00')
              self.number.update()
        
          elif 'touch' in message:
              buttons = message['touch']['buttons']
              if buttons['1'] and self.stopwatch.status == 'STOPPED':
                  self.stopwatch.start()
              elif buttons['1'] and self.stopwatch.status == 'RUNNING':
                  self.stopwatch.stop()
                  self.stopwatch.reset()
              elif buttons['2'] and self.stopwatch.status in ['PAUSED', 'RUNNING']:
                  self.stopwatch.pause()
              elif buttons['4'] and self.stopwatch.status in ['PAUSED', 'STOPPED']:
                  self.stopwatch.reset()
                  self.number.set_number(0.0, precision='00')
                  self.number.update()
        
        
  class MyProject(Project):
      required_modules = [MyStopwatch, ]
    

  if __name__ == '__main__':
      MyProject()  
  
As with the all of our projects the first thing we need to do is import all the
necessary bits and bobs. For this one they are the basic ``Project``, the basic
``Module`` plus the ``Number``, the ``Touch`` and the ``Stopwatch`` *things*::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Number
  from blackpearl.things import Stopwatch
  from blackpearl.things import Touch

As before we define our own module, using **blackpearl**'s **Module** class as
our base class::

  class MyStopwatch(Module):
      
First we want to make sure that the number displays ``0.00`` before it starts::
  
      def setup(self):
          self.number.set_number(0.0, precision='00')
          self.number.update()
  
We're ``listening_for`` messages from the stopwatch *and* the touch this time,
and we need the number and touch for this to work. For the first time we also
need to define a ``software_required``, as we're using the stopwatch as well::

      hardware_required = [Number, Touch,]
      software_required = [Stopwatch,]
      listening_for = ['stopwatch', 'touch',]

This time our ``.receive()`` is called with messages from either the ``touch``
or the ``stopwatch``, so we need to have an ``if ... elif ... else`` right at
the start our our ``.recieve()``.

.. note:: The format of the message that the touch sends is documented on the
          :ref:`Touch's page <touch-hardware>`.

If the message is from the stopwatch (which it will be once every 1/100th of a
second!) we want to send the new time to the number display. We use the number's
``.set_number()`` method to set the time, and we use ``precision='00'`` to force
it to always use 2 decimal places (so that the decimal point doesn't jump
around when we go from ``1.89`` to ``1.9`` and so on). Finally we issue 
``.update()`` so that the number displays our new value::

      def receive(self, message):
          if 'stopwatch' in message:
              tm = message['stopwatch']['time']
              self.number.set_number(tm, precision='00')
              self.number.update()
  
If, however, the message was from the touch we want to take some very different
actions. If it was **button 1** that was pressed, we want to either start or 
stop the timer::
  
          elif 'touch' in message:
              buttons = message['touch']['buttons']
              if buttons['1'] and self.stopwatch.status == 'STOPPED':
                  self.stopwatch.start()
              elif buttons['1'] and self.stopwatch.status == 'RUNNING':
                  self.stopwatch.stop()
                  self.stopwatch.reset()
  
If it was **button 2** we want to either pause or unpause the timer::
  
              elif buttons['2'] and self.stopwatch.status in ['PAUSED', 'RUNNING']:
                  self.stopwatch.pause()
  
And if it was **button 4** we want to reset the timer and show ``0.00`` on the
number display::
  
              elif buttons['4'] and self.stopwatch.status in ['PAUSED', 'STOPPED']:
                  self.stopwatch.reset()
                  self.number.set_number(0.0, precision='00')
                  self.number.update()
  
As before, the rest of the script is the bit that makes the whole thing run::

  class MyProject(Project):
      required_modules = [MyStopwatch,]
  
  if __name__ == '__main__':
      MyProject()
  
Now our project will run from within our virtual environment as follows::

  cd /home/pi/projects/blackpearl
  source venv/bin/activate
  python blackpearl/examples/example_5.py
  
  