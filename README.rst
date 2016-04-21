==========
blackpearl
==========

Flotilla for Twisted Little Pirates
-----------------------------------

What is it?
===========

This packages provides an asyncronous API to the Pimoroni Flotilla (you can
read more at `http://flotil.la`).

  I've heard of one, supposed to be very fast, nigh uncatchable: The Black Pearl
  
It is so named because we rely on the Twisted network communication library to
do all our heavy lifting, and because we want to be like Captain Jack.

Why?
====

As provided both the Javascript and Python APIs for the Flotilla cause the
Raspberry Pi 2 processor to max out and lots of lag to be introduced as soon as
you try to do anything complicated with it. Javascript is not my thing, but
Python is. So I thought I'd help out and write a more efficient Python API.

**blackpearl** is capable of taking input from multiple inputs, processing that
input and sending it to multiple outputs with the Rpi2 running at around 4%
processor load. In other words, you could be playing with your Flotilla whilst
also watching a movie. On a Raspberry Pi.

Installation
============

Right now (0.0.1.dev0) you really need to know what you're doing, Python-wise,
so I'm deliberately making the instructions very high level. If the following
don't make sense you should probably hang on for a bit. Version 1.0.0 is just
around the corner and will be well documented:

- Create a python3 virtual environment
- Clone this repository into it
- ``pip install -e .``

Examples will be forthcoming.