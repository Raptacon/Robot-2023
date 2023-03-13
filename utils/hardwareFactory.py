import logging
from . import motorHelper
from . import sensorFactory
#TODO Delet me
logging.basicConfig(level=logging.DEBUG)

log = logging.root.getChild("HardwareFactory")
#log.setLevel(logging.DEBUG)

class HardwareFactory(object):
    '''
    Hardware factory for instantiating hardware components in a config
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
        self.components = {}
    def addConfig(self, subsystem: str, config: dict):
        """
        Adds a new config. Replaces or updates exsisting components.
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
            #create the hardware components at config time to catch errors early
            if isinstance(value, dict) and "type" in value:
                log.debug(f"Creating {subsystem}.{name} type {value['type']}")
                self.createHardwareComponent(subsystem, name, value)
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

    def getHardwareComponent(self, subsystem: str, name: str):
        """
        Returns an instantiated component. Return None if does not exsist
        """
        if subsystem == None:
            subsystem = "any"
        log.debug(f"Geting component {subsystem}.{name}")

        component = None
        for ss in self.components:
            if ss == subsystem or subsystem == "any":
                if name in self.components[ss]:
                    component = self.components[ss][name]
                    log.debug(f"Got {component} from {ss}.{name}")
                    return component
        
        log.debug(f"{subsystem}.{name} not created. Creating")
        if self.createHardwareComponent(subsystem, name):
            log.error("Not finished")
            return self.components[name]
        else:
            log.error(f"Failed to find component {name}")
            return None

    def createHardwareComponent(self, subsystem: str, name: str, config: dict = None):
        """
            Creates a component from a dictory.
        """

        if not config:
            config = self.getConfig(subsystem, name)

        config = config.copy()
        try:
            subtype = config["type"].split(".", 1)[0]
            compType = config["type"].split(".", 1)[1]
            log.info(f"Creating component {subsystem}.{name} as {subtype}.{compType}")
        except Exception as e:
            log.error(f"**** {config['type']} is not in the format subtype.type. i.e. motor.SparkMax) for {subsystem} {name}")
            log.debug(e)
            if "required" in config and config["required"]:
                raise RuntimeError(f"Failed to create required hardware {config['type']} in {subsystem} {name}")
            
            return None

        #clean up components
        if not subsystem in self.components:
            self.components[subsystem] = {}
        if not name in self.components[subsystem]:
            self.components[subsystem][name] = {}

        #use short name without subtype
        config["type"] = compType
        component = None
        match subtype:
            case "motor":
                component = motorHelper.createMotor(config)
            case "sensor":
                component = sensorFactory.create(compType, config)
            case _:
                log.error(f"{subtype} is not a valid subtype. Support for matching any factory not done")
        if component:
            #add names for later use
            self.components[subsystem][name] = component
        elif "required" in config and config["required"]:
            raise RuntimeError(f"Failed to create {subsystem}.{name} {subtype}.{compType} and is required")

        return component






def getHardwareFactory() -> HardwareFactory:
    return HardwareFactory()
