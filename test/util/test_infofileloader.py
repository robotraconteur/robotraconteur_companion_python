import RobotRaconteur as RR
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
import RobotRaconteurCompanion as RRC
import importlib_resources
from .. import infoparser as test_infoparser_m


def test_infoparser():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        info_text = (importlib_resources.files(test_infoparser_m) / ('sawyer_robot_default_config.yml')).read_text()
        parser = InfoFileLoader(node)
        robot_info, fd = parser.LoadInfoFileFromString(
            info_text, "com.robotraconteur.robotics.robot.RobotInfo", category="test")
        with fd:
            print(robot_info)

    finally:
        node.Shutdown()
