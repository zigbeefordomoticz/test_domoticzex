try:
    import DomoticzEx as Domoticz
    domoticzex = True
except:
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


def create_widget(self, Devices , deviceid, unit):

    list_widget( self, Devices )
    if not domoticzex:
        # Legacy
        Domoticz.Device(Name="Counter_%s" % unit, Unit=unit, Type=244, Subtype=73, Switchtype=7 ).Create()

    else:
        # Ex
        Domoticz.Unit(
            Name="Counter_%s" % deviceid,
            DeviceID=str(deviceid),
            Unit=unit,
            Type=244, 
            Subtype=73,
            Switchtype=7
        ).Create()
        Domoticz.Log("Created device: " + Devices[str(deviceid)].Units[unit].Name)
        Domoticz.Unit(
            Name="Counter2_%s" % deviceid,
            DeviceID=str(deviceid),
            Unit=unit+1,
            Type=241, 
            Subtype=4,
            Switchtype=7
        ).Create()
        Domoticz.Log("Created device: " + Devices[str(deviceid)].Units[unit+1].Name)




def list_widget( self, Devices ):

    if not domoticzex:
        # Legacy
        for x in list(Devices):
            Domoticz.Log(
                "Loading Devices[%s]: %s"
                % (x, Devices[x].Name)
            )
    else:
        # Ex
        for x in list(Devices):
            for y in list(Devices[x].Units):
                Domoticz.Log(
                    "Loading Devices[%s].Units[%s]: %s"
                    % (x, y, Devices[x].Units[y].Name)
                )



def get_widget_attributes(self, Devices, DeviceId, Unit, Attribute=None):

    return_dict = {}

    if Attribute is None:
        list_attributes = LIST_OF_WIDGET_ATTRIBUTES
    else:
        list_attributes = (Attribute,)

    if not domoticzex:
        # Legacy
        for x in list_attributes:
            if x == "sValue":
                return_dict[x] = Devices[Unit].sValue
            elif x == "nValue":
                return_dict[x] = Devices[Unit].nValue
            elif x == "Battery":
                return_dict[x] = Devices[Unit].BatteryLevel
            elif x == "SignalLevel":
                return_dict[x] = Devices[Unit].SignalLevel
            elif x == "Color":
                return_dict[x] = Devices[Unit].Color
            elif x == "TimedOut":
                return_dict[x] = Devices[Unit].TimedOut
    else:
        # Ex
        for x in list_attributes:
            if x == "sValue":
                return_dict[x] = Devices[DeviceId].Units[Unit].sValue
            elif x == "nValue":
                return_dict[x] = Devices[DeviceId].Units[Unit].nValue
            elif x == "Battery":
                return_dict[x] = Devices[DeviceId].Units[Unit].BatteryLevel
            elif x == "SignalLevel":
                return_dict[x] = Devices[DeviceId].Units[Unit].SignalLevel
            elif x == "Color":
                return_dict[x] = Devices[DeviceId].Units[Unit].Color
            elif x == "TimedOut":
                return_dict[x] = Devices[DeviceId].Units[Unit].TimedOut
    Domoticz.Log("get_widget_attributes: %s" % str(return_dict))
    return return_dict


def set_timedout_device(self, Devices, DeviceId, Unit, timedout):
    widget_attribute = get_widget_attributes(self, Devices, DeviceId, Unit)
    if not domoticzex:
        # Legacy

        Devices[Unit].Update(
            nValue=widget_attribute["nValue"],
            sValue=widget_attribute["sValue"],
            TimedOut=timedout,
        )
    else:
        # Ex
        Devices[DeviceId].Units[Unit].nValue = widget_attribute["nValue"]
        Devices[DeviceId].Units[Unit].sValue = widget_attribute["sValue"]
        Devices[DeviceId].Units[Unit].Update(Log=True)


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
