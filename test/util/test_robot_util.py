import RobotRaconteur as RR
from RobotRaconteurCompanion import InfoParser
import RobotRaconteurCompanion as RRC
import importlib_resources
from RobotRaconteurCompanion.Util.RobotUtil import RobotUtil
import numpy.testing as nptest
import numpy as np
import general_robotics_toolbox as rox


def test_infoparser():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        info_f = importlib_resources.files() / ".." / "infoparser" / 'sawyer_robot_default_config.yml'
        parser = InfoParser(node)
        robot_info = parser.ParseInfoFile(info_f, "com.robotraconteur.robotics.robot.RobotInfo")

        robot_util = RobotUtil(node)
        robot = robot_util.robot_info_to_rox_robot(robot_info, 0)

        nptest.assert_allclose(robot.joint_type, [0, 0, 0, 0, 0, 0, 0])
        nptest.assert_allclose(robot.joint_lower_limit,
                               [-3.0503, -3.8095, -3.0426, -3.0439, -2.9761, -2.9761, -4.7124])
        nptest.assert_allclose(robot.joint_upper_limit, [
            3.0503, 2.2736, 3.0426, 3.0439, 2.9761, 2.9761, 4.7124])
        nptest.assert_allclose(robot.joint_vel_limit, [
            1.74, 1.328, 1.957, 1.957, 3.485, 3.485, 4.545])
        nptest.assert_allclose(robot.joint_acc_limit, [
            3.5, 2.5, 5.0, 5.0, 5.0, 5.0, 5.0])
        assert robot.joint_names == [
            'right_j0', 'right_j1', 'right_j2', 'right_j3', 'right_j4', 'right_j5', 'right_j6']
        assert robot.root_link_name == "right_arm_base_link"
        assert robot.tip_link_name == "right_hand"
        assert robot.R_tool is None and robot.p_tool is None
        # nptest.assert_allclose(robot.R_tool, rox.rot(
        #     [0, 0, 1], np.deg2rad(5)), atol=1e-4)
        # nptest.assert_allclose(robot.p_tool, [0, 0, 0.1577], atol=1e-4)
        # if T_base_expected is None:
        #     assert robot.T_base is None
        # else:
        #     assert T_base_expected.isclose(robot.T_base, tol=1e-4)
        assert robot.T_base is None
        nptest.assert_allclose(rox.R2q(
            robot.T_flange.R), [-0.45451851, 0.54167662, -0.45452185, 0.54167264], atol=1e-4)
        nptest.assert_allclose(robot.T_flange.p, [0.0, 0.0, 0.0])

    finally:
        node.Shutdown()


def test_infoparser2():
    node = RR.RobotRaconteurNode()
    node.Init()
    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        info_f = importlib_resources.files() / "sawyer_robot_with_electric_gripper_config.yml"
        parser = InfoParser(node)
        robot_info = parser.ParseInfoFile(info_f, "com.robotraconteur.robotics.robot.RobotInfo")

        robot_util = RobotUtil(node)
        robot = robot_util.robot_info_to_rox_robot(robot_info, 0)

        nptest.assert_allclose(robot.joint_type, [0, 0, 0, 0, 0, 0, 0])
        nptest.assert_allclose(robot.joint_lower_limit,
                               [-3.0503, -3.8095, -3.0426, -3.0439, -2.9761, -2.9761, -4.7124])
        nptest.assert_allclose(robot.joint_upper_limit, [
            3.0503, 2.2736, 3.0426, 3.0439, 2.9761, 2.9761, 4.7124])
        nptest.assert_allclose(robot.joint_vel_limit, [
            1.74, 1.328, 1.957, 1.957, 3.485, 3.485, 4.545])
        nptest.assert_allclose(robot.joint_acc_limit, [
            3.5, 2.5, 5.0, 5.0, 5.0, 5.0, 5.0])
        assert robot.joint_names == [
            'right_j0', 'right_j1', 'right_j2', 'right_j3', 'right_j4', 'right_j5', 'right_j6']
        assert robot.root_link_name == "right_arm_base_link"
        assert robot.tip_link_name == "right_hand"
        assert robot.R_tool is None and robot.p_tool is None
        # nptest.assert_allclose(robot.R_tool, rox.rot(
        #     [0, 0, 1], np.deg2rad(5)), atol=1e-4)
        # nptest.assert_allclose(robot.p_tool, [0, 0, 0.1577], atol=1e-4)
        T_base_expected = rox.Transform(rox.rot([0, 0, 1], -np.pi / 2), [0.5, 0.23, 0.8])
        assert T_base_expected.isclose(robot.T_base, tol=1e-4)
        nptest.assert_allclose(rox.R2q(
            robot.T_flange.R), [-0.45451851, 0.54167662, -0.45452185, 0.54167264], atol=1e-4)
        nptest.assert_allclose(robot.T_flange.p, [0.00001, 0.00002, 0.00003])

    finally:
        node.Shutdown()
