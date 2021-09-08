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


from domoTools import get_widget_attributes, write_attribute_device, create_widget


class BasePlugin:

    def __init__(self):
        self.count = 0

    def onStart(self):
        Domoticz.Log("onStart...")

        if not domoticzex:
            unit = len(Devices)+1
        else:
            unit = 1

        deviceid = len(Devices)+1
        create_widget(self, Devices, deviceid, unit)

        # Initialise Value
        attribute_dict = {
            "nValue": 0, 
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

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called for connection: '" + Connection.Name + "'")

    def onHeartbeat(self):
        Domoticz.Log("Heartbeating... ")

        if not domoticzex:
            # Legacy
            for x in Devices:
                attribute_dict = {
                    'nValue': 0,
                    'sValue': str(int(get_widget_attributes(self, Devices, None, x, "sValue")["sValue"]) + 1)
                }
                write_attribute_device(self, Devices, None, x, attribute_dict)

        else:

            for x in Devices:
                for y in Devices[x].Units:
                    Domoticz.Log(
                        "%s:%s" % (Devices[x].Units[y].nValue, Devices[x].Units[y].sValue)
                    )

                    attribute_dict = {
                        'nValue': 0,
                        'sValue': str(int(get_widget_attributes(self, Devices, x, y, "sValue")["sValue"]) + 1)
                    }

                    write_attribute_device(self, Devices, x, y, attribute_dict)

    def onCommand_Ex(self, DeviceID, Unit, Command, Level, Color):
        Domoticz.Log("onCommand... Ex")

    def onCommand_Legacy(self, Unit, Command, Level, Color):
        Domoticz.Log("onCommand... Legacy")

    def onDeviceRemoved(self, DeviceID, Unit):
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
        _plugin.onDeviceRemoved(DeviceID, Unit)

    def onCommand(Unit, Command, Level, Hue):
        global _plugin
        _plugin.onCommand(DeviceID, Unit, Command, Level, Hue)

else:
    # Legacy
    def onDeviceRemoved(Unit):
        global _plugin
        _plugin.onDeviceRemoved(Unit)

    def onCommand(Unit, Command, Level, Hue):
        global _plugin
        _plugin.onCommand(Unit, Command, Level, Hue)


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
