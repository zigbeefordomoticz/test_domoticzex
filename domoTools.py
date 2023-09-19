try:
    import DomoticzEx as Domoticz
    domoticzex = True
except Exception:
    import Domoticz
    domoticzex = False

LIST_OF_WIDGET_ATTRIBUTES = (
    "nValue",
    "sValue",
    "Battery",
    "SignalLevel",
    "Color",
    "TimedOut",
)

def domo_create_api(self, Devices, Name, DeviceID, Unit, Type, Subtype, Switchtype, Option=None):
    
    Domoticz.Log("domo_create_api(Name: %s, DeviceID: %s, Unit: %s, Type: %s, Subtype: %s, Switchtype: %s, Option: %s)" %(
        Name, DeviceID, Unit, Type, Subtype, Switchtype, Option ))
    
    list_widget( self, Devices )
    if domoticzex:
        myDev = Domoticz.Unit( Name=Name, DeviceID=DeviceID, Unit=Unit, Type=Type, Subtype=Subtype, Switchtype=Switchtype)
        myDev.Create()
        return myDev.ID
    else:
        # Legacy
        myDev = Domoticz.Device(Name=Name, Unit=Unit, Type=Type, Subtype=Subtype, Switchtype=Switchtype )
        myDev.Create()
        Domoticz.Log("Extended Device %s Created!" %str(Devices[DeviceID].Units[Unit].ID))
        return Devices[DeviceID].Units[Unit].ID


def find_widget_unit(self, Devices, WidgetID ):
    # Should be used in domoMaj, when looking for the 'DeviceUnit'
    # In legacy 'DeviceUnit' will be a Number, while in Extended, it will be a Tupple of DeviceID and Unit
    
    for x in list(Devices):
        if domoticzex:
            for y in list(Devices[x].Units):
                if Devices[x].Units[y].ID == int(WidgetID):
                    return ( x, y )

        elif Devices[x].ID == int(WidgetID):
            return x
    return None

        
def create_widget(self, Devices , deviceid, unit):
    
    Domoticz.Log("create_widget( deviceid: %s, unit: %s)" %(deviceid, unit))

    _name = "Counter_%s" % unit
    if domoticzex:
        _name += '_Ext'
        
    myDev = domo_create_api(self, Devices, Name=_name, DeviceID=str(deviceid), Unit=unit, Type=244, Subtype=73, Switchtype=7 )
    Domoticz.Log("  - %s created! %s" %(_name, myDev))
    if domoticzex:
        unit += 1
        _name = "Counter_%s_Ext" % unit
        myDev = domo_create_api(self, Devices, Name=_name, DeviceID=str(deviceid), Unit=unit, Type=244, Subtype=73, Switchtype=7 )
        Domoticz.Log("  - %s created! %s" %(_name, myDev))
        

def list_widget( self, Devices ):

    for x in list(Devices):
        if not domoticzex:
            Domoticz.Log( "Loading Devices[%s]: %s" % (x, Devices[x].Name) )

        else:
            for y in list(Devices[x].Units):
                Domoticz.Log( "Loading Devices[%s].Units[%s]: %s" % (x, y, Devices[x].Units[y].Name) )



def get_widget_attributes(self, Devices, DeviceId, Unit, Attribute=None):
    
    Domoticz.Log("get_widget_attributes(%s %s %s" %(DeviceId, Unit, Attribute))

    return_dict = {}

    if Attribute is None:
        list_attributes = LIST_OF_WIDGET_ATTRIBUTES
    else:
        list_attributes = (Attribute,)

    for x in list_attributes:
        Domoticz.Log("-- attribute: %s" %x)
        if domoticzex:
            if x == "Battery":
                return_dict[x] = Devices[DeviceId].Units[Unit].BatteryLevel
            elif x == "Color":
                return_dict[x] = Devices[DeviceId].Units[Unit].Color
            elif x == "SignalLevel":
                return_dict[x] = Devices[DeviceId].Units[Unit].SignalLevel
            elif x == "TimedOut":
                return_dict[x] = Devices[DeviceId].TimedOut
            elif x == "nValue":
                return_dict[x] = Devices[DeviceId].Units[Unit].nValue
            elif x == "sValue":
                return_dict[x] = Devices[DeviceId].Units[Unit].sValue
        elif x == "Battery":
            return_dict[x] = Devices[Unit].BatteryLevel
        elif x == "Color":
            return_dict[x] = Devices[Unit].Color
        elif x == "SignalLevel":
            return_dict[x] = Devices[Unit].SignalLevel
        elif x == "TimedOut":
            return_dict[x] = Devices[Unit].TimedOut
        elif x == "nValue":
            return_dict[x] = Devices[Unit].nValue
        elif x == "sValue":
            return_dict[x] = Devices[Unit].sValue
    Domoticz.Log("get_widget_attributes: %s" % str(return_dict))
    return return_dict


def set_timedout_device(self, Devices, DeviceId, Unit, timedout):
    widget_attribute = get_widget_attributes(self, Devices, DeviceId, Unit)
    Domoticz.Log("set_timedout_device %s" %str(timedout))
    if not domoticzex:
        # Legacy

        Devices[Unit].Update(
            nValue=widget_attribute["nValue"],
            sValue=widget_attribute["sValue"],
            TimedOut=timedout,
        )
    else:
        # Ex
        Devices[DeviceId].TimedOut = timedout
        # Devices[DeviceId].Units[Unit].Update(Log=True)


def set_lastseen_device(self, Devices, DeviceId, Unit):

    if not domoticzex:
        # Legacy
        Devices[Unit].Touch()
    else:
        # Ex
        Devices[DeviceId].Units[Unit].Touch()


def write_attribute_device(self, Devices, DeviceId, Unit, attribute_dict):
    Domoticz.Log("write_attribute_device: %s" % str(attribute_dict))

    if "nValue" not in attribute_dict and "sValue" not in attribute_dict:
        return

    if not domoticzex:
        # Legacy
        Devices[Unit].Update(
            nValue=attribute_dict["nValue"],
            sValue=attribute_dict["sValue"],
        )
    else:
        Devices[DeviceId].Units[Unit].nValue = attribute_dict["nValue"]
        Devices[DeviceId].Units[Unit].sValue = attribute_dict["sValue"]
        if "Battery" in attribute_dict:
            Devices[DeviceId].Units[Unit].BatteryLevel = attribute_dict["Battery"]
        if "SignalLevel" in attribute_dict:
            Devices[DeviceId].Units[Unit].SignalLevel = attribute_dict["SignalLevel"]            
        Devices[DeviceId].Units[Unit].Update(Log=True)
