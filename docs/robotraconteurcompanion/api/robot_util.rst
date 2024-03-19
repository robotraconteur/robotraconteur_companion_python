RobotRaconteurCompanion.Util.RobotUtil
===========================================

Utility class for to convert a com.robotraconteur.robotics.robot.RobotInfo structure to a
general_robotics_toolbox.Robot object. The general_robotics_toolbox package contains functions
for working with robot kinematics.

A simple example:

.. code-block:: python

    from RobotRaconteur.Client import *
    from RobotRaconteurCompanion.Util.RobotUtil import RobotUtil
    import general_robotics_toolbox as rox

    c = RRN.ConnectService('rr+tcp://localhost:2356?service=robot')
    robot_util = RobotUtil(client_obj=c)

    # Read the robot info off the driver
    robot_info = c.robot_info

    # Convert to a general_robotics_toolbox.Robot object
    robot = robot_util.robot_info_to_rox_robot(robot_info)

    # Get the forward kinematics
    T = rox.fwdkin(robot,[0,0,0,0,0,0])


RobotUtil
--------------

.. autoclass:: RobotRaconteurCompanion.Util.RobotUtil.RobotUtil
    :members:
