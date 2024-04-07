import RobotRaconteur as RR
from RobotRaconteurCompanion.Util.TestFixtures import IntraTaskFixture

from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil

from RobotRaconteurCompanion.Util.DeviceConnector import DeviceConnector, DeviceConnectorDetails

import importlib_resources
from .. import infoparser as test_infoparser_m
import yaml

import time
import pytest

import io


class _RobotStub:
    def __init__(self, robot_info):
        self.device_info = robot_info.device_info
        self.robot_info = robot_info

        self.tool_changed = RR.EventHook()
        self.payload_changed = RR.EventHook()
        self.param_changed = RR.EventHook()


class _DevConnectorTestFixture:
    def __init__(self):
        self.fixture = IntraTaskFixture()
        self.fixture.register_standard_service_types()

        self.info_loader = InfoFileLoader(self.fixture.server_node)
        self.attributes_util = AttributesUtil(self.fixture.server_node)

        robot1_info = self.load_info("robot1")
        robot2_info = self.load_info("robot2", "54738")
        robot3_info = self.load_info("robot3_another_robot", tags=[
            "my_tag1",
            {
                "name": "my_tag2",
                "uuid": "5a85724f-8533-4a7a-b955-698e1740eff9"
            },
            {
                "uuid": "a3a7fbc2-52b0-426f-8ea9-4934bd24aa8c"
            }
        ])
        robot4_info = self.load_info("robot3_another_robot", tags=[
            "my_tag4",
            {
                "name": "my_tag5",
                "uuid": "25f9682d-932e-44cd-89a5-13d724c2583a"
            },
            {
                "uuid": "385e3ec4-5faa-4c2f-b766-7a9295604a4a"
            }
        ], category="test2")

        self.register_robot_stub(robot1_info, "robot1")
        self.register_robot_stub(robot2_info, "robot2")
        self.register_robot_stub(robot3_info, "robot3")
        self.register_robot_stub(robot4_info, "robot4")

        self.client_node = self.fixture.client_node
        self.client_node.SetLogLevelFromEnvVariable()

    def load_info(self, device_ident, serial_number=None, tags=None, category="test"):
        with (importlib_resources.files(test_infoparser_m) / ('sawyer_robot_default_config.yml')).open() as info_f:
            info_dict = yaml.safe_load(info_f)
        if device_ident is not None:
            info_dict["device_info"]["device"] = device_ident
        if serial_number is not None:
            info_dict["device_info"]["serial_number"] = serial_number
        if tags is not None:
            info_dict["device_info"]["tags"] = tags
        robot_info, fd = self.info_loader.LoadInfoFileFromDict(
            info_dict, "com.robotraconteur.robotics.robot.RobotInfo", category)
        return robot_info

    def register_robot_stub(self, robot_info, service_name):
        attributes = self.attributes_util.GetDefaultServiceAttributesFromDeviceInfo(robot_info.device_info)
        robot_stub = _RobotStub(robot_info)
        ctx = self.fixture.register_service(
            service_name, "com.robotraconteur.robotics.robot.Robot", robot_stub)
        ctx.SetServiceAttributes(attributes)
        return robot_stub

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fixture.shutdown()


def test_device_connector():
    with _DevConnectorTestFixture() as test_fixture:
        con = DeviceConnector(node=test_fixture.client_node)

        d1 = DeviceConnectorDetails(device_nickname="robot1", device="robot1")

        con.AddDevice(d1)

        dev1 = con.GetDevice("robot1")
        c1 = dev1.GetDefaultClientWait(5)

        d1 = c1.device_info
        assert d1.device.name == "robot1"

        con.RemoveDevice("robot1")

        time.sleep(0.5)

        with pytest.raises(Exception):
            con.GetDevice("robot1")

        with pytest.raises(Exception):
            dev1.GetDefaultClientWait(0.1)


def test_device_connector2():
    with _DevConnectorTestFixture() as test_fixture:
        con = DeviceConnector(node=test_fixture.client_node)

        d1 = DeviceConnectorDetails(device_nickname="robot1", urls=["rr+intra:///?nodename=server_node&service=robot1"])

        con.AddDevice(d1)

        dev1 = con.GetDevice("robot1")
        c1 = dev1.GetDefaultClientWait(5)

        d1 = c1.device_info
        assert d1.device.name == "robot1"

        con.RemoveDevice("robot1")


