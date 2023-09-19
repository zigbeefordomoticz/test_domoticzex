"""
<plugin key="test-domoticzex" name="Test DomoticzEx" author="pipiche" version="1.0">
    <description>
        Testing Configure
    </description>
    <params>
        <param field="Mode6" label="Debug" width="150px">
            <options>
                <option label="None" value="0"  default="true" />
                <option label="Python Only" value="2"/>
                <option label="Basic Debugging" value="62"/>
                <option label="Basic+Messages" value="126"/>
                <option label="Connections Only" value="16"/>
                <option label="Connections+Python" value="18"/>
                <option label="Connections+Queue" value="144"/>
                <option label="All" value="-1"/>
            </options>
        </param>
    </params>
</plugin>
"""


try:
    import DomoticzEx as Domoticz
    domoticzex = True

except:
    import Domoticz
    domoticzex = False

try:
    if domoticzex:
        from DomoticzEx import Devices, Images, Parameters, Settings
    else:
        from Domoticz import Devices, Images, Parameters, Settings
except ImportError:
    pass


from domoTools import get_widget_attributes, write_attribute_device, create_widget, set_timedout_device
import random


class BasePlugin:

    def __init__(self):
        self.count = 0

    def onStart(self):
        Domoticz.Log("onStart...")

        if not domoticzex:
            unit = len(Devices)+1
            Domoticz.Log("old dz interface")
        else:
            unit = 1
            Domoticz.Log("new dz interface EX")

        deviceid = len(Devices)+1
        create_widget(self, Devices, deviceid, unit)

        # Initialise Value
        attribute_dict = {
            "nValue": 2, 
            "sValue": '1'
        }
        write_attribute_device(self, Devices, str(deviceid), unit, attribute_dict)

    def onStop(self):
        Domoticz.Debug("onStop...")

    def onConnect(self, Connection, Status, Description):
        if Status == 0:
            Domoticz.Log("Successful connect to: " + Connection.Address)
        else:
            Domoticz.Log(
                "Failed to connect to: "
                + Connection.Address
                + ", Description: "
                + Description
            )

    def onDisconnect( self, Connection):
        pass
    
    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called for connection: '" + Connection.Name + "'")

    def onHeartbeat(self):
        Domoticz.Log("Heartbeating... ")

        if not domoticzex:
            # Legacy
            for x in Devices:
                prev_value = get_widget_attributes(self, Devices, None, x, "sValue")["sValue"]
                if prev_value == '':
                    prev_value = '0'
                attribute_dict = {
                    'nValue': 2,
                    'sValue': str(min(100,int(prev_value) + 1)),
                    'Battery': random.randint(0,100),
                    'SignalLevel' : random.randint(0,12)
                }
                write_attribute_device(self, Devices, None, x, attribute_dict)

        else:

            for x in Devices:
                #for y in Devices[x].Units:
                y = 1
                if random.randint(0,4) == 2:
                    set_timedout_device(self, Devices, x, y, timedout=True)
                else:
                    set_timedout_device(self, Devices, x, y, timedout=False)
                
                Domoticz.Log(
                    "%s:%s" % (Devices[x].Units[y].nValue, Devices[x].Units[y].sValue)
                )
                prev_value = get_widget_attributes(self, Devices,  x, y, "sValue")['sValue']
                if prev_value == '':
                    prev_value = '0'

                attribute_dict = {
                    'nValue': 2,
                    'sValue': str(min(100,int(prev_value) + 1)),
                    'Battery': random.randint(0,100),
                    'SignalLevel' : random.randint(0,12)
                }

                write_attribute_device(self, Devices, x, y, attribute_dict)

    def onCommand_Ex(self, DeviceID, Unit, Command, Level, Color):
        Domoticz.Log("onCommand... Ex: DeviceID:%s, Unit:%s, Command:%s,  Level:%s, Color:%s" %(DeviceID, Unit, Command, Level, Color))

    def onCommand_Legacy(self, Unit, Command, Level, Color):
        Domoticz.Log("onCommand... Legacy: Unit:%s, Command:%s,  Level:%s, Color:%s" %(Unit, Command, Level, Color))

    def onDeviceRemoved_Ex(self, DeviceID, Unit):
        Domoticz.Log("onDeviceRemoved... Ex")

    def onDeviceRemoved_Legacy(self, Unit):
        Domoticz.Log("onDeviceRemoved... Legacy")


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


if domoticzex:
    # Exented
    def onDeviceRemoved(DeviceID, Unit):
        global _plugin
        _plugin.onDeviceRemoved_Ex(DeviceID, Unit)

    def onCommand(DeviceID, Unit, Command, Level, Hue):
        global _plugin
        _plugin.onCommand_Ex(DeviceID, Unit, Command, Level, Hue)

else:
    # Legacy
    def onDeviceRemoved(Unit):
        global _plugin
        _plugin.onDeviceRemoved_Legacy(Unit)

    def onCommand(Unit, Command, Level, Hue):
        global _plugin
        _plugin.onCommand_Legacy(Unit, Command, Level, Hue)


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
