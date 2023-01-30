from utils import yaml
import logging
from pprint import pprint
import os
from pathlib import Path
import importlib

log = logging.getLogger("configMapper")

class ConfigMapper(object):
    def __init__(self, filename, configDir):
        """
        Initlizes the config off a tree of yamls.
        "/" holds global config
        "<subsystem>" holds configs for subsystems
        configDir points to folder with configs. Future work make it take a list and search.
        """
        self.configDir = configDir
        initialData = self.__loadFile(filename)
        log.debug("Intial data %s", initialData)
        self.subsystems = self.__convertToSubsystems(initialData, "/")


    def getSubsystem(self, subsystemName):
        """
        returns the complete config for specified subsystem or none if not
        found
        """
        # gives the values.

        if subsystemName not in self.subsystems:
            raise RuntimeError(f"Failed to find {subsystemName} in config")

        subsystem = self.subsystems[subsystemName]

        if "subsystem" not in subsystem:
            raise RuntimeError(f"Failed to find `subsystem` in {subsystemName}. Found {subsystem}")

        #load and create subsystem
        subClass = importClassFromModule(subsystem["subsystem"])


        if subClass == None:
            if subsystem["required"]:
                raise RuntimeError(f"Failed to create {subsystemName} from {subsystem['subsystem']} and is required")
            else:
                log.warn(f"Failed to create {subsystemName} from {subsystem['subsystem']} and is not required")
                return None

        return subClass(**subsystem)


    def getSubsystems(self):
        subsystems = list(self.subsystems.keys())
        return subsystems

    def getGroupDict(self, subsystem, groupName, name = None):
        """
        returns a dictonary with data from a subsystem matching the groups and
        if given then name.
        i.e.
        if you have a lifter with
        lifter.sensors.groups=sensor
        lifter.intakeMotors.groups=motors
        lifter.beltMotors.groups=motors
        calling getTypeDict("lifter", "motors")
        returns all motors in intakeMotors and beltMotors

        calling getTypeDict("lifter", "motors", "beltMotors")
        returns all motors in beltMotors

        calling getTypeDict("lifter", "sensor")
        returns all sensors
        """
        data = self.getSubsystem(subsystem)
        data =  self.__getGroups(data, groupName, name)
        if "groups" in data:
            data.pop("groups")

        return data

    def getTypesDict(self, subsystem, typeNames, name = None):
        """
        returns a dictonary with data from a subsystem matching the type(s) and
        Once a type is found in an entry it is not searched any deeper
        """
        if not isinstance(typeNames, list):
            typeNames = [typeNames]
        data = self.getSubsystem(subsystem)
        data = self.__getTypes(data, typeNames, name)
        return data

    def __getGroups(self, data, groupName, name):
        """
        internal call, recusivley search the data for entries with
        groups in "types" and if a name is given only types inside key with name
        """

        retVal = {}
        for key in data:
            if isinstance(data[key], dict):
                recusiveDict = self.__getGroups(data[key], groupName, name)
                retVal.update(recusiveDict)

            if isinstance(data[key], dict) and "groups" in data[key]:
                if name and not key == name:
                    continue

                if groupName in data[key]["groups"]:
                    retVal.update(data[key])
        return retVal

    def __getTypes(self, data, typeNames, name):
        """
        internal call, recusivley search the data for entries with
        typeName in ["types"] and if a name is given only types
        inside key with name
        """
        retVal = {}
        for key in data:
            if isinstance(data[key], dict):
                recusiveDict = self.__getTypes(data[key], typeNames, name)
                retVal.update(recusiveDict)

            if isinstance(data[key], dict) and "type" in data[key]:
                if name and not key == name:
                    continue

                if data[key]["type"] in typeNames:
                    retVal[key] = data[key]
        return retVal

    def __loadFile(self, filename):
        """
        Loads a yaml or yml file and returns the contents as dictionary
        """
        with open(self.configDir + os.path.sep + filename) as file:
            values = yaml.load(file, yaml.FullLoader)
            return values

    def __convertToSubsystems(self, inputData, defSubsystem):
        """
        Takes a dictionary and searchs for subsystem types to create leafs of a new tree.
        Loads files as "file" is encountered
        """
        print(inputData)

        if "subsystems" not in inputData:
            log.error("No Subsystems included in config")
        subsystems = inputData["subsystems"]
        processedData = {}

        for name, subsystem in subsystems.items():
            processedData[name] = {}
            #add required data defaults
            processedData[name]["required"] = True

            for key, value in subsystem.items():
                # if file, load file and walk
                if key == "file":
                    file = "subsystems" + os.sep + value
                    #TODO special handling for other types. Yaml only supproted type
                    if "type" in subsystem and not subsystem["type"] == "yaml":
                        log.error("Unknown file type fileType. Trying Yaml")
                    log.info("Loading %s into entry %s", file, key)
                    try:
                        data = self.__loadFile(file)
                    except FileNotFoundError as e:
                        log.error(f"Failed to find file {file} for subsystem {subsystem}")
                        data = {}
                        data["error"] = e
                    # Flatten the root node of newly loaded yaml file.
                    processedData[name].update(data)


                # if subsystem, walk subsystem
                #TODO add nested subsystems
                '''
                if "subsystem" in subsystem[key] and isinstance(subsystem[key], dict):
                    log.info("Walking subsystem")
                    # make a new subsystem
                    print(subsystem[key])
                    print(subsystem[key]["subsystem"])
                    processedData[subsystem[key]["subsystem"]] = self.__convertToSubsystems(inputData[key], inputData[key]["subsystem"])
                '''

                #skip special meanings
                if key == "type" and "file" in subsystem:
                    continue

                if key == "file":
                    continue

                # copy field over if no special processing
                processedData[name][key] = subsystem[key]


        return processedData


