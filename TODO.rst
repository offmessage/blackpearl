Missing modules
===============

Joystick - lots of maths
 - left/right, up/down, steering
Light - simple, like weather (I think!)
Motion - simple, like weather
 - six axes?
 
URL fetchers
 - JSON fetcher
 - Scraper?
Minecraft
 - event on flotilla causes event in minecraft (e.g. button press, temperature change)
 - event in minecraft causes event on flotilla (e.g. door opening causes rainbow to flash)

Little refactorings
===================

Noticed that ``hardware_required``, ``software_required`` but ``required_modules``

Noticed that the Matrix has a .update() method that takes pixels, whereas the
other .update() methods (rainbow and number) are called without parameters and
take the set values. Think this probably needs to be made the same - look at
.addFrame() and .next()

Check where waves and clocks and so on get created - are they attributes of
modules (in which case they can't be manipulated by other modules)? If they are
fix this so that they are attributes of the project, and then attached to
modules as required (so self.sawtoothwave is the same instance of SawtoothWave
for every module)

New features
============

Make matrix choose how it implements its clock?
Add-column-move-column on matrix (so we can plot moving graphs)
Add .active_pixels() to rainbow (so that set_all() only sets those marked as 'active'
If we've got animation on the matrix why not on the rainbow and clock?

