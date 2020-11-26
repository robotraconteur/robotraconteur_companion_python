import RobotRaconteurCompanion.StdRobDef as StdRobDef
import RobotRaconteurCompanion as RRC

def test_robdef_basic_checks():
    assert len(StdRobDef.STANDARD_ROBDEF_NAMES) == 45
    for k,v in StdRobDef.STANDARD_ROBDEF_TEXT.items():
        assert isinstance(v,str)
        assert len(v) > 0

def test_register_robdefs():
    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    RRC.RegisterStdRobDefServiceTypes(RRN)
    assert len(RRN.GetRegisteredServiceTypes()) == 46