RobotRaconteurCompanion.Util.UuidUtil
===========================================

Utility class for working with Robot Raconteur UUIDs.

UUIDs are statistically guaranteed to be unique. The use of UUIDs eliminates the need for a central
registry for object identifiers, and allows for easy discovery of devices and services on a network.
The name is used to identify services and devices when guaranteed unique identification is not required.

.. code-block:: python

    .. code-block:: python

    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    import RobotRaconteurCompanion as RRC
    from RobotRaconeteurCompanion.Util.UuidUtil import UuidUtil

    RRC.RegisterStdRobDefServiceTypes(RRN)

    # Create an UuidUtil
    uuid_util = UuidUtil(RRN)

    # Create a UUID
    my_uuid = uuid_util.NewRandomUuid()

    # Create a UUID from a string
    my_uuid = uuid_util.UuidFromUuidString("12345678-1234-1234-1234-123456789012")

    # Convert UUID to Python UUID
    my_uuid = uuid_util.UuidToPyUuid(my_uuid)

    # Convert UUID to string
    my_uuid_str = uuid_util.UuidToString(my_uuid)

UuidUtil
--------------

.. autoclass:: RobotRaconteurCompanion.Util.UuidUtil.UuidUtil
    :members:
