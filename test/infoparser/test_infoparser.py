import RobotRaconteur as RR
from RobotRaconteurCompanion.InfoParser.InfoParser import InfoParser
import RobotRaconteurCompanion as RRC
import pkg_resources

resource_package = __name__

def test_infoparser():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        info_text = pkg_resources.resource_string(resource_package, 'sawyer_robot_default_config.yml').decode('utf-8')
        parser = InfoParser(node)
        robot_info = parser.ParseInfoString(info_text,"com.robotraconteur.robotics.robot.RobotInfo")
        print(robot_info)
    finally:
        node.Shutdown()
