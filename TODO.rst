Missing things
==============

Joystick Module - lots of maths
 - left/right, up/down, steering
 
Light Module - simple, like weather (I think!)

Motion Module - simple, like weather
 - six axes?
 
URL fetchers
 - JSON fetcher
 - Scraper?
 
Minecraft
 - event on flotilla causes event in minecraft (e.g. button press, temperature change)
 - event in minecraft causes event on flotilla (e.g. door opening causes rainbow to flash)

Docstrings are woeful

Little refactorings
===================

Noticed that the Matrix has a .update() method that takes pixels, whereas the
other .update() methods (rainbow and number) are called without parameters and
take the values set on the class. Think this probably needs to be made the same
- look at .addFrame() and .next()

New features
============

Make matrix choose how it implements its clock?
Add-column-move-column on matrix (so we can plot moving graphs)
Add .active_pixels() to rainbow (so that set_all() only sets those marked as 'active'
If we've got animation on the matrix why not on the rainbow and clock?

