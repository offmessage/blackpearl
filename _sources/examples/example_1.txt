.. _example1:
    
Example 1: Simple interactive light show
========================================

.. note:: Like the getting started example, this project uses the touch keypad
          and rainbow LEDs, so it'll work with the Mini Starter Kit.

Step by step example
--------------------

Our first example project (in :doc:`/gettingstarted`) made the rainbow LEDs
change colour depending on the button that was pressed (red for button 1, green
for button 2, blue for button 3 and nothing for button 4).

This time we want only one LED to light up at a time, and have that change 
every time someone presses button 1. And we want to change the colour every time
someone presses button 2.

This example can be found in
`blackpearl/examples/example_1.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/example_1.py>`_,
but it's also included here in its entirety for reference::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Rainbow
  from blackpearl.things import Touch
  
  
  class TouchTheRainbow(Module):
      listening_for = ['touch',]
      hardware_required = [Touch, Rainbow,]
    
      button1_press_count = 0
      button2_press_count = 0
      colours = [(255,51,204),
                 (255,102,51),
                 (204,255,51),
                 (204,51,255),
                 (102,51,255),
                 (102,255,51),
                 (51,102,255),
                 (255,204,51),
                 (51,255,102),
                 ]
    
      def receive(self, message):
          buttons = message['touch']['buttons']
          if button['1'] is True:
              self.button1_press_count = self.button1_press_count + 1
              
              colour_index = self.button1_press_count % 9
              r, g, b = self.colours[colour_index]
              
              active_pixel = self.button2_press_count % 5
              
              self.rainbow.reset()
              self.rainbow.set_pixel(active_pixel, r, g, b)
              self.rainbow.update()
              
          if button['2'] is True:
              self.button2_press_count = self.button2_press_count + 1
              
              colour_index = self.button1_press_count % 9
              r, g, b = self.colours[colour_index]
              
              active_pixel = self.button2_press_count % 5
              
              self.rainbow.reset()
              self.rainbow.set_pixel(active_pixel, r, g, b)
              self.rainbow.update()
  
  
  class MyProject(Project):
      required_modules = [TouchTheRainbow,]
      
      
  if __name__ == '__main__':
      MyProject()
  
This project remembers the state of the rainbow each time a button is pressed
and changes it the next time a button is pressed. This ability to remembering
is because we've used Python classes to wrap the functionality of the hardware,
and can store the state of the hardware in those classes.

As with the :ref:`Getting Started example <gettingstarted-example>` the first
thing we need to do is import all the necessary bits and bobs. These are the
basic ``Project``, the basic ``Module`` and the ``Rainbow`` and ``Touch``
*things*::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Rainbow
  from blackpearl.things import Touch

As before we define our own module, using **blackpearl**'s **Module** class as
our base class::

  class TouchTheRainbow(Module):
  
And as before we are listening for button presses from the touch keypad, and
need both the touch keypad and the rainbow LEDs for our module to work::

      listening_for = ['touch',]
      hardware_required = [Rainbow, Touch,]

We also define some new things that are unique to this module; we want to keep
count of how many times button 1 and button 2 have been pressed. To do this
we define new *attributes* of our module class::
  
      button1_press_count = 0
      button2_press_count = 0
  
We also want a list of colours to cycle through, so we define that as an
attribute too::
  
      colours = [(255,51,204),
                 (255,102,51),
                 (204,255,51),
                 (204,51,255),
                 (102,51,255),
                 (102,255,51),
                 (51,102,255),
                 (255,204,51),
                 (51,255,102),
                 ]
  
The main difference with this module is our ``.receive()`` method, as we want
to do something different when a button is pressed. 

Remember, our ``.receive()`` method is only called when a button has been
pressed or released, because we're only listening for messages from the touch
(which we defined in our ``listening_for``).

::

      def receive(self, message):
          # We're listening for buttons!
          buttons = message['touch']['buttons']
  
The first thing we do is take some actions when button 1 is pressed. In this
case we want to add 1 to our counter that tells us how many times it's been
pressed::

          if buttons['1'] is True:
              self.button1_press_count = self.button1_press_count + 1
  
The next line works out which member of the colour list to use. We do this
using the ``%`` operator. This is the **remainder** operator. So ``5%2`` is
``1`` (because 5/2 is 2 *remainder* 1). By using this operator we ensure that
however big our button counts get we'll always end up with a number that is
between 0 and 8 which we can use to get a colour from our list (which, because
computers start from 0, is number 0 to 8 too).

::
  
              colour_index = self.button1_press_count % 9
  
Next we get the red green and blue colour values from our selected colour.
In Python it's possible to access the *nth* item in a list (remembering that
computers start counting at zero) by saying ``list[n]``. So to get the word
"two" from the list ``mylist = ['zero', 'one', 'two', 'three',]`` we can say
``mylist[2]``.

