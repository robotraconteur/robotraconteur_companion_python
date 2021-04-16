import RobotRaconteur as RR
from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil
import RobotRaconteurCompanion as RRC
from RobotRaconteur.RobotRaconteurPythonUtil import PackMessageElement, UnpackMessageElement
import numpy as np
import os
import general_robotics_toolbox as rox

def _do_array_test(to_rr, from_rr, shape, rr_type, node, f = None):
    if f is None:
        f = lambda a: a
    arr = f(np.random.rand(*shape))
    rr_val = to_rr(arr)
    rr_msg = PackMessageElement(rr_val,f"com.robotraconteur.geometry.{rr_type}",node=node)
    rr_msg.UpdateData()
    rr_val2 = UnpackMessageElement(rr_msg,node=node)
    arr2 = from_rr(rr_val2)
    np.testing.assert_almost_equal(arr,arr2)

def test_geometry_util_array_types():
    node = RR.RobotRaconteurNode()
    node.SetLogLevelFromString("DEBUG")
    node.Init()    

    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        geom_util = GeometryUtil(node)
        _do_array_test(geom_util.xy_to_vector2, geom_util.vector2_to_xy, (2,), "Vector2", node)
        _do_array_test(geom_util.xyz_to_vector3, geom_util.vector3_to_xyz, (3,), "Vector3", node)
        _do_array_test(geom_util.abgxyz_to_vector6, geom_util.vector6_to_abgxyz, (6,), "Vector6", node)
        _do_array_test(geom_util.xy_to_point2d, geom_util.point2d_to_xy, (2,), "Point2D", node)
        _do_array_test(geom_util.xyz_to_point, geom_util.point_to_xyz, (3,), "Point", node)
        _do_array_test(geom_util.wh_to_size2d, geom_util.size2d_to_wh, (2,), "Size2D", node)
        _do_array_test(geom_util.whd_to_size, geom_util.size_to_whd, (3,), "Size", node)
        _do_array_test(geom_util.q_to_quaternion, geom_util.quaternion_to_q, (3,), "Quaternion", node, lambda a: rox.R2q(rox.rpy2R(a)))
        _do_array_test(geom_util.R_to_quaternion, geom_util.quaternion_to_R, (3,), "Quaternion", node, lambda a: rox.rpy2R(a))
        _do_array_test(geom_util.rpy_to_quaternion, geom_util.quaternion_to_rpy, (3,), "Quaternion", node)
        _do_array_test(geom_util.array_to_spatial_velocity, geom_util.spatial_velocity_to_array, (6,), "SpatialVelocity", node)
        _do_array_test(geom_util.array_to_spatial_acceleration, geom_util.spatial_acceleration_to_array, (6,), "SpatialAcceleration", node)
        _do_array_test(geom_util.array_to_wrench, geom_util.wrench_to_array, (6,), "Wrench", node)

    finally:
        node.Shutdown()

def _do_transform_test(to_rr, from_rr, rr_type, node):
    rox_transform = rox.Transform(rox.rpy2R(np.random.rand(3)),np.random.rand(3))
    rr_val = to_rr(rox_transform)
    rr_msg = PackMessageElement(rr_val,f"com.robotraconteur.geometry.{rr_type}",node=node)
    rr_msg.UpdateData()
    rr_val2 = UnpackMessageElement(rr_msg,node=node)
    rox_transform2 = from_rr(rr_val2)

    np.testing.assert_almost_equal(rox_transform.R,rox_transform2.R)
    np.testing.assert_almost_equal(rox_transform.p,rox_transform2.p)

def _do_named_transform_test(to_rr, from_rr, rr_type, node):
    rox_transform = rox.Transform(rox.rpy2R(np.random.rand(3)),np.random.rand(3),"parent_frame", "child_frame")
    rr_val = to_rr(rox_transform)
    rr_msg = PackMessageElement(rr_val,f"com.robotraconteur.geometry.{rr_type}",node=node)
    rr_msg.UpdateData()
    rr_val2 = UnpackMessageElement(rr_msg,node=node)
    rox_transform2 = from_rr(rr_val2)

    np.testing.assert_almost_equal(rox_transform.R,rox_transform2.R)
    np.testing.assert_almost_equal(rox_transform.p,rox_transform2.p)
    assert rox_transform.parent_frame_id == rox_transform2.parent_frame_id
    assert rox_transform.child_frame_id == rox_transform2.child_frame_id

def test_geometry_util_transform_types():
    node = RR.RobotRaconteurNode()
    node.SetLogLevelFromString("DEBUG")
    node.Init()    

    try:
        RRC.RegisterStdRobDefServiceTypes(node)
        geom_util = GeometryUtil(node)
        
        _do_transform_test(geom_util.rox_transform_to_transform, geom_util.transform_to_rox_transform, "Transform", node)
        _do_transform_test(geom_util.rox_transform_to_pose, geom_util.pose_to_rox_transform, "Pose", node)
        _do_named_transform_test(geom_util.rox_transform_to_named_transform, geom_util.named_transform_to_rox_transform, "NamedTransform", node)
        _do_named_transform_test(geom_util.rox_transform_to_named_pose, geom_util.named_pose_to_rox_transform, "NamedPose", node)
        
    finally:
        node.Shutdown()