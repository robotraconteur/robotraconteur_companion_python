import RobotRaconteur as RR
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
import RobotRaconteurCompanion as RRC
import pkg_resources
from .. import infoparser as test_infoparser

resource_package = "test.infoparser"

def test_infoparser():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        info_text = pkg_resources.resource_string(resource_package, 'sawyer_robot_default_config.yml').decode('utf-8')
        parser = InfoFileLoader(node)
        robot_info, fd = parser.LoadInfoFileFromString(info_text,"com.robotraconteur.robotics.robot.RobotInfo",category="test")
        with fd:            
            print(robot_info)
        
    finally:
        node.Shutdown()
