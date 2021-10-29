# DomoticzEx implementation study in Domoticz-Zigate plugin

## Overview

Domoticz has recently enhanced the Python Framework to remove the 255 units ( Domoticz Devices) limitations. In addition the new framework DomoticzEx provided much more functionnality than the legacy framework Domoticz

The objective is now to understand and study the best way to move the plugin from the legacy framework to the new extended one.

## Objective

The main objective is a 100% upward compatibility. This mean a user who have created all of his Domoticz Devices under the legacy will continue to work with the new implementation.
It is not our objective to achieve downward compatibility. In other words, a user whom have created Domoticz Devices with the new version of the plugin using the Extended Framework, won't be able to go down.

## Principle

The principle is create an abstract layer above the Python framework. It will then act as a middleware to abstract the way to access to the Domoticz devices.

## Domoticz Devices Acess

* DeviceID
* TimedOut
* Units

### Domoticz Devices > Unit

`Domoticz.Log(Devices["123456"].Units[2].Name)`

* Name
* nValue
* sValue
* SignalLevel
* BatteryLevel
* Image
* Type
* SubType
* Switchtype
* Used
* Options
* LastLevel
* LastUpdate
* Description
* Color
* Adjustment &nbsp;&nbsp;&nbsp;&nbsp;    __new in the DomoticzEx__ &nbsp;&nbsp;(temperature...)
* Multiplier &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   __new in the DomoticzEx__
* Parent    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    __new in the DomoticzEx__


## Abstract methods

Those methods will be called independantly of the Framework.

| Method                 | Description                                        |
| ---------------------- | -------------------------------------------------- |
| get_widget_Functions   | return the value of the Function given in argument |
| set_timedout_device    | set/unset the Device TimedOut                      |
| set_lastseen_device    | set the Device lastseen information                |
| write_Function_device  | update the nValue:sValue and option of SignalLevel and BatteryLevel |

## Expected impact in today's plugin

| Module        | impacts |
| ------        | -------------------------------------------- |
| Modules/domoTools.py  | all                                          |
| Modules/domoMaj.py    | all                                          |
| Modules/domoCreate.py | all                                          |
| Modules/command.py    | all                                          |
| Modules/database.py   | checkDevices2LOD, checkListOfDevice2Devices  |
| Classes/AdminWidgets.py | to be assess |
| Modules/heartbeat.py |to be assess |
| Modules/input.py |to be assess |
| Modules/pairingProcess.py |to be assess |
| Modules/tools.py |to be assess |

## references

* [Extended Plugin Framework documentation](https://www.domoticz.com/wiki/Developing_a_Python_plugin#Extended_Plugin_Framework)
