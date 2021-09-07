LIST_OF_WIDGET_ATTRIBUTES = (
    "nValue",
    "sValue",
    "Battery",
    "SignalLevel",
    "Color",
    "TimedOut",
)


def get_widget_attributes(self, Devices, DeviceId, Unit, Attribute=None):
    return_dict = {}

    if Attribute:
        list_attributes = (Attribute,)
    else:
        list_attributes = LIST_OF_WIDGET_ATTRIBUTES

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

    # Ex

    return dict()


def set_timedout_device(self, Devices, DeviceId, Unit, timedout):

    # Legacy
    widget_attribute = get_widget_attributes(self, Devices, DeviceId, Unit)
    Devices[Unit].Update(
        nValue=widget_attribute["nValue"],
        sValue=widget_attribute["sValue"],
        TimedOut=timedout,
    )

    # Ex


def set_lastseen_device(self, Devices, DeviceId, Unit):

    # Legacy
    Devices[Unit].Touch()


    # Ex


def update_widget_attributes(self, Devices, DeviceId, Unit, attributes_dict):
    pass
