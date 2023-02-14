import logging
from . import motorHelper
#TODO Delet me
logging.basicConfig(level=logging.DEBUG)

log = logging.root.getChild("HardwareFactory")
#log.setLevel(logging.DEBUG)

class HardwareFactory(object):
    '''
    Hardware factory for instantiating hardware componets in a config
    '''
    def __new__(cls):
        if not hasattr(cls, "instance"):
            log.debug("New instance created")
            cls.instance = super(HardwareFactory, cls).__new__(cls)
        else:
            log.debug("HardwareFactory alread created returning singleton")
        return cls.instance

    def __init__(self):
        log.debug("New HardwareFactory")
        self.config = {}
        self.componets = {}
    def addConfig(self, subsystem: str, config: dict):
        """
        Adds a new config. Replaces or updates exsisting componets.
        """
        log.debug(f"Adding config {subsystem}.{config}")

        if subsystem == None:
            log.debug("Adding to root")
            subsystem = "root"

        #TODO add logic to check if a HW instance was alread created. If so need to log a warning. Crashing for now
        if subsystem in self.config:
            assert False, "Subsystem updatinng and saftey not done"
        self.config[subsystem] = config

        for name, value in self.config[subsystem].items():
            #create the hardware componets at config time to catch errors early
            if isinstance(value, dict) and "type" in value:
                log.debug(f"Creating {subsystem}.{name} type {value['type']}")
                self.createHardwareComponet(subsystem, name, value)
            else:
                log.info(f"{subsystem}.{name} is not hardware")
        
    def getConfig(self, subsystem: str, name: str):
        """
        returns the config for a given subsystem / name.
        If subsystem = None, searchs for the first name that matches.
        Returns None on failure to find config
        """
        if not subsystem:
            for subsystem in self.config:
                if name in self.config[subsystem]:
                    return self.config[subsystem]

        elif subsystem in self.config:
            if name in self.config[subsystem]:
                return self.config[subsystem][name]
        log.info(f"getConfig({subsystem}, {name}) failed to find config")
        return None

    def getHardwareComponet(self, subsystem: str, name: str):
        """
        Returns an instantiated componet. Return None if does not exsist
        """
        if subsystem == None:
            subsystem = "any"
        log.debug(f"Geting componet {subsystem}.{name}")

        componet = None
        for ss in self.componets:
            if ss == subsystem or subsystem == "any":
                if name in self.componets[ss]:
                    componet = self.componets[ss][name]
                    log.debug(f"Got {componet} from {ss}.{name}")
                    return componet
        
        log.debug(f"{subsystem}.{name} not created. Creating")
        if self.createHardwareComponet(subsystem, name):
            return self.componets[name]
        else:
            log.error(f"Failed to find componet {name}")
            return None

    def createHardwareComponet(self, subsystem: str, name: str, config: dict = None):
        """
            Creates a componet from a dictory.
        """
        if not config:
            config = self.getConfig(subsystem, name)

        config = config.copy()
        subtype = config["type"].split(".")[0]
        compType = config["type"].split(".")[1]
        log.info(f"Creating componet {subsystem}.{name} as {subtype}.{compType}")

        #clean up componets
        if not subsystem in self.componets:
            self.componets[subsystem] = {}
        if not name in self.componets[subsystem]:
            self.componets[subsystem][name] = {}

        #use short name without subtype
        config["type"] = compType
        componet = None
        match subtype:
            case "motor":
                componet = motorHelper.createMotor(config)
            case "sensor":
                log.warning("TODO create sensor factory")
            case _:
                log.error(f"{subtype} is not a valid subtype. Support for matching any factory not done")
        if componet:
            #add names for later use
            self.componets[subsystem][name] = componet
        elif "required" in config and config["required"]:
            raise RuntimeError(f"Failed to create {subsystem}.{name} {subtype}.{compType} and is required")

        return componet






def getHardwareFactory() -> HardwareFactory:
    return HardwareFactory()
