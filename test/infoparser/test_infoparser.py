import RobotRaconteur as RR
from RobotRaconteurCompanion import InfoParser
import RobotRaconteurCompanion as RRC
import importlib_resources

def test_infoparser():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        info_text = importlib_resources.read_text(__package__, 'sawyer_robot_default_config.yml')
        parser = InfoParser(node)
        robot_info = parser.ParseInfoString(info_text,"com.robotraconteur.robotics.robot.RobotInfo")
        print(robot_info)
    finally:
        node.Shutdown()
