import RobotRaconteur as RR
from RobotRaconteurCompanion import InfoParser
import RobotRaconteurCompanion as RRC
import importlib_resources
from RobotRaconteur.RobotRaconteurPythonUtil import PackMessageElement, UnpackMessageElement


def test_infoparser():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        info_text = (importlib_resources.files(__package__) / ('sawyer_robot_default_config.yml')).read_text()
        parser = InfoParser(node)
        robot_info = parser.ParseInfoString(info_text, "com.robotraconteur.robotics.robot.RobotInfo")
        rr_robot_info = PackMessageElement(robot_info, f"com.robotraconteur.robotics.robot.RobotInfo", node=node)
        rr_robot_info.UpdateData()
        UnpackMessageElement(rr_robot_info, node=node)
        print(robot_info)
    finally:
        node.Shutdown()
