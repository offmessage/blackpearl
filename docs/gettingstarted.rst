.. _gettingstarted:
    
Getting started with blackpearl
===============================

The basics
----------

**blackpearl** makes heavy use of Python classes, so you'll need to be
comfortable with Python's concept of subclassing to make the most of it. By 
taking this approach I've allowed beginners to simply change a few things and 
see the effect, and more advanced programmers to get into the guts of it and 
build their own classes using the building blocks provided. Hopefully that 
strikes a good balance, even if it does require a little more Python knowledge 
than the very basics.

**blackpearl** has the concept of a **Project**. There is only one **Project**
running at a time, and a **Project** acts as the container for all of your code.

Hanging off projects are **Modules**. These are containers of code that tie
together functionality. A **Project** can contain any number of **Modules**, and
**Modules** can interact with each other via messages that are passed around
the system.

Each module defines 3 things:

 * What messages it's listening for
 * What hardware needs to be connected to the Flotilla dock for the module to
   work
 * What additional software components (like clocks, wave generators, etc) are
   also needed for the module to work
   
An example
----------

.. note:: To start with we'll only use the rainbow and the touch, as these are
          the components that come with the Mini Starter Kit. Later projects
          will use the parts that came with the larger kits.
          
I'll use the example that we used to test our installation to describe what's
going on in practical terms. That script can be found in
`blackpearl/examples/touchtherainbow.py
<https://github.com/offmessage/blackpearl/blob/master/blackpearl/examples/touchtherainbow.py>`_,
but it's also included here in its entirety for reference::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  from blackpearl.things import Rainbow
  from blackpearl.things import Touch
  
  
  class TouchTheRainbow(Module):
      listening_for = ['touch',]
      hardware_required = [Touch, Rainbow,]
      
      def receive(self, message):
          # We're listening for buttons!
          buttons = message['touch']['buttons']
          if buttons['1']:
              self.rainbow.set_all(255, 0, 0)
              self.rainbow.update()
          elif buttons['2']:
              self.rainbow.set_all(0, 255, 0)
              self.rainbow.update()
          elif buttons['3']:
              self.rainbow.set_all(0, 0, 255)
              self.rainbow.update()
          elif buttons['4']:
              self.rainbow.reset()
  
  
  class MyProject(Project):
      required_modules = [TouchTheRainbow,]
      
      
  if __name__ == '__main__':
      MyProject()
  
At the top of the file we import the necessary bits and bobs, Firstly, as
described above, the **Module** and **Project** classes that are the basic
building blocks of a **blackpearl** project::

  from blackpearl.modules import Module
  from blackpearl.projects import Project
  
Then from ``blackpearl.things`` (because they are, after all, *things*), we
import the things that we need for our module to work::

  from blackpearl.things import Rainbow
  from blackpearl.things import Touch

