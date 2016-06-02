.. _example4_2:
    
Example 4 (part 2): A more complex stopwatch
============================================

.. note:: This project uses the number display and touch keypad, which come with
          the Mega Treasure Chest.

I said in the last example that we'd make a more complex stopwatch. This is it.
Instead of just pausing when we press **button 2** this one gives us a *lap
time* - that is, it flashes the time when you pressed button 2, but the clock
keeps running in the background and when you press button 2 again the display
shows the stopwatch time again.

This replicates the stopwatch behaviour on classic digital watches from the
eighties. Very important to get right, I'm sure you'll agree.

This project starts storing the state of the timer on our own module, rather
than within the Stopwatch thing itself. It gives us more control, but it makes
our code more complicated...

Step by step example
--------------------

This example can be found in
`blackpearl/examples/example_5_2.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/example_5_2.py>`_,
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
      
      status = 'STOPPED'
      on = True
      display_time = 0.0
      
      def setup(self):
          self.number.set_number(0.0, precision='00')
          self.number.update()
        
      def receive(self, message):
          if 'stopwatch' in message:
              tm = message['stopwatch']['time']
              if self.status == 'RUNNING':
                  self.display_time = tm
                  self.number.set_number(tm, precision='00')
                  self.number.update()
              elif self.status == 'PAUSED':
                  hundredths = int(tm*100)
                  if hundredths % 50 == 0:
                      self.on = not self.on
                      if self.on:
                          self.number.set_number(self.display_time, precision='00')
                          self.number.update()
                      else:
                          self.number.reset()
                      
          elif 'touch' in message:
              buttons = message['touch']['buttons']
              if buttons['1'] and self.status == 'STOPPED':
                  self.status = 'RUNNING'
                  self.stopwatch.start()
              elif buttons['1'] and self.status == 'RUNNING':
                  self.status = 'STOPPED'
                  self.stopwatch.stop()
                  self.stopwatch.reset()
              elif buttons['2'] and self.status == 'RUNNING':
                  self.status = 'PAUSED'
              elif buttons['2'] and self.status == 'PAUSED':
                  self.status = 'RUNNING'
              elif buttons['4'] and self.status in ['PAUSED', 'STOPPED']:
                  self.status = 'STOPPED'
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
  
We also need to define some class attributes to store our state::
  
      status = 'STOPPED'
      on = True
      display_time = 0.0

This time our ``.receive()`` is called with messages from either the ``touch``
or the ``stopwatch``, so we need to have an ``if ... elif ... else`` right at
the start of our ``.recieve()`` to decide what to do.

.. note:: The format of the message that the touch sends is documented on the
          :ref:`Touch's page <touch-hardware>`.

The decisions that we take when we get a tick from the stopwatch are a bit more
complicated this time. If our status is ``"RUNNING"`` we want to do what we did
before - display the time - but we also want to store the time we displayed,
just in case it's about to be paused::

      def receive(self, message):
          if 'stopwatch' in message:
              tm = message['stopwatch']['time']
              if self.status == 'RUNNING':
                  self.display_time = tm
                  self.number.set_number(tm, precision='00')
                  self.number.update()
                  
If, however, our status is ``"PAUSED"`` (because the user has pressed button 2)
then we want to start flashing the display with the time at the moment the user
pressed the button::
  
              elif self.status == 'PAUSED':
                  hundredths = int(tm*100)
                  if hundredths % 50 == 0:
                      self.on = not self.on
                      if self.on:
                          self.number.set_number(self.display_time, precision='00')
                          self.number.update()
                      else:
                          self.number.reset()
  
.. warning:: YOU GOT TO HERE. SUGGEST FOR THE PURPOSES OF EXPLAINING THAT YOU
             ACTUALLY MOVE THE TOUCH STUFF ABOVE THE STOPWATCH, AS THIS MAKES
             MORE SENSE.
             
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
  
  