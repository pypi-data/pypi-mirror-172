# Copyright (c) 2022, Adam Lake
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# ======================================================================================================================
# Created: 18/10/2022
# GitHub: https://github.com/adam1lake/Pi-LCD
# ======================================================================================================================

# LCD1602 pinout:
# 1 : Power Supply Ground       - Ground
# 2 : Power Supply              - +5V
# 3 : LCD Contrast              - 0-5V
# 4 : RS (Register Select)      - GPIO pin LCD_RS
# 5 : R/W (Read/Write)          - Ground
# 6 : Enable                    - GPIO pin LCD_E
# 7 : Data Bit 0                - Not used
# 8 : Data Bit 1                - Not used
# 9 : Data Bit 2                - Not used
# 10: Data Bit 3                - Not used
# 11: Data Bit 4                - GPIO pin LCD_D4
# 12: Data Bit 5                - GPIO pin LCD_D5
# 13: Data Bit 6                - GPIO pin LCD_D6
# 14: Data Bit 7                - GPIO pin LCD_D7
# 15: LCD Backlight Brightness  - 0-5V, 5V is full brightness
# 16: LCD Backlight Ground      - Ground

# ============== Imports ==============
import RPi.GPIO as GPIO
from time import sleep
import threading
from datetime import datetime

# ========= LCD1602 constants =========
LCD_WIDTH = 16
# RAM addresses for each line
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
# Enable pin timings
E_DELAY = 0.0005
E_PULSE = 0.0005
# R/S pin mode, True for character, False for command
LCD_CHR = True
LCD_CMD = False


