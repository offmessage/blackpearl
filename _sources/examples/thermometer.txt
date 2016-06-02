.. _example-thermometer:
    
Making a thermometer
====================

.. note:: This project uses the weather sensor, which comes with the Medium
          Starter kit.

Step by step example
--------------------

Ever wanted someone to turn the heating up in your house, but been told that
it's already too warm? Wanted a way to prove that it really *is* cold and the
heating really *should* be turned up? Look no further!

This project makes an impossible to ignore glowing thermometer that shows the
current temperature in the room. If the room is cold (below 16 Celcius) only
one LED on the rainbow lights up, and it's **blue**. As the temperature
increases more LEDs light up orange, until the temperature gets over 21
Celcius when all 5 LEDs light up red!

This example can be found in
`blackpearl/examples/thermometer.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/thermometer.py>`_,
but it's also included here in its entirety for reference::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Rainbow
  from blackpearl.things import Weather
  
  
  class Thermometer(Module):
      listening_for = ['weather',]
      hardware_required = [Weather, Rainbow,]
      
      cold = (0, 0, 255)
      warm = (255, 153, 0)
      hot = (255, 0, 0)
      
      def receive(self, message):
          temperature = message['weather']['temperature']
          
          if temperature < 16:
              colour = self.cold
              leds = [0,]
          elif temperature < 17:
              colour = self.warm
              leds = [0,]
          elif temperature < 18:
              colour = self.warm
              leds = [0, 1,]
          elif temperature < 19:
              colour = self.warm
              leds = [0, 1, 2,]
          elif temperature < 20:
              colour = self.warm
              leds = [0, 1, 2, 3,]
          elif temperature < 21:
              colour = self.warm
              leds = [0, 1, 2, 3, 4,]
          else:
              colour = self.hot
              leds = [0, 1, 2, 3, 4,]
          
          self.rainbow.reset()
          r = colour[0]
          g = colour[1]
          b = colour[2]
          for led in leds:
              self.rainbow.set_pixel(led, r, g, b)
          self.rainbow.update()
          
  
  class MyProject(Project):
      modules_required = [Thermometer,]
      
      
  if __name__ == '__main__':
      MyProject()
  
As with the all of our projects the first thing we need to do is import all the
necessary bits and bobs. For this one they are the basic ``Project``, the basic
``Module`` plus the ``Rainbow`` and ``Weather`` *things*::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Rainbow
  from blackpearl.things import Weather

As before we define our own module, using **blackpearl**'s **Module** class as
our base class::

  class Thermometer(Module):
  
Instead of listening for button presses from the touch, this time we're looking
out for changes to the temperature from the weather sensor, so we change the
``listening_for``. And this time we need the ``Weather`` and ``Rainbow`` bits
of hardware for our project to work, so we put them in our ``hardware_required``
list::

      listening_for = ['weather',]
      hardware_required = [Rainbow, Weather,]

As always all of the real work is done in the ``.receive()`` method. This time
we want to do something every time the temperature changes (as the weather
module reports to an accuracy of 0.01 Celcius the temperature will change a
lot!).

Like in our last project we have some constants - this time colours for cold,
warm and hot - which we also define as class attributes::
  
      cold = (0, 0, 255)
      warm = (255, 128, 0)
      hot = (255, 0, 0)
  
This time our ``.receive()`` method is only called when there is a change to the
weather, because we're only listening for messages from the weather sensor
(which we defined in our ``listening_for``). We're only interested in the
temperature, so we pull the temperature out of the message dictionary.

.. note:: The format of the message that the weather sends is documented on the
          :ref:`Weather's page <weather-hardware>`.

::

      def receive(self, message):
          temperature = message['weather']['temperature']
  
And then we want to take some decisions about what to do with the temperature
information that we get. This code uses Python's ``if ... elif ... else``
structure, and says *"if the temperature is less then 16 do this, if it wasn't
less than 16, but is less than 17 do this"*, and so on right up to *if it
wasn't any of those then do this one*.

Each ``if`` clause selects a colour (``cold`` if it's below 16C, ``warm`` if
it's between 16C and 21C and ``hot`` if it's above 21C) and we make a list of
the LEDs that we want turned on (only 1 for the lowest temperature, upto 5 for
the hottest temperatures)::

          if temperature < 16:
              colour = self.cold
              leds = [0,]
          elif temperature < 17:
              colour = self.warm
              leds = [0,]
          elif temperature < 18:
              colour = self.warm
              leds = [0, 1,]
          elif temperature < 19:
              colour = self.warm
              leds = [0, 1, 2,]
          elif temperature < 20:
              colour = self.warm
              leds = [0, 1, 2, 3,]
          elif temperature < 21:
              colour = self.warm
              leds = [0, 1, 2, 3, 4,]
          else:
              colour = self.hot
              leds = [0, 1, 2, 3, 4,]
  
Now we've got both the colour that we want to display (``colour``) and a list
of LEDs that we want to light up (``leds``) we can set the rainbow. First we
reset it so that none stay on by accident that we don't want to, and then we
cycle through the list of LEDs that we want to light up and set each one to
the colour that we want, before sending ``rainbow.update()`` to make our
changes take effect::
  
          self.rainbow.reset()
          r = colour[0]
          g = colour[1]
          b = colour[2]
          for led in leds:
              self.rainbow.set_pixel(led, r, g, b)
          self.rainbow.update()

As before, the rest of the script is the bit that makes the whole thing run::

  class MyProject(Project):
      modules_required = [Thermometer,]
  
  if __name__ == '__main__':
      MyProject()
  
Now our project will run from within our virtual environment as follows::

  cd /home/pi/projects/blackpearl
  source venv/bin/activate
  python blackpearl/examples/thermometer.py
  
Making the code neater
----------------------

Only a small one this time...

Python supports the idea that if a function takes multiple *positional*
arguments (like the Rainbow's ``.set_pixel(posn, r, g, b)`` does it's possible
to create a list of those arguments and pass them in as a single list, prefixed
with an asterisk.

So instead of::
  
          self.rainbow.reset()
          r = colour[0]
          g = colour[1]
          b = colour[2]
          for led in leds:
              self.rainbow.set_pixel(led, r, g, b)
          self.rainbow.update()
  
It's possible to write::
  
          self.rainbow.reset()
          for led in leds:
              self.rainbow.set_pixel(led, *colour)
          self.rainbow.update()
  
(Really don't worry about it if this makes no sense, but if you're interested
have a Google for *Python positional and keyword arguments* to start exploring
this topic)
