import RobotRaconteur as RR
import uuid
import numpy as np

from RobotRaconteurCompanion.Util.DateTimeUtil import DateTimeUtil
import RobotRaconteurCompanion as RRC


def test_now():
    node = RR.RobotRaconteurNode()
    node.SetLogLevelFromString("DEBUG")
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        date_time_util = DateTimeUtil(node=node)
        print(date_time_util.UtcNow())

        uuid_dtype = node.GetNamedArrayDType("com.robotraconteur.uuid.UUID")
        identifier_type = node.GetStructureType("com.robotraconteur.identifier.Identifier")
        device_info_type = node.GetStructureType("com.robotraconteur.device.DeviceInfo")
        uuid_info = node.ArrayToNamedArray(np.array(
            [0xa8, 0xe3, 0xc0, 0x7b, 0x12, 0xd0, 0x45, 0xd9, 0x84, 0xb0, 0x01, 0xe9, 0x75, 0xf0, 0x95, 0x7f], np.uint8), uuid_dtype)

        device_info = device_info_type()
        device_info.device = identifier_type()
        device_info.device.name = "test_device"
        device_info.device.uuid = uuid_info

        print(date_time_util.UtcNow(device_info))

        print(date_time_util.TimeSpec2Now(device_info))

        print(date_time_util.TimeSpec3Now())

        print(date_time_util.FillDeviceTime(device_info, 275837))
    finally:
        node.Shutdown()
