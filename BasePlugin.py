import Domoticz


class BasePlugin:
    def __init__(self):
        self.count = 0

    def onStart(self, Devices):
        Domoticz.Log("onStart...Legacy")
        Domoticz.Debug(-1)

        # if len(Devices) > 0:
        #    for x in list(Devices):
        #        Devices[x].Delete()

        unit = len(Devices) + 1
        Domoticz.Device(Name="Counter_%s" % unit, Unit=unit, Type=113).Create()
        Domoticz.Log("Created device: %s" % Devices[unit].Name)
        Devices[ unit ].Update(nValue=0, sValue="0")

    def onStop(self):
        Domoticz.Log("onStop...Legacy")

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

    def onHeartbeat(self, Devices):
        Domoticz.Log("Heartbeating...Legacy")

        for x in Devices:
            Domoticz.Log("%s:%s" % (Devices[x].nValue, Devices[x].sValue))
            sValue = "%s" % (int(Devices[x].sValue) + 1)
            Devices[x].Update(nValue=0, sValue=sValue)

    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Log("onCommand... Legacy")

    def onDeviceRemoved(self, Unit):
        Domoticz.Log("onDeviceRemoved... Legacy")
