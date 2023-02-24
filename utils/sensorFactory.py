"""
Contains helpers to create various sensor types
"""

from wpilib import DigitalInput as di
import logging
import navx
import wpilib
import traceback

log = logging.getLogger("SensorFactory")

def gyroFactory(descp):
    """
    Creates gyros from a gyro descp
    """
    try:
        if "navx" == descp["type"]:
            """
            Supports spi and i2c with default values. More can be added as needed.
            """
            method = descp["method"]
            if method == "spi":
                return navx.AHRS.create_spi()
            if method == "i2c":
                return navx.AHRS.create_i2c()
            #invalid method, thorw a fit
            raise ValueError(f"{method} method is invalid")

    except Exception as e:
        logging.error("Failed to create gyro for %s. Error %s",descp, e)
    return None

def breaksensorFactory(descp):
    """
    Creates break sensors from a break sensor descp
    """
    try:
        if "RIODigitalIn" in descp["type"]:
            return di(descp["channel"])

    except Exception as e:
        logging.error("Failed to create IR Break sensor for %s. Error %s", descp, e)
    return None


def dutyCycleEncoderFactory(config: dict) -> wpilib.DutyCycleEncoder:
    """
        config format:
        type: "sensor.wpilib.DutyCycleEncoder"
        channel: digital IO channel (i.e. 0). required
        offset: sensor offset in units (i.e. 180.0 for 180 degrees). default 0.0
        unitsPerRotation: units per rotation (i.e 360.0 for degrees). default 1.0
        minDutyCycle: see setDutyCycleRange. default 0
        maxDutyCycle: see setDutyCycleRange. default 1.0
    """
    channel = config["channel"] #raise value error if not present
    offset = config.get("offset", 0.0)
    upr = config.get("unitsPerRotation", 1.0)
    minDuty = config.get("minDutyCycle", 0.0)
    maxDuty = config.get("maxDutyCYcle", 1.0)
    log.info(f"Creating DutyCycleEncoder")
    log.info(f"Channel {channel}, UnitsPerRotation {upr}, offset {offset}, minDutyCycle {minDuty} maxDutyCycle {maxDuty}")
    encoder = wpilib.DutyCycleEncoder(config["channel"])
    encoder.setDistancePerRotation(upr)
    encoder.setPositionOffset(offset)
    encoder.setDutyCycleRange(minDuty, maxDuty)
    return encoder

def create(compType: str, config: dict):
    try:
        match compType:
            case "wpilib.DutyCycleEncoder":
                log.info("Creating DutyCycleEndoer")
                return dutyCycleEncoderFactory(config)
            case _:
                log.error(f"Unsupported Sensor {compType} for {config}")
    except Exception as e:
        log.error(f"Failed to create sensor {compType} for {config}")
        log.error(f"Error caught: {e}")
        traceback.print_exception(e)

        if config.get("required", False):
            raise RuntimeError(f"Failed to create required component {compType} for {config}")
    
    return None