class LCDControl:
    """
    A class to provide full control of the LCD1602 module. All GPIO PINs are BCM numbers.

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
    lcd_byte(bits, mode):
        Sends data directly to the data pins 4-7.
    lcd_string(message, line):
        Displays a string on the LCD.
    lcd_toggle_enable():
        Toggles the Enable pin.
    start_scroll(text, line, direction, timeout):
        Callback for the thread, executed when the thread is active to start the scrolling of text.
    start_scroll_thread(text, line, direction, timeout):
        Starts the scroll thread triggering start_scroll function to run.
    stop_scroll_thread(line):
        Stops the while loop in the scrolling thread, therefore stopping the thread and scrolling.
    """

    def __init__(self, lcd_rs, lcd_e, lcd_d4, lcd_d5, lcd_d6, lcd_d7):
        self.lcd_rs = lcd_rs
        self.lcd_e = lcd_e
        self.lcd_d4 = lcd_d4
        self.lcd_d5 = lcd_d5
        self.lcd_d6 = lcd_d6
        self.lcd_d7 = lcd_d7

        self.lock = False

        # Scrolling/threading variables
        self.is_scrolling = [False, False]
        self.thread = None
        self.thread_stop_timeout = 5
        self.scroll_period = 0.2

        # ======= GPIO configuration =======
        # Disables warnings
        GPIO.setwarnings(False)
        # Uses BCM GPIO numbers
        GPIO.setmode(GPIO.BCM)
        # Sets up each GPIO pin
        GPIO.setup(self.lcd_e, GPIO.OUT)
        GPIO.setup(self.lcd_rs, GPIO.OUT)
        GPIO.setup(self.lcd_d4, GPIO.OUT)
        GPIO.setup(self.lcd_d5, GPIO.OUT)
        GPIO.setup(self.lcd_d6, GPIO.OUT)
        GPIO.setup(self.lcd_d7, GPIO.OUT)

        # ======= LCD initialisation ========
        self.lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD)  # 001100 Display on, cursor off, blink off
        self.lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        sleep(E_DELAY)

    # ======= LCD control functions =======

    def lcd_byte(self, bits, mode):
        """
         Sends data directly to the data pins 4-7.

        Parameters
        ----------
        bits : int
            Data to be sent to the LCD. If Mode is True, this is a Unicdde code point for the character. If Mode is
            False, this is a RAM address for the line to be written to.
        mode : bool
            R/S pin value, set to True for character, False for command.

        Returns
        -------
        None
        """

        assert isinstance(bits, int) and isinstance(mode, bool)

        # Lock to prevent two writes in lcd_byte from occurring at the same time
        while self.lock:
            pass

        self.lock = True

        # Sets R/S pin based on the mode
        GPIO.output(self.lcd_rs, mode)

        # High bits
        GPIO.output(self.lcd_d4, False)
        GPIO.output(self.lcd_d5, False)
        GPIO.output(self.lcd_d6, False)
        GPIO.output(self.lcd_d7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(self.lcd_d4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(self.lcd_d5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(self.lcd_d6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(self.lcd_d7, True)

        # Toggle the Enable pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.lcd_d4, False)
        GPIO.output(self.lcd_d5, False)
        GPIO.output(self.lcd_d6, False)
        GPIO.output(self.lcd_d7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(self.lcd_d4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(self.lcd_d5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(self.lcd_d6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(self.lcd_d7, True)

        # Toggle the Enable pin
        self.lcd_toggle_enable()

        self.lock = False

    def lcd_string(self, message, line):
        """
        Displays a string on the LCD.

        This function sends commands to the LCD to display the message on the specified line.

        Parameters
        ----------
        message : str
            The string to be displayed on the screen.
        line : int
            The line on which the string is to be displayed. Must be 1 or 2.

        Returns
        -------
        None
        """

        # Sets the RAM address for the line
        if line == 1:
            line_address = 0x80
        else:
            line_address = 0xC0

        message = message.ljust(LCD_WIDTH, " ")

        self.lcd_byte(line_address, LCD_CMD)

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def lcd_toggle_enable(self):
        """
        Toggles the Enable pin.

        This function sets the enable pin, allowing the LCD to correctly read the data send to it in the lcd_byte
        function.

        Returns
        -------
        None
        """

        # Toggle enable
        sleep(E_DELAY)
        GPIO.output(self.lcd_e, True)
        sleep(E_PULSE)
        GPIO.output(self.lcd_e, False)
        sleep(E_DELAY)

    # ======= Scrolling functions =======

    def start_scroll(self, text, line, direction, timeout):
        """
        Callback for the thread, executed when the thread is active to start the scrolling of text.

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

        # Sets the start string depending on the direction
        if direction == "left":
            start = (" " * 16) + text
        else:
            start = text + (" " * 16)

        # Initial variables for the while loop
        displayed = start
        text_length = len(text)

        self.is_scrolling[line-1] = True

        # Start time of the while loop
        start = datetime.now()

        while self.is_scrolling[line-1]:
            if direction == "left":
                # Displays the text
                self.lcd_string(displayed[0:16], line)
                # Adds the first character of the string to the end of the string
                displayed += displayed[0]
                # Removes the first character of the string
                displayed = displayed[1:]
            else:
                # Displays the text
                self.lcd_string(displayed[text_length:16+text_length], line)
                # Adds the last character of the string to the start of the string
                displayed = displayed[-1] + displayed
                # Removes the last character of the string
                displayed = displayed[:-1]

            if timeout is not None:
                # Breaks the while loop when the timeout is reached
                if (datetime.now() - start).total_seconds() > timeout:
                    break

            sleep(self.scroll_period)

        self.is_scrolling[line-1] = False

    def start_scroll_thread(self, text, line, direction, timeout):
        """
        Starts the scroll thread triggering start_scroll function to run.

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

        self.thread = threading.Thread(target=self.start_scroll, args=(text, line, direction, timeout))
        self.thread.start()

    def stop_scroll_thread(self, line):
        """
        Stops the while loop in the scrolling thread, therefore stopping the thread and scrolling.

        Parameters
        ----------
        line : int
            The line on which the scrolling should be stopped. Must be 1 or 2.
        Returns
        -------
        None
        """

        # Checks that the thread has been initialised
        if isinstance(self.thread, threading.Thread):
            # Start time of the while loop
            start = datetime.now()
            self.is_scrolling[line-1] = False

            while True:
                # Breaks to cleanup when the thread is no longer alive
                if not self.thread.is_alive():
                    break
                    # Exits the function before cleaning up if the thread is still running after a timeout
                if (datetime.now() - start).total_seconds() > self.thread_stop_timeout:
                    raise RuntimeError("Failed to stop thread.")
                # Period at which the thread is polled to check its status
                sleep(0.1)

        # Clears the screen
        self.lcd_string("", 1)
        self.lcd_string("", 2)
