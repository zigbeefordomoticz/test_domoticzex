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
    from BasePluginEx import BasePlugin

    domoticzex = True

except:
    import Domoticz

    domoticzex = False
    from BasePlugin import BasePlugin

domoticzex = False


global _plugin
if domoticzex:
    _plugin = BasePluginEx()
else:
    _plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart(Devices)


def onStop():
    global _plugin
    _plugin.onStop()


if domoticzex:

    def onDeviceRemoved(DeviceID, Unit):
        global _plugin
        _plugin.onDeviceRemoved(DeviceID, Unit)

    def onCommand(Unit, Command, Level, Hue):
        global _plugin
        _plugin.onCommand(DeviceID, Unit, Command, Level, Hue)


else:

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
    _plugin.onHeartbeat(Devices)