def _assert_connected_device_count(dev, count):
    if count == 0:
        time.sleep(0.5)
        c = dev.GetConnectedClients()
        assert len(c) == 0
        return
    c1 = dev.GetDefaultClientWait(5)
    for _ in range(5):
        c = dev.GetConnectedClients()
        if len(c) == count:
            break
        time.sleep(0.5)
    assert len(c) == count


def _assert_service_name(node, dev, service_name):
    c = dev.GetDefaultClientWait(5)
    assert node.GetObjectServicePath(c) == service_name


def test_device_connector3():
    with _DevConnectorTestFixture() as test_fixture:
        con = DeviceConnector(node=test_fixture.client_node)

        d1 = DeviceConnectorDetails(device_nickname="robot1", device="robot3_another_robot")
        d2 = DeviceConnectorDetails(device_nickname="robot2", device="robot3_another_robot", tags=["my_tag1"])
        d3 = DeviceConnectorDetails(device_nickname="robot3", device="robot3_another_robot", tags=["my_tag2"])
        d4 = DeviceConnectorDetails(device_nickname="robot4", device="robot3_another_robot", tags=["my_tag10"])
        d5 = DeviceConnectorDetails(device_nickname="robot5", device="robot3_another_robot",
                                    tags=["my_tag1", "my_tag2"])
        d6 = DeviceConnectorDetails(device_nickname="robot6", device="robot3_another_robot",
                                    tags=["my_tag1", "my_tag11"])
        d7 = DeviceConnectorDetails(device_nickname="robot7", device="robot3_another_robot",
                                    tags=["my_tag5|25f9682d-932e-44cd-89a5-13d724c2583a"])
        d8 = DeviceConnectorDetails(device_nickname="robot8", device="robot3_another_robot",
                                    tags=["385e3ec4-5faa-4c2f-b766-7a9295604a4a"])

        con.AddDevice(d1)
        con.AddDevice(d2)
        con.AddDevice(d3)
        con.AddDevice(d4)
        con.AddDevice(d5)
        con.AddDevice(d6)
        con.AddDevice(d7)
        con.AddDevice(d8)

        _assert_connected_device_count(con.GetDevice("robot1"), 2)
        _assert_connected_device_count(con.GetDevice("robot2"), 1)
        _assert_connected_device_count(con.GetDevice("robot3"), 1)
        _assert_connected_device_count(con.GetDevice("robot4"), 0)
        _assert_connected_device_count(con.GetDevice("robot5"), 1)
        _assert_connected_device_count(con.GetDevice("robot6"), 0)
        _assert_connected_device_count(con.GetDevice("robot7"), 1)
        _assert_connected_device_count(con.GetDevice("robot8"), 1)

        _assert_service_name(test_fixture.client_node, con.GetDevice("robot1"), "robot3")
        _assert_service_name(test_fixture.client_node, con.GetDevice("robot2"), "robot3")
        _assert_service_name(test_fixture.client_node, con.GetDevice("robot5"), "robot3")
        _assert_service_name(test_fixture.client_node, con.GetDevice("robot7"), "robot4")
        _assert_service_name(test_fixture.client_node, con.GetDevice("robot8"), "robot4")


def test_device_connector_yaml():
    yaml = \
        """
    devices:
      robot1:
        device: robot1
      robot2:
        device:
          name: robot2
      robot3:
        urls:
        - rr+intra:///?nodename=server_node&service=robot1
      robot4:
        device: robot3_another_robot
        tags:
        - my_tag1
      robot5:
        device:
          name: robot3_another_robot
        tags:
        - my_tag2
      robot6:
        device:
          name: robot3_another_robot
        tags:
        - name: my_tag5
          uuid: 25f9682d-932e-44cd-89a5-13d724c2583a
    """
    with _DevConnectorTestFixture() as test_fixture:
        f = io.StringIO(yaml)
        con = DeviceConnector(devices_yaml_f=f, node=test_fixture.client_node)

        _assert_connected_device_count(con.GetDevice("robot1"), 1)
        _assert_connected_device_count(con.GetDevice("robot2"), 1)
        _assert_connected_device_count(con.GetDevice("robot3"), 1)
        _assert_connected_device_count(con.GetDevice("robot4"), 1)
        _assert_connected_device_count(con.GetDevice("robot5"), 1)
        _assert_connected_device_count(con.GetDevice("robot6"), 1)
