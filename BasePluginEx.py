import DomoticzEx as Domoticz


class BasePlugin:
    def __init__(self):
        self.count = 0

    def onStart(self, Devices):
        Domoticz.Log("onStart...Ex")

        for x in list(Devices):
            for y in list(Devices[x].Units):
                Domoticz.Log(
                    "Loading Devices[%s].Units[%s]: %s"
                    % (x, y, Devices[x].Units[y].Name)
                )
                deviceid = len(Devices)
                Domoticz.Unit(
                    Name="Counter_%s" % deviceid,
                    DeviceID=str(deviceid),
                    Unit=1,
                    TypeName="Counter",
                ).Create()
                Domoticz.Log("Created device: " + Devices[str(deviceid)].Units[1].Name)

                Devices[str(deviceid)].Units[1].nValue = 0
                Devices[str(deviceid)].Units[1].sValue = "0"
                Devices[str(deviceid)].Units[1].Update()

    def onStop(self):
        Domoticz.Debug("onStop...Ex")

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
        Domoticz.Log("Heartbeating... Ex")
        for x in Devices:
            for y in Devices[x].Units:
                Domoticz.Log(
                    "%s:%s" % (Devices[x].Units[y].nValue, Devices[x].Units[y].sValue)
                )
                Devices[x].Units[y].nValue = 0
                Devices[x].Units[y].sValue = "%s" % (
                    int(Devices[x].Units[y].sValue) + 1
                )
                Devices[x].Units[y].Update(Log=True)

    def onCommand(self, DeviceID, Unit, Command, Level, Color):
        Domoticz.Log("onCommand... Ex")

    def onDeviceRemoved(self, DeviceID, Unit):
        Domoticz.Log("onDeviceRemoved... Ex")
