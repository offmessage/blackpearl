==========
blackpearl
==========

For Twisted Little Pirates
--------------------------

What is it?
===========

This packages provides an asyncronous API to the Pimoroni Flotilla (you can
read more at `http://flotil.la`). It is so named because we rely on the
excellent Twisted network communication library to do all our heavy lifting.

Why?
====

With some excitement I fired up my Flotilla when it first arrived. I was running
it on a Raspberry Pi 2 (as recommended), but as soon as we tried to do anything
complicated - more than a couple of inputs, outputs and transformations, for
example - the CPU usage went flat out and loads of lag was introduced. I had a
quick read of the various forum posts and it seemed like I should try the Python
API instead. Luckily I used to write Python for a living and still keep my hand
in.

Unfortunately the Python API as provided isn't the most efficient way of doing
things. In fact, the Python API also pegs the processor, largely because of its
reliance on ``while True`` loops and lots of ``time.sleep()`` calls.

**blackpearl** is capable of taking input from multiple inputs, processing that input
and sending it to multiple outputs with the Rpi2 running at around 7% processor
load. In other words, you could be playing with your Flotilla while also
watching a movie. On a Raspberry Pi.

Installation
============

I assume that you are looking for something more than the *"pipe this URL through
bash, while running as root"*. I know that those types of instructions are easy
to follow, but they are dangerous. We are pirates. We only take calculated
risks.

Add the ``pi`` (or your preferred user) to the ``dialout`` group

Create a python virtual environment

Clone this package into that virtualenv

pip install -e .