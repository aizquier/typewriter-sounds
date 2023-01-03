Typewriter sounds emulator for Python
=====================================

This program plays typewriter sounds each time a key is pressed, giving
the user the vintage experience of and old typewriter machine.

The code is inspired on the keylogger demo that comes in the The Python
X Library ( <http://python-xlib.sourceforge.net/> ). The logic is
simple: grab the keycode of a pressed key, and instead to record it (as
any keylogger does), just play a sound.

As the key detection is made using Xlib, this program should work on
those platforms that support X11. It was developed and tested under
Linux.

Sound samples come from <https://www.freesound.org/>, some were modified
for this project.

Requeriments
------------

-   Python 3.5
-   [X11 and Xlib bindings for Python](http://python-xlib.sourceforge.net/)
-   [PyGame](http://pygame.org) (for sound)

Install requeriments:

    $ pip install -r requeriments.txt


Usage
-----

cd into the project's directory and type:

    $ python typewriter_sounds.py

to stop the program, just type CTRL-C.

TODO
----

-   Test it in different platforms. In Windows it should work using
    Cygwin
-   Add an installer
-   Eventually: add a tray icon GUI.

Author
------

Manuel Arturo Izquierdo <aizquier@gmail.com>

