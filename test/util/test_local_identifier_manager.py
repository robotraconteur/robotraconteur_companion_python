import RobotRaconteurCompanion.Util.LocalIdentifiersManager as id_manager
import RobotRaconteur as RR
import RobotRaconteurCompanion as RRC

def test_get_paths():
    path = id_manager._get_user_identifier_path()
    path2 = id_manager._get_user_run_path()
    path3 = id_manager._get_user_identifier_path()

    print(path)
    print(path2)
    print(path3)

def test_identifier_lock():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        id_manager_c = id_manager.LocalIdentifiersManager(node) 
        ident, f1 = id_manager_c.GetIdentifierForNameAndLock("test","my_robot")
    finally:
        node.Shutdown()
    
    