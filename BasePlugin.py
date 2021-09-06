import Domoticz

class BasePlugin:

    def __init__( self ):
        self.count = 0
 
    def onStart(self):
        Domoticz.Debug("onStart...Legacy")
        pass
                
    def onConnect(self, Connection, Status, Description):
        if (Status == 0):
            Domoticz.Log("Successful connect to: "+Connection.Address)
        else:
            Domoticz.Log("Failed to connect to: "+Connection.Address+", Description: "+Description)

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called for connection: '"+Connection.Name+"'")

    def onHeartbeat(self):
        Domoticz.Debug("Heartbeating...Legacy")