::

              r, g, b = self.colours[colour_index]
              
Using the same process (the ``%`` operator) we can calculate which LED to light
up. We know there are 5 LEDs on the rainbow, so we get the remainder by
dividing by 5, which will give us a number between 0 and 4.

::

              active_pixel = self.button2_press_count % 5
  
Now we have all the values that we need we can use them to manipulate the
rainbow LEDs::
  
              self.rainbow.reset()
              self.rainbow.set_pixel(active_pixel, r, g, b)
              self.rainbow.update()
  
The code above resets the rainbow (sets all the LEDs to *off*) and then sets
the colour of only the one we want to the colour from our list.

The code for when button 2 is pressed is exactly the same, except we add one
to the counter we're storing for button 2 presses instead::
  
          if buttons['2'] is True:
              self.button2_press_count = self.button2_press_count + 1
              
              colour_index = self.button1_press_count % 9
              r, g, b = self.colours[colour_index]
              
              active_pixel = self.button2_press_count % 5
              
              self.rainbow.reset()
              self.rainbow.set_pixel(active_pixel, r, g, b)
              self.rainbow.update()
  
As before, the rest of the script is the bit that makes the whole thing run::

  class MyProject(Project):
      required_modules = [TouchTheRainbow,]
  
  if __name__ == '__main__':
      MyProject()
  
Now our project will run from within our virtual environment as follows::

  cd /home/pi/projects/blackpearl
  source venv/bin/activate
  python blackpearl/examples/example_1.py
  
Making the code neater
----------------------

Some of you will have noticed a couple of things about our project:

 * Firstly, there's a lot of code that repeats itself. Most of what's done in
   the two ``if`` statements is exactly the same, and 
 * Secondly, nothing happens until we press a button, which means that the
   first LED to light up is the second one, not the first
   
Let's address the first thing. We can break the repeated code out into
it's own method, so that if we want to change it we only have to change it
in one place, and we know that if it works for one it will work for the other.

We do this by defining a new method (which I've called ``.update_rainbow()``)
that has all the repeated code in::
  
      def update_rainbow(self):
        colour_index = self.button1_press_count % len(self.colours)
        r, g, b = self.colours[colour_index]
        
        active_pixel = self.button2_press_count % 5
        
        self.rainbow.reset()
        self.rainbow.set_pixel(active_pixel, r, g, b)
        self.rainbow.update()
        
You can also see that instead of doing ``% 9`` to get the ``colour_index`` I've
changed it to be ``len(self.colours)``. This means that if you change the number
of colours in the ``self.colours`` list the calculation will always work
(because the Python ``len()`` function returns the length of a list).

Now our button press code can be much simpler::
  
      def receive(self, message):
        buttons = message['touch']['buttons']
        if buttons['1'] is True:
            self.button1_press_count += 1
            self.update_rainbow()
        if buttons['2'] is True:
            self.button2_press_count += 1
            self.update_rainbow()

(In Python ``foo += 1`` is a shortcut for ``foo = foo + 1``).

We can address the second point because modules define a method called
``.setup()`` that is called when a new instance of the module is created. We can
use this to get the first LED lit up with the first colour by calling our new
``.update_rainbow()`` method from the ``.setup()`` method::
  
      def setup(self):
        self.update_rainbow()

This code works exactly the same way as the example at the top, but is much 
neater and addresses both of our points (plus a couple of others along the
way)::
  
  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Rainbow
  from blackpearl.things import Touch
  
  
  class TouchTheRainbow(Module):
      listening_for = ['touch',]
      hardware_required = [Touch, Rainbow,]
      
      button1_press_count = 0
      button2_press_count = 0
      colours = [(255,51,204),
                 (255,102,51),
                 (204,255,51),
                 (204,51,255),
                 (102,51,255),
                 (102,255,51),
                 (51,102,255),
                 (255,204,51),
                 (51,255,102),
                 ]
      
      def update_rainbow(self):
          colour_index = self.button1_press_count % len(self.colours)
          r, g, b = self.colours[colour_index]
          
          active_pixel = self.button2_press_count % 5
          
          self.rainbow.reset()
          self.rainbow.set_pixel(active_pixel, r, g, b)
          self.rainbow.update()
          
      def receive(self, message):
          buttons = message['touch']['buttons']
          if buttons['1'] is True:
              self.button1_press_count += 1
              self.update_rainbow()
          if buttons['2'] is True:
              self.button2_press_count += 1
              self.update_rainbow()
  
      def setup(self):
          self.update_rainbow()
          
  
  class MyProject(Project):
      required_modules = [TouchTheRainbow,]
      
      
  if __name__ == '__main__':
      MyProject()

This updated, neater, example can be found in
`blackpearl/examples/example_1_2.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/example_1_2.py>`_,
