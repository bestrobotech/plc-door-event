from opcua import Client
from opcua import ua

client = Client("opc.tcp://192.168.1.11:4840")

client.connect()  

try:
    root = client.get_root_node()
    print("Root node is: ", root)
    objects = client.get_objects_node()
    print("Objects node is: ", objects)

    # Node objects have methods to read and write node attributes as well as browse or populate address space
    print("Children of root are: ", root.get_children())

    plc_array = client.get_node("ns=4;s=PLC_ARRAY")

    dv = ua.DataValue(ua.Variant([True, False, True], ua.VariantType.Boolean))
    plc_array.set_value(dv)
finally:
    client.disconnect()