def importClassFromModule(name: str, base : str = "subsystems"):
    """
    Imports a class from a given module

    Args:
        name (str): Name of class in module.path.Class format
        base (str, optional): base module to load from. Defaults to "subsystems".

    Returns:
        _type_: Class or None
    """
    name = base + "." + name
    moduleName, className = name.rsplit(".", 1)

    log.info(f"Loading {name} as module {moduleName} and class {className}")

    module = importlib.import_module(moduleName)
    try:
        return getattr(module, className)
    except:
        log.warning(f"Failed to find {className} in {module}")
        return None


def findConfig(defaultConfig = "greenbot.yml", configPath = None) -> tuple[dict, str]:
    """
    Will determine the correct yml file for the robot.
    Please run 'echo (robotCfg.yml) > robotConfig' on the robot.
    This will tell the robot to use robotCfg file remove the () and use file name file.
    Files should be configs dir
    """
    if not configPath:
        configPath = os.path.dirname(__file__) + os.path.sep + ".." +os.path.sep + "configs" + os.path.sep
    home = str(Path.home()) + os.path.sep
    robotConfigFile = home + "robotConfig"

    if not os.path.isfile(robotConfigFile):
        log.error("Could not find %s. Using default", robotConfigFile)
        robotConfigFile = configPath + "default"
    try:
        file = open(robotConfigFile)
        configFileName = file.readline().strip()
        file.close()
        configFile = configPath + configFileName
        if os.path.isfile(configFile):
            log.info("Using %s config file", configFile)
            return configFileName, configPath
        log.error("No config? Can't find %s", configFile)
        log.error("Using default %s", defaultConfig)
    except Exception as e:
        log.error("Could not find %s", robotConfigFile)
        log.error(e)
        log.error("Please run `echo <robotcfg.yml> > ~/robotConfig` on the robot")
        log.error("Using default %s", defaultConfig)

    return defaultConfig, configPath


if __name__ == "__main__":
    mapper = ConfigMapper("doof.yml", "configs")
    print("Subsystem driveTrain:", mapper.getSubsystem("driveTrain"))

    print("driveTrain Motors")
    pprint(mapper.getGroupDict("driveTrain", "motors"))

    print("Shooter motors:")
    pprint(mapper.getGroupDict("shooter", "motors", "loaderMotors"))

    print("All motors:")
    mapper.getGroupDict("/", "motors")
    # print()
    pprint(mapper.getGroupDict("/", "motors"))

    print("CANTalonFXFollower motors:")
    data = mapper.getTypesDict("/", "CANTalonFXFollower")
    # print()
    pprint(data)

    compatTest = ["Dog", "all", "doof", "minibot", "DOOF"]
    for item in compatTest:
        compat = mapper.checkCompatibilty(item)
        print(f"{item} is {compat}")

    print("Subsystems: ", mapper.getSubsystems())
