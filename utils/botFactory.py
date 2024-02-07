import logging
import importlib
import re
import os
from pathlib import Path

# Easy Line Debugging
# https://github.com/gruns/icecream
from icecream import ic

# Imported just to define the object returned from the BotFactory
from robots.configBasedRobot import ConfigBasedCommandRobot


logging.basicConfig(level=logging.DEBUG)
log = logging.root.getChild("BotFactory")
log.setLevel(logging.DEBUG)


class BotFactory(object):
    robot_full_name = None  # nameBot"
    raw_name = None  # Whatever ws given to the Factory as a name
    robot_class_name = None  # NameBot

    def __init__(self, name: str = None) -> ConfigBasedCommandRobot:
        """BotFactory will get the configs and create the bot for the supplied name.
        If no name is supplied, then it will query the filesystem for ~/robotConfig and
        read the robot name from the file (yaml extension not necessary) Bot is assumed at the end of the name.
        Eventually this method should be able to query the RoboRio itself for the robot name but this still still unimplmented."

        Returns:
            ConfigBasedCommandRobot: Instance of the robot like greenBot, dumboBot, teapotBot, labBot, etc
        """
        botName = None
        # User supplied the name so use that
        if name is not None:
            log.info(f"Using supplied name {name} for bot")
            botName = name
        # We need to figure out which bot to create
        else:
            log.info("Determining name of bot")
            # Robo Rio Query
            # TODO what is the Pythonic way of doing this???
            try:
                ic()
                botName = self._get_name_from_robo_rio()
            except LookupError as e:
                ic(e)
                try:
                    botName = self._get_name_from_config_file()
                except LookupError as e:
                    ic(e)
                    raise LookupError(
                        f"----> Unable to determine bot name from anything. Please look at README.md and READ on how to properly define your config file {e}"
                    )

        # Remove any extension from the botName as this will be computed
        ic(f"before normalize {botName}")
        botName = self._normalize_bot_name(botName)
        ic(f"after normalize {botName}")

        # Validate the bot name and match it to a yaml file, verify the config and python exist for the bot too
        try:
            self._validate_bot_name_for_yaml_file(botName)
            self._validate_bot_config_exists(botName)
            self._validate_bot_python_exists(botName)
        except Exception as e:
            raise AssertionError(
                "The " + botName + " could not be found or had errors. error=" + e
            )

        # If we made it here, we know our botName is valid and the python for the bot exists and the config for the bot exists

    def _normalize_bot_name(self, robotName: str) -> str:
        """Takes in a name of <robot name>Bot.py, <robot name>, <robot name>Bot <robot name>Bot.yml/yaml and
        will normalize to just <robot name> and then assign to internal vars for future use

        Args:
            name (str): The name of the robot in the form of <robot name> or <robot name>Bot.yml/yaml

        Returns:
            str: The normalize name of the robot in the form of <robot name> ie dumbo or lab
        """
        pos = robotName.find("Bot")
        ic(f"Bot={pos}")
        # If we have the format of <robot name> then just take the robotName in it's entirety
        if pos == -1:
            name = robotName
        else:
            name = robotName[:pos]
        ic(f"name={name}")

        self.raw_name = robotName
        self.name = name
        self.robot_full_name = f"{name}Bot"
        self.robot_class_name = f"{name.capitalize()}Bot"
        self.robot_module_name = f"robots.{self.robot_full_name}"

        return self.name

    def _validate_bot_name_for_yaml_file(self, filename: str) -> bool:
        """Checks for <name>Bot.yaml or <name>Bot.yml

        Args:
            filename (str): The name of the file to check for config

        Returns:
            bool: True if the file matches our desired syntax otherwise False
        """
        ic(f"validateBotNameForYamlFile before {filename}")
        filename = filename + "Bot.yml"
        ic(f"validateBotNameForYamlFile after {filename}")
        pattern = r"^\S+Bot\.(yml|yaml)$"
        return bool(re.match(pattern, filename))

    def _validate_bot_config_exists(self, filename: str) -> bool:
        ic(f"validateBotConfigExist before {filename}")
        filename = filename + "Bot.yml"
        ic(f"validateBotNameForYamlFile after {filename}")
        ic(filename)
        configPath = (
            os.path.dirname(__file__)
            + os.path.sep
            + ".."
            + os.path.sep
            + "configs"
            + os.path.sep
            + filename
        )
        ic(configPath)

        if not os.path.isfile(configPath):
            log.error(f"Could not find {configPath}")
            return False

        return True

    def _validate_bot_python_exists(self, botname: str) -> bool:
        """Checks to see if the python file exists for the supplied bot name

        Args:
            filename (str): The name of the bot to check for the python file

        Returns:
            bool: True if the python file for the bot was found or False otherwies
        """
        ic(f"validateBotPythonExist before {botname}")
        filename = botname + "Bot.py"
        ic(f"validateBotPythonFile after {filename}")
        ic(filename)
        configPath = (
            os.path.dirname(__file__)
            + os.path.sep
            + ".."
            + os.path.sep
            + "robots"
            + os.path.sep
            + filename
        )
        ic(configPath)

        if not os.path.isfile(configPath):
            log.error(f"Could not find {configPath}")
            return False

        return True

    def _get_name_from_config_file(self) -> str:
        """Locates a config file in ~/robotConfig and if found, will read the name of bot

        Raises:
            LookupError: If the fully qualified robotConfig file can't be opened
            LookupError: If the robotConfig can't be read

        Returns:
            str: The stripped contents of the config file
        """
        ic()
        # Need to supply a sane value to findConfig in the form of <botname>Bot.yml

        home = str(Path.home()) + os.path.sep
        robotConfigFile = home + "robotConfig"

        if not os.path.isfile(robotConfigFile):
            raise LookupError(
                f"Unable to open configFile.  {robotConfigFile} not found."
            )

        # We can find the file so lets open it and attempt to determine the bot name
        with open(robotConfigFile) as file:
            name = file.read()
            if name is None:
                raise LookupError(
                    f"Unable to determine name from configFile.  {robotConfigFile} is empty."
                )

            # Remove any leading and trailing whitespace in the file
            name = name.strip()
            ic(name)

            return name

    def _get_name_from_robo_rio(self) -> str:
        """Gets the robot name from the roboRio

        Raises:
            LookupError: If name can't be determined raise a lookup error

        Returns:
            str: name of the bot stored in the roboRio
        """
        ic()
        raise LookupError("Unable to determine name from roboRio. NOT IMPLEMENTED")

    def get_robot_name(self) -> str:
        """Determine the name of the robot from either the config file or the RoboRio memory

        Returns:
            str: name of the robot like green, dumbo, teapot, lab, etc
        """
        return "greenbot"

    def get_robot(self) -> ConfigBasedCommandRobot:
        # The name should be greenBot or dumboBot (no yaml/yml/py)
        ic(f"getRobotFromName {self.name}")
        # TODO Need an interator that does this to all bots
        # from robots.name import selfDumbo
        # robots.dumbo
        lib = f"robots.{self.robot_full_name}"
        ic(lib)
        # module = importlib.import_module(lib)
        module = None
        try:
            module = importlib.import_module(self.robot_module_name)
        except Exception as e:
            err_msg = f"Unable to import module {self.robot_module_name} please ensure that your ~/robotConfig exists, and contents are correct. robot name from config file={self.raw_name} Exception: {e}"
            log.error(err_msg)
            raise ImportError(err_msg)
        ic(module)
        # Dynamically get the robot_class_name (ie DumboBot,LabBot, etc) and use getattr() to call the class in the
        # imported module
        obj = None
        try:
            obj = getattr(module, self.robot_class_name)()
        except Exception as e:
            err_msg = f"Unable to get attributes on {module}.{self.robot_class_name} please ensure that your ~/robotConfig exists, and contents are correct. robot name={self.raw_name} Exception: {e}"
            log.error(err_msg)
            raise Exception(err_msg)

        # return getattr(module, self.robot_class_name)()
        return obj


def get_bot(name: str) -> ConfigBasedCommandRobot:
    """getBot will get the configs and create the bot for the supplied name.
    If no name is supplied, then it will query the filesystem for ~/robotConfig and
    read the robot name from the file (yaml extension not necessary) Bot is assumed at the end of the name.
    Eventually this method should be able to query the RoboRio itself for the robot name but this still still unimplmented."

        Returns:
            ConfigBasedCommandRobot: Instance of a name of the robot like green, dumbo, teapot, lab, etc
    """
    ic(name)
    return BotFactory(name).get_robot()
