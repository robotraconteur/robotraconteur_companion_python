from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
import RobotRaconteur as RR
import RobotRaconteurCompanion as RRC
import numpy as np

def test_attributes_util():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        attributes_util = AttributesUtil(node)

        uuid_dtype = node.GetNamedArrayDType("com.robotraconteur.uuid.UUID")
        identifier_type = node.GetStructureType("com.robotraconteur.identifier.Identifier")
        device_info_type = node.GetStructureType("com.robotraconteur.device.DeviceInfo")
        uuid_info = node.ArrayToNamedArray(np.array([0xa8, 0xe3, 0xc0, 0x7b, 0x12, 0xd0, 0x45, 0xd9, 0x84, 0xb0, 0x01,0xe9, 0x75, 0xf0, 0x95, 0x7f],np.uint8),uuid_dtype)

        device_info = device_info_type()
        device_info.device = identifier_type()
        device_info.device.name = "test_device"
        device_info.device.uuid = uuid_info

        device_info.serial_number = "123432"

        attr_dict = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(device_info)
        
        print(attr_dict)

    finally:
        node.Shutdown()
    