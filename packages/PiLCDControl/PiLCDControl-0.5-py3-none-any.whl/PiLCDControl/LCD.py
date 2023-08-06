# Copyright (c) 2022, Adam Lake
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# ======================================================================================================================
# Created: 18/10/2022
# GitHub: https://github.com/adam1lake/Pi-LCD
# ======================================================================================================================

from time import sleep
from numbers import Number
from PiLCDControl import _LCDControl
from RPi.GPIO import GPIO


class LCD:
    """
    A class to provide a user-friendly interface to the LCD1602 module. All GPIO PINs are BCM numbers.

    Attributes
    ----------
    lcd_rs : int
        GPIO pin for the connection to the LCD Register Select (RS) pin
    lcd_e : int
        GPIO pin for the connection to the LCD Enable (E) pin
    lcd_d4 : int
        GPIO pin for the connection to the LCD Data Bit 4 (D4) pin
    lcd_d5 : int
        GPIO pin for the connection to the LCD Data Bit 5 (D5) pin
    lcd_d6 : int
        GPIO pin for the connection to the LCD Data Bit 6 (D6) pin
    lcd_d7 : int
        GPIO pin for the connection to the LCD Data Bit 7 (D7) pin
    Methods
    -------
    display_text(text, line, timeout, fade_in):
        Displays the text on the screen with an optional timeout
    start_scroll(text, line, direction, timeout):
        Scrolls through the text either indefinitely or until the timeout
    stop_scroll(line):
        Stops scrolling on the given line
    """

    def __init__(self, lcd_rs, lcd_e, lcd_d4, lcd_d5, lcd_d6, lcd_d7, fade_in_delay=0.05):
        # Asserts that all the GPIO pins are integers
        assert isinstance(lcd_rs, int) and isinstance(lcd_e, int) and isinstance(lcd_d4, int) and isinstance(lcd_d5, int) and isinstance(lcd_d6, int) and isinstance(lcd_d7, int), "GPIO pins must be integers."
        self.lcd_control = _LCDControl.LCDControl(lcd_rs, lcd_e, lcd_d4, lcd_d5, lcd_d6, lcd_d7)
        self.fade_in_delay = fade_in_delay

        # Constants
        self.is_scrolling = False
        self.thread = None

    def display_text(self, text, line, timeout=None, fade_in=False):
        """
        Displays text on the LCD.

        Parameters
        ----------
        text : str
            The string to be displayed scrolling on the screen. Must be less than or equal to 16 characters.
        line : int
            The line on which the string is to be displayed. Must be 1 or 2.
        timeout : Number, optional
            Time in seconds after which the text should disappear.
        fade_in : bool, optional
            Whether to fade the text in character-by-character or display it immediately
        Returns
        -------
        None
        """

        assert isinstance(text, str) and len(text) <= 16, "Invalid text value."
        assert line == 1 or line == 2, "Invalid line value."
        assert timeout is None or isinstance(timeout, Number), "Invalid timeout value."
        assert isinstance(fade_in, bool), "Invalid fade_in value."

        # If scrolling is active for this line, stop it
        if self.lcd_control.is_scrolling:
            self.lcd_control.stop_scroll_thread(line)

        if fade_in:
            # Displays the string at one character per time with a delay between characters.
            for x in range(len(text) + 1):
                self.lcd_control.lcd_string(text[:x], line)
                sleep(self.fade_in_delay)
        else:
            self.lcd_control.lcd_string(text, line)
        if timeout is not None:
            # If an integer timeout has been specified, wait, then clear the line
            sleep(timeout)
            self.lcd_control.lcd_string("", line)

    def start_scroll(self, text, line, direction="left", timeout=None):
        """
        Scrolls through the text either indefinitely or until the timeout

        Parameters
        ----------
        text : str
            The string to be displayed scrolling on the screen.
        line : int
            The line on which the string is to be displayed. Must be 1 or 2.
        direction : str
            The direction that scrolling should occur in. Left or Right.]
        timeout : Number, optional
            Time in seconds after which the scrolling should be stopped.
        Returns
        -------
        None
        """
        assert isinstance(text, str), "Invalid text value."
        assert line == 1 or line == 2, "Invalid line value."
        direction = direction.lower()
        assert direction == "left" or direction == "right", "Invalid direction value."
        assert timeout is None or isinstance(timeout, Number), "Invalid timeout value."

        self.lcd_control.start_scroll_thread(text, line, direction, timeout)

    def stop_scroll(self, line):
        """
        Stops the text scrolling on the specified line.

        Parameters
        ----------
        line : int
            The line on which the scrolling should be stopped. Must be 1 or 2.
        Returns
        -------
        None
        """
        assert line == 1 or line == 2, "Invalid line value."
        self.lcd_control.stop_scroll_thread(line)

    def cleanup(self):
        """
        Clears the display and performs GPIO cleanup.

        Returns
        -------
        None
        """
        self.display_text("", 1)
        self.display_text("", 2)
        self.stop_scroll(1)
        self.stop_scroll(2)
        GPIO.cleanup()
