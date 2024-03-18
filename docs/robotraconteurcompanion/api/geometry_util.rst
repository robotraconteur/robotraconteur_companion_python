RobotRaconteurCompanion.Util.GeometryUtil
=========================================

Utility class for working with Robot Raconteur geometry types. The utility functions convert
between Robot Raconteur geometry types and Python types. numpy and general_robotics_toolbox types are used
where appropriate.

A simple example:

.. code-block:: python

    from RobotRaconteur.Client import *
    from RobotRaconteur.Companion.Util import GeometryUtil

    c = RRN.ConnectService('rr+tcp://localhost:22222?service=MyRobot')
    geom_util = GeometryUtil(client_obj=c)

    # Create GeometryUtil using the connected object

    # Get a position vector
    v = c.getf_position()

    # Convert to numpy array
    v2 = vector3_to_xyz(v)

    # Convert a rpy xyz to a Robot Raconteur com.robotraconteur.geometry.Transform
    t = rpy_xyz_to_transform(np.deg2rad([10,20,30],[0.1,0.2,0.3]))

The GeometryUtil class works with `com.robotraconteur.geometry`, `com.robotraconteur.geometryf`, and
`com.robotraconteur.geometryi`. These standard service types use float64, float32, and int32 respectively.
Use the dtype argument to specify the type to use for numpy arrays. The default is float64.

GeometryUtil
------------

.. autoclass:: RobotRaconteurCompanion.Util.GeometryUtil.GeometryUtil
    :members:
