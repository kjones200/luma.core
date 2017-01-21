# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

import atexit

from luma.core.serial import i2c
from luma.core import mixin
import luma.core.const


class device(mixin.capabilities):
    """
    Base class for display driver classes

    .. warning::
        Direct use of the :func:`command` and :func:`data` methods are
        discouraged: Screen updates should be effected through the
        :func:`display` method, or preferably with the
        :class:`luma.core.render.canvas` context manager.
    """
    def __init__(self, const=None, serial_interface=None):
        self._const = const or luma.core.const.common
        self._serial_interface = serial_interface or i2c()
        atexit.register(self.cleanup)

    def command(self, *cmd):
        """
        Sends a command or sequence of commands through to the delegated
        serial interface.
        """
        self._serial_interface.command(*cmd)

    def data(self, data):
        """
        Sends a data byte or sequence of data bytes through to the delegated
        serial interface.
        """
        self._serial_interface.data(data)

    def show(self):
        """
        Sets the display mode ON, waking the device out of a prior
        low-power sleep mode.
        """
        self.command(self._const.DISPLAYON)

    def hide(self):
        """
        Switches the display mode OFF, putting the device in low-power
        sleep mode.
        """
        self.command(self._const.DISPLAYOFF)

    def contrast(self, level):
        """
        Switches the display contrast to the desired level, in the range
        0-255. Note that setting the level to a low (or zero) value will
        not necessarily dim the display to nearly off. In other words,
        this method is **NOT** suitable for fade-in/out animation.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0 <= level <= 255)
        self.command(self._const.SETCONTRAST, level)

    def cleanup(self):
        self.hide()
        self.clear()
        self._serial_interface.cleanup()
