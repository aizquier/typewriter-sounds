from __future__ import print_function
import sys
import os
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
import pygame

class TypeWriterSounds:

    """
    Typewriter sounds emulator for Python
    =====================================

    This program plays typewriter sounds each time a key is pressed, giving
    the user the vintage experience of and old typewriter machine.

    The code is inspired on the keylogger demo that comes in the The Python
    X Library ( http://python-xlib.sourceforge.net/ ). The logic is simple:
    grab the keycode of a pressed key, and instead to record it (as any
    keylogger does), just play a sound.

    As the key detection is made using Xlib, this program should work on
    those platforms that support X11. It was developed and tested under
    Linux.

    Sound samples come from https://www.freesound.org/, some were modified
    for this project.

    Requeriments
    ------------

    -   Python >= 3.5 
    -   [X11 and Xlib bindings for Python](http://python-xlib.sourceforge.net/)
    -   [PyGame](http://pygame.org) (for sound)

    Install requeriments:

         $ pip install -r requeriments.txt


    Usage
    -----

    cd into the project's directory and type:

    ::

        $ python typewriter~sounds~.py

    to stop the program, just type CTRL-C.

    TODO
    ----

    -  Test it in different platforms. In Windows it should work using
       Cygwin
    -  Add an installer
    -  Eventually: add a tray icon GUI.

    Author
    ------

    Manuel Arturo Izquierdo aizquier@gmail.com

    """

    def __init__(self):
        # * Initialises pygame mixer. A buffer of 512 bytes is required for
        # * better performance
        pygame.mixer.init(buffer=512)

        self.bellcount = 0

        # * Preloads sound samples
        self.keysounds = {
            'load' : pygame.mixer.Sound('samples/manual_load_long.wav'),
            'shift' : pygame.mixer.Sound('samples/manual_shift.wav'),
            'delete': pygame.mixer.Sound('samples/manual_backspace.wav'),
            'space': pygame.mixer.Sound('samples/manual_space.wav'),
            'key': pygame.mixer.Sound('samples/manual_key.wav'),
            'enter': pygame.mixer.Sound('samples/manual_return.wav'),
            'bell': pygame.mixer.Sound('samples/manual_bell.wav')
        }

        # * Get keynames from X11
        self.keys = {}
        for name in dir(XK):
            if name[:3] == "XK_" :
                self.keys[name] = getattr(XK, name)


        print("TypeWriter Sounds Emulator. v1.1")
        print("type now and enjoy the vintage experience!...")
        self.keysounds['bell'].play()
        self.keysounds['enter'].play()


        # * Activates key grabber

        self.local_dpy = display.Display()
        self.record_dpy = display.Display()

        # Check if the extension is present
        if not self.record_dpy.has_extension("RECORD"):
            print ("RECORD extension not found")
            sys.exit(1)



        # Create a recording context; we only want key events
        self.ctx = self.record_dpy.record_create_context(
                0,
                [record.AllClients],
                [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        'device_events': (X.KeyPress, X.KeyPress),
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                }])


        try:
            # Enable the context; this only returns after a call to
            # record_disable_context,
            # while calling the callback function in the meantime
            self.record_dpy.record_enable_context(  self.ctx, \
                                                    self.record_callback)
        except KeyboardInterrupt:
            # Exits if CTRL-c is typed
            self.record_dpy.record_free_context(self.ctx)
            print('\nbye!')
            sys.exit(0)

    def record_callback(self, reply):
        if reply.category != record.FromServer:
            return

        if reply.client_swapped:
            print("* received swapped protocol data, cowardly ignored")
            return

        if not len(reply.data) or ord(str(reply.data[0])) < 2:
        # not an event
            return

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).\
                            parse_binary_value( data,
                                                self.record_dpy.display,
                                                None, None)

            if event.type == X.KeyPress:
                # * If a key is pressed, gets its keycode
                pr = event.type == X.KeyPress and "Press" or "Release"
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)


                # * Plays an audio sample according the keycode

                # * - Enter
                if keysym == self.keys['XK_Return']:
                    self.keysounds['enter'].play()
                    self.bellcount = 0

                # * - Spacebar
                elif keysym == self.keys['XK_space']:
                    self.keysounds['space'].play()
                    self.bellcount += 1

                # * - Delete and backspace
                elif (keysym == self.keys['XK_Delete']) or \
                     (keysym == self.keys['XK_BackSpace']):
                    self.keysounds['delete'].play()
                    self.bellcount -= 1
                    if self.bellcount <= 0:
                        self.bellcount = 0

                # * - Shift (and other control keys)
                elif    keysym == self.keys['XK_Up'] or \
                        keysym == self.keys['XK_Down'] or \
                        keysym == self.keys['XK_Left'] or \
                        keysym == self.keys['XK_Right'] or \
                        keysym == self.keys['XK_Control_L'] or \
                        keysym == self.keys['XK_Control_R'] or \
                        keysym == self.keys['XK_Shift_R'] or \
                        keysym == self.keys['XK_Shift_L'] or \
                        keysym == self.keys['XK_Alt_L'] or \
                        keysym == self.keys['XK_Alt_R'] or \
                        keysym == self.keys['XK_Tab'] or\
                        keysym == self.keys['XK_Caps_Lock'] or \
                        keysym == self.keys['XK_F1'] or \
                        keysym == self.keys['XK_F2'] or \
                        keysym == self.keys['XK_F3'] or \
                        keysym == self.keys['XK_F4'] or \
                        keysym == self.keys['XK_F5'] or \
                        keysym == self.keys['XK_F6'] or \
                        keysym == self.keys['XK_F7'] or \
                        keysym == self.keys['XK_F8'] or \
                        keysym == self.keys['XK_F9'] or \
                        keysym == self.keys['XK_F10'] or \
                        keysym == self.keys['XK_F11'] or \
                        keysym == self.keys['XK_F12'] or \
                        keysym == self.keys['XK_Super_L'] or\
                        keysym == self.keys['XK_Super_R'] or\
                        keysym == self.keys['XK_Escape'] or\
                        keysym > 65535:

                    self.keysounds['shift'].play()

                # * - Page Up/Down, Home/End: play page load
                elif    keysym == self.keys['XK_Page_Up'] or \
                        keysym == self.keys['XK_Next'] or\
                        keysym == self.keys['XK_Home'] or \
                        keysym == self.keys['XK_End']:
                    self.keysounds['load'].play()

                # * - A simple key
                else:
                    self.keysounds['key'].play()
                    self.bellcount += 1

                # * - After 70 consecutive keypresses, play the bell sound
                if self.bellcount == 70:
                    self.keysounds['bell'].play()
                    self.bellcount = 0

if __name__ == '__main__':
    TypeWriterSounds()
