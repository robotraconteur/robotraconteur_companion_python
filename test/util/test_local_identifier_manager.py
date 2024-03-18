import RobotRaconteurCompanion.Util.LocalIdentifiersManager as id_manager
import RobotRaconteur as RR
import RobotRaconteurCompanion as RRC


def test_identifier_lock():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        id_manager_c = id_manager.LocalIdentifiersManager(node)
        ident, f1 = id_manager_c.GetIdentifierForNameAndLock("test", "my_robot")
        with f1:
            pass
    finally:
        node.Shutdown()
