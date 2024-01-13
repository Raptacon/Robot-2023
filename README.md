![Raptacon (Team 3200) CI Pipeline](https://github.com/Raptacon/Robot-2023/workflows/Raptacon%20(Team%203200)%20CI%20Pipeline/badge.svg)

![Build link](https://github.com/Raptacon/Robot-2023/actions/workflows/robot_ci.yml)

## Welcome to Robot 2023

Please take a look at the [wiki](https://github.com/Raptacon/Robot-2023/wiki) for the most up to date documenation

Also make sure to check out the [Kanban board](https://github.com/Raptacon/Robot-2023/projects/1)
test

# Installation

According to [Robotpy](https://robotpy.readthedocs.io/en/stable/faq.html#what-version-of-python-do-robotpy-projects-use) the "RobotPy WPILib on the roboRIO uses the latest version of Python 3 at kickoff". The version of Python for 2023 you want to install is [3.11.1](https://www.python.org/downloads/release/python-3111/)

There is a general setup that is needed for each OS before you can build the code. Please look at the ![FRC Zero to Robot](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/frc-game-tools.html) to get the initial setup for NI and then ![WPILib](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/wpilib-setup.html) which has an amazing need to mount an ISO this year so make sure to pay attention to the "Mount" instructions. Once you have those completed in theory you can clone our code and type make. Make sure to see the OS specific instructions below.

## OSX Users

If you're using OSX you probably want to install python from python.org. Brew python has problems with Tk (simulator) where the widgets won't render correctly.

## Windows Users

### Initial Installation

The easiest way to get things working is to install the package manager ![Chocolatey](https://chocolatey.org/) by going ![here](https://chocolatey.org/install) and going to Step 2 and following the directions OR just opening a PowerShell windows as Admin (yes...be careful) and doing:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```
once you have that completed you may install the Make system for windows by doing
```powershell
choco install make
```
after make has been installed, you can simply just go to the root of the Robot-2023 source and type in ```make``` and it should create a venv and install the required packages for building the robot code.
# Use

```powershell
#Windows setup from cmd
python -m venv raptaconVenv
raptaconVenv\Scripts\activate.bat
pip install -r requirements.txt
```

# Hardware for the Robot

## roboRio (Gray box)

There are now two types of roboRIOs. The v2 can be identified by having the microSD card reader next to the large USB header on the top of the roboRIO. Otherwise the RIOs look the same. Identify your RIO version first before going to the v1 or v2 section to program the image.

Once you DO install the latest image, PLEASE LABEL the RIO with the current date and image version. This will make it easy to identify when the RIO was last updated. 

### roboRio v1

To install the roboRIO image for a v1 RIO look at the docs [here](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/imaging-your-roborio.html#imaging-your-roborio-1).

Once you DO install the latest image, PLEASE LABEL the RIO with the current date and image version. This will make it easy to identify when the RIO was last updated. 

### roboRio v2

To install the roboRIO image for a v1 RIO look at the docs [here](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/roborio2-imaging.html#imaging-your-roborio-2).

Once you DO install the latest image, PLEASE LABEL the RIO with the current date and image version. This will make it easy to identify when the RIO was last updated.

## Radio Firmware (white box)

See this [doc](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/radio-programming.html) on how to update/program the radio. Be sure to label the radio with the new SSID and firmware version!

Once you install the firmware, PLEASE LABEL the radio with the current date, firmware version AND SSID. This will make it easy to identify when the RIO was last updated and how to connect to the bot.

## Motors / Motor Controllers

Once you install the firmware, PLEASE LABEL the radio with the current date, firmware version AND SSID. This will make it easy to identify when the RIO was last updated and how to connect to the bot.

TODO more documentation here around motors, controllers and how to update them.

# Configuration

Ensure that you have a robotConfig definied in your home directory: 

If you DON'T have this file defined, you may not be using the correct robot config and end up with the sim/bot crashing with something like
```python
Traceback (most recent call last):
  File "/Users/chirsch/src/raptacon/2023/Robot-2023.deleteme/.venv_osx/lib/python3.11/site-packages/wpilib/_impl/start.py", line 163, in _start
    self.robot.startCompetition()
  File "/Users/chirsch/src/raptacon/2023/Robot-2023.deleteme/robot.py", line 37, in robotInit
    self.container = Dumbo()
                     ^^^^^^^
  File "/Users/chirsch/src/raptacon/2023/Robot-2023.deleteme/robots/breadboxBot.py", line 20, in __init__
    self.robot_arm = self.subsystems["arm"]
```

For Linux/OSX 
``` bash
echo breadboxBot.yml > ~/robotConfig
```

For Windows create a file called robotConfig in your home directory with the contents of
breadboxBot.yml or greenBot.yml etc

```powershell
echo breadboxBot.yml > ~/robotConfig
```
=======


# Enable Power shell
Power shell does not allow sccripts on windows now by default

* run power shell as admin
* run `set-executionpolicy remotesigned`
* Select A when prompted
>>>>>>> ad7e0ef862389d91723a336a9e63fe0e7932085f

