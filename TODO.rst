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

New features
============

Make matrix choose how it implements its clock?
Add column move column on matrix (so we can plot moving graphs)
Add .active_pixels() to rainbow (so that set_all() only sets those marked as 'active'
If we've got animation on the matrix why not on the rainbow and clock?

