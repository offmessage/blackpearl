==========
blackpearl
==========

Flotilla for Twisted Little Pirates
-----------------------------------

**blackpearl** aims to provide an easy to use Python framework to allow coders
from novice to expert to interact with Pimoroni's `Flotilla
<http://flotil.la>`_. As well as being easy to use it is also fast; blisteringly
fast. Hence its name.

  *I've heard of one, supposed to be very fast, nigh uncatchable: The Black
  Pearl*
  
(It also helps that we're using `Twisted <https://twistedmatrix.com/>`_ under
the hood, and the crew of The Black Pearl were definitely ... *twisted*)

It is available on GitHub at https://github.com/offmessage/blackpearl This is
where you should raise issues, should you find any. Increasingly complete
documentation is available at https://offmessage.github.io/blackpearl/

**blackpearl** is capable of taking input from multiple inputs, processing that
input and sending it to multiple outputs with the Rpi2 running at around 4%
processor load. In other words, you could be playing with your Flotilla whilst
also watching an HD movie. On a Raspberry Pi. Neat, huh?

It has a quick *"plug and play"* style of coding that allows users to get
started very quickly, but provides a rich API under the hood that more
experienced coders can use for far more complex projects.

And when I say get started very quickly, this is all the code you have to
write to get the rainbow module displaying the colour that the colour sensor
is currently looking at::

  class ColourMatcher(Module):
      hardware_required = [Colour, Rainbow,]
      listening_for = ['colour']
      
      def receive(self, message):
          r, g, b = message['colour']['rgb']
          self.rainbow.set_all(r, g, b)
          self.rainbow.update()


Installation
============

Right now you need to know what you're doing, Python-wise, to use it
so I'm deliberately making the instructions very high level. If the following
don't make sense you should probably hang on for a bit. Version 1.0.0 is just
around the corner and will be well documented::

  cd ~/projects
  git clone https://github.com/offmessage/blackpearl
  cd blackpearl
  virtualenv -p python3 venv
  source venv/bin/activate
  pip install -e .
  
To see what it's capable of, connect all of the following to your Flotilla (and
connect your Flotilla to your Rpi2):

 * The rainbow
 * The touch
 
And then::

  cd ~/projects/blackpearl
  source venv/bin/activate
  cd blackpearl/projects
  python touchtherainbow.py

Further examples are in the ``examples/`` directory. More documentation is
available at https://offmessage.github.io/blackpearl/ - this is slowly
improving. Bear with me.
