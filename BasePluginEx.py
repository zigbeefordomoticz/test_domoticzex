import DomoticzEx as Domoticz

class BasePlugin:

    def __init__( self ):
        self.count = 0
 
    def onStart(self, Devices):
        Domoticz.Log("onStart...Ex")

    def onStop(self):
        Domoticz.Debug("onStop...Ex")
                
    def onConnect(self, Connection, Status, Description):
        if (Status == 0):
            Domoticz.Log("Successful connect to: "+Connection.Address)
        else:
            Domoticz.Log("Failed to connect to: "+Connection.Address+", Description: "+Description)

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called for connection: '"+Connection.Name+"'")

    def onHeartbeat(self, Devices):
        Domoticz.Log("Heartbeating... Ex")

    def onCommand( self, DeviceID, Unit, Command, Level, Color ):
        Domoticz.Log("onCommand... Ex")

    def onDeviceRemoved( self, DeviceID, Unit ):
        Domoticz.Log("onDeviceRemoved... Ex")

