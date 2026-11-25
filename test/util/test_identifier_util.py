from RobotRaconteurCompanion.Util.IdentifierUtil import IdentifierUtil
import RobotRaconteur as RR
import RobotRaconteurCompanion as RRC


def test_identifier_util():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        ident_util = IdentifierUtil(node)

        ident1 = ident_util.CreateIdentifier("test_device", "e6f7f559-f45a-495c-853f-26f7899693ed")
        ident2 = ident_util.CreateIdentifierFromName("test_device2")
        ident3 = ident_util.CreateIdentifierFromName("test_device")

        assert ident_util.IsIdentifierAny(ident1) == False
        assert ident_util.IsIdentifierAnyName(ident1) == False
        assert ident_util.IsIdentifierAnyUuid(ident1) == False
        assert ident_util.IsIdentifierAnyUuid(ident2) == True

        assert ident_util.IsIdentifierMatch(ident1, ident1) == True
        assert ident_util.IsIdentifierMatch(ident1, ident2) == False
        assert ident_util.IsIdentifierMatch(ident1, ident3) == True

        ident_str1 = ident_util.IdentifierToString(ident1)
        ident_str2 = ident_util.IdentifierToString(ident2)

        ident1_parsed = ident_util.StringToIdentifier(ident_str1)
        ident2_parsed = ident_util.StringToIdentifier(ident_str2)

        assert ident_util.IsIdentifierMatch(ident1, ident1_parsed) == True
        assert ident_util.IsIdentifierMatch(ident2, ident2_parsed) == True

    finally:
        node.Shutdown()


def test_string_to_identifier_invalid():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        ident_util = IdentifierUtil(node)

        ident1 = ident_util.StringToIdentifier("test_device")
        assert ident1.name == "test_device"
        assert ident_util.IsIdentifierAnyUuid(ident1)

        ident2 = ident_util.StringToIdentifier("e6f7f559-f45a-495c-853f-26f7899693ed")
        assert ident_util.IsIdentifierAnyName(ident2)
        assert not ident_util.IsIdentifierAnyUuid(ident2)

        ident3 = ident_util.StringToIdentifier("test_device|e6f7f559-f45a-495c-853f-26f7899693ed")
        assert ident3.name == "test_device"
        assert not ident_util.IsIdentifierAnyUuid(ident3)

        for s in ["test_device|", "test_device|not-a-uuid", "test_device trailing", "|e6f7f559-f45a-495c-853f-26f7899693ed",
                  "1test_device", "test_device_", ""]:
            try:
                ident_util.StringToIdentifier(s)
            except RR.InvalidArgumentException:
                pass
            else:
                assert False, "Expected InvalidArgumentException for " + repr(s)

    finally:
        node.Shutdown()