**blackpearl** provides a Python class for each of the hardware components that
come with the Flotilla kits. So there is a ``Rainbow`` class for the rainbow
LEDs, a ``Touch`` class for the touch keypad, a ``Motor`` class for the motors
and so on (these are documented in detail later on; please feel free to skip
ahead if this bit's boring!)

Next we define our own module, using **blackpearl**'s **Module** class as our
base class::

  class TouchTheRainbow(Module):
  
This is the core component of **blackpearl**. Each module that we build
works up from one of the base **Module** classes (we'll talk about the others
later), and defines its own code on top.

Each module can define any of three things - what messages it's interested in
receiving, what hardware is required for it to work, and what additional
software is required for it to work. In this first example we're only interested
in the first two; ``listening_for`` and ``hardware_required``::

      listening_for = ['touch',]
      
The ``listening_for`` attribute is a Python list that defines which messages
the module is hoping to receive. Only messages sent by the things in this list
will be passed to our module's ``.receive()`` method. All of the standard
messages that **blackpearl** sends out are listed on the :doc:`messages page
</messages>`, but for the purposes of this example we're only interested
in ``'touch'``.

::
  
      hardware_required = [Rainbow, Touch,]

The ``hardware_required`` attribute defines which Flotilla hardware our module
needs in order to work. Like ``listening_for`` it's a Python list, but this
time it includes the *classes* we imported from ``blackpearl.things``; that
means their names are *not* in quotes.

Every time a message is broadcast that our module has said it's listening for
the message gets passed to the ``.receive()`` method of our module. So next we
define that method::

      def receive(self, message):
          # We're listening for buttons!
          buttons = message['touch']['buttons']
  
Each message that arrives is a dictionary, called ``message``. Each message is
structured such that the first key is the name of the thing that we're listening
for (in this case ``'touch'``. The Touch hardware sends out its message in the
form of another dictionary (called ``'buttons'``) that defines each button on
the keypad. If the button is ``True`` then it's pressed. If it's ``False`` then
it's not.

An example message from the touch when someone has pressed button 1 will look 
like this::

  {'touch': {'buttons': {'1': True,
                         '2': False,
                         '3': False,
                         '4': False,
                         }
             }
   }

Our code then takes some decisions based on which button has been pressed.
Remember, our ``.receive()`` method is only called when a button has been
pressed or released, because we're only listening for messages from the touch.

::

          if buttons['1']:
              self.rainbow.set_all(255, 0, 0)
              self.rainbow.update()
          elif buttons['2']:
              self.rainbow.set_all(0, 255, 0)
              self.rainbow.update()
          elif buttons['3']:
              self.rainbow.set_all(0, 0, 255)
              self.rainbow.update()
          elif buttons['4']:
              self.rainbow.reset()
  
One slight piece of magic (magic isn't generally considered very Pythonic, but
it's useful here) is that by listing things in ``hardware_required`` our
module automatically gets attributes that match the required hardware. In other
words, if we list a ``Rainbow``, our module automatically gets to access the
``Rainbow`` code through an attribute called ``.rainbow``. (Even cleverer, if
there's more than one they are magically numbered, and called ``.light1`` and
``.light2``, for example).

Which means, in the example above, that we're able to access our rainbow LEDs
through the ``.rainbow`` attribute of our module. The methods that the
``Rainbow`` offers are all explained on :doc:`its page
</hardware/outputs/rainbow>`, but for the purposes of this example all we care
about right now are the ``.set_all()`` and ``.update()`` methods.

``.set_all()`` sets the RGB value of all 5 of the rainbow's LEDs, while
``.update()`` tells the rainbow to use the new values. The RGB values are passed
in to ``.set_all()`` in the order red, green, blue, and should be in the range
0 to 255 (anyone used to web design or CSS will recognise this format for
describing a colour). So the code above says: if button 1 is pressed, set all
of the rainbow's LEDs to red. If button 2 is pressed set all the rainbow's LEDs
to green. If button 3 is pressed set them all to blue, and if button 4 is
pressed turn them all off.

That's all the code we need to write to make the rainbow respond to button
presses on the touch.

To recap:

 * We define the messages we're ``listening_for``
 * We define the ``hardware_required``
 * Then we define our ``.receive()`` method that acts upon the message we
   receive, talking to the rainbow through the magic ``.rainbow`` attribute

The rest of the script is the bit that actually makes it run. Remember I said
at the top of this page that the **Project** is the bit that everything hangs
off? Well, we need to define a project, and attach our ``TouchTheRainbow``
module to it. We use the **Project**'s ``required_modules`` attribute to tell
the project which modules it should use. This is, like ``hardware_required`` on
the **Module**, is a list of classes (so names *not* in quotes)::

  class MyProject(Project):
      required_modules = [TouchTheRainbow,]
  
And then finally we need to make our code run when it's passed to the python
interpreter (the ``if __name__ == '__main__'`` bit is just standard Python, it
means that if you invoke the script using ``python touchtherainbow.py`` it'll
run). Anything that subclasses **blackpearl**'s **Project** class will
automatically run when an instance is created. This means that all we need to
do in our ``if __name__ == '__main__'`` block is create an instance of our
project class (which we do by *calling* it; putting brackets after its name)::

  if __name__ == '__main__':
      MyProject()
  
Now our project will run from within our virtual environment as follows::

  cd /home/pi/projects/blackpearl
  source venv/bin/activate
  python blackpearl/examples/touchtherainbow.py
  
