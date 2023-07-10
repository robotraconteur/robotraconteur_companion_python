import RobotRaconteur as RR
from RobotRaconteurCompanion.Util import RobDef

def test_robdef_util():
    node = RR.RobotRaconteurNode()
    RobDef.register_service_type_from_resource(node, __package__, "experimental.robdef_test")

    node2 = RR.RobotRaconteurNode()
    RobDef.register_service_types_from_resources(node2, __package__, ["experimental.robdef_test"])