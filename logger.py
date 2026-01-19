"""
    Project: AU-23-0044 [TEMPEROFEN LOGGING]
    Author(s): Simon Schachinger, Marcel Luttenberger

    File: TEMPLATE.py
    Version: V1.1.2 (08.08.2025)

    File-/Projectdescription:
        This file holds the class logger and its methods

    Hotspots:

    Arguments:

    Returns:
"""

# LIBRARIES:
###############################################################################
# Standard Libraries
from __future__ import annotations      # for target datatype annotation
from colorama import Fore, Style, init  # for console coloring
import inspect                          # for parent file data
from enum import Enum                   # for ENUM usage
import datetime                         # for time handling
# Custom Modules
###############################################################################

# GLOBAL VARIABLES
###############################################################################
###############################################################################

# CLASSES
###############################################################################
class Logger:
    """
    Summary:
        ... used to handle logging mechanisms. This is intended for console and
        UI logging purposes.

    Args:

    Returns:
        self (type Logger):
    """

    class LEVEL(Enum):
        """
        Summary:
            ... used to sort logging levels

        Args:

        Returns:
            none
        """
        DEBUG = 0
        INFO = 1
        WARNING = 2
        ERROR = 3
        NONE = 100

        @property
        def char(self) -> str:
            return {
                self.DEBUG: "#",
                self.INFO: "i",
                self.WARNING: "!",
                self.ERROR: "X",
                self.NONE: "-"
            }[self]

        @property
        def color(self):
            return {
                self.DEBUG: Fore.CYAN,
                self.INFO: Fore.GREEN,
                self.WARNING: Fore.YELLOW,
                self.ERROR: Fore.RED,
                self.NONE: Fore.WHITE
            }

    def __init__(self, arg_level: Logger.LEVEL = LEVEL.DEBUG, arg_file = None) -> None:
        """
        Summary:
            ... used to initiate the logging class - automatically called.

        Args:
            arg_level (LEVEL): minimum logging level

        Returns:
            none
        """
        self.level = None
        self.set_level(arg_level)
        self.file = arg_file

        init(autoreset=False)

    def __str__(self):
        """
        Summary:
            ... used to return string from class

        Args:

        Returns:
            corresponding string
        """

        return self.level.name

    def set_level(self, arg_level: LEVEL = LEVEL.DEBUG):
        """
        Summary:
            ... used to set the minimum logging level.

        Args:
            arg_level (LEVEL): minimum logging level

        Returns:
            TRUE, if valid arg_level
            FALSE, if invalid arg_level
        """

        if not isinstance(arg_level, self.LEVEL):
            self.level = self.LEVEL.DEBUG
            self.log("Invalid level passed.", Logger.LEVEL.DEBUG)
            return False
        else:
            self.level = arg_level
            return True

    def log(self, arg_message: str = None, arg_level: Logger.LEVEL = None):
        """
        Summary:
            ... logs the message:

        Args:
            arg_message (str): payload of message
            arg_level (LEVEL): logging level

        Returns:
            None
        """

        if not (level := self.check_level(arg_level)):
            self.log("Level requirement not met.", Logger.LEVEL.DEBUG)
            return False

        if not (message := self.check_message(arg_message)):
            self.log("Message not passed.", Logger.LEVEL.DEBUG)
            return False



        log_message = self.create_msg(arg_level, arg_message)

        print(log_message)
        open("dev/log.txt", "a").write(f"\n{log_message}")
        return True

    def level2string(self, arg_level: LEVEL = None):
        """
        Summary:
            ... used to return string from ENUM

        Args:
            arg_level (enum Level): log level to return string, defaults to set level

        Returns:
            corresponding string
        """

        if arg_level is None:
            arg_level = self.level

        return arg_level.name

    def level2char(self, arg_level: LEVEL = None):
        """
        Summary:
            ... used to return char from ENUM

        Args:
            arg_level (enum Level): log level to return char, defaults to set level

        Returns:
            corresponding string
        """

        if arg_level is None:
            arg_level = self.level

        return arg_level.char

    def check_message(self, arg_message: str = None) -> str | bool:
        """
        Summary:
            ... checks if message was passed and returns applicable payload

        Args:
            arg_message (str): payload of message

        Returns:
            message if message was passed
            "Message was not passed." when message was not passed and self.level is self.LEVEL.DEBUG
            "FALSE" if message was not passed and self.level is not self.LEVEL.DEBUG
        """

        if arg_message is None:
            if self.level is self.LEVEL.DEBUG:
                return "Message was not passed."
            else:
                return False
        else:
            return arg_message

    def check_level(self, arg_level: Logger.LEVEL = None) -> Logger.LEVEL | bool:
        """
        Summary:
            ... checks if message level is higher than minimum level

        Args:
            arg_level (str): level of message

        Returns:
            arg_level if arg_level was passed and higher than minimum level
            self.level is arg_level was not passed
            False if arg_level was passed and lower than minimum level
        """

        if arg_level is None:
            return self.level
        elif arg_level.value >= self.level.value:
            return arg_level
        else:
            return False

    @staticmethod
    def create_msg(arg_level: LEVEL, arg_message: str) -> str:
        """
        Summary:
            ... creates the logging message
            "[Icon] [Date Time] [File (LineNr)] [arg_message]"

        Args:
            arg_level (LEVEL): logging level
            arg_message (str): payload of message

        Returns:
            str
        """
        space = "    "
        caller = inspect.stack()[2]
        filename = caller.filename
        lineno = caller.lineno
        funcname = caller.function
        file_info = f"\n{30*" "}-{filename}\\{funcname} ({lineno})-" if (
                arg_level == Logger.LEVEL.DEBUG or arg_level == Logger.LEVEL.ERROR) else ""

        log_message = (f"{arg_level.color}[{arg_level.char}]{Style.RESET_ALL}"
                       f"{space}"
                       f"{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
                       f"{space}"
                       f"{arg_message}"
                       f"{file_info}")
        return log_message

    @staticmethod
    def static_log(arg_message: str = "Message was not passed.",
                   arg_level: Logger.LEVEL = "Logger.LEVEL.DEBUG",
                   arg_file: str = None) -> bool:
        """
        Summary:
            ... logs the message without initializing the class

        Args:
            arg_file: output foile path (relative to project)
            arg_message (str): payload of message
            arg_level (LEVEL): logging level

        Returns:
            None
        """
        try:
            log_message = Logger.create_msg(arg_level, arg_message)
            print(log_message)

            if arg_file is not None:
                open(arg_file, "a").write(f"\n{log_message}")

            return True
        except:
            return False
###############################################################################

# FUNCTIONS
###############################################################################
# Function Header
###############################################################################

# SEQUENCE
###############################################################################
###############################################################################
