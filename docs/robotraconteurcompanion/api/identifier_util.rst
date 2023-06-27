RobotRaconteurCompanion.Util.IdentifierUtil
===========================================

Utility class for working with Robot Raconteur identifiers. Identifiers in Robot Raconteur consist
of a UUID and a name. The UUID is a 16 byte array, and the name is a string. The UUID is used to
uniquely identify the object, and the name is used to identify the object to humans. The name is
not guaranteed to be unique, and should not be used to identify the object in a production environment.

UUIDs are statistically guaranteed to be unique. The use of UUIDs eliminates the need for a central
registry for object identifiers, and allows for easy discovery of devices and services on a network.
The name is used to identify services and devices when guaranteed unique identification is not required.

.. code-block:: python

    .. code-block:: python

    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    import RobotRaconteurCompanion as RRC
    from RobotRaconeteurCompanion.Util.IdentifierUtil import IdentifierUtil

    RRC.RegisterStdRobDefServiceTypes(RRN)

    # Create an IdentifierUtil
    id_util = IdentifierUtil(RRN)

    # Create an identifier from a name
    my_device_identifier = id_util.CreateIdentifierFromName("my_device")

    # Convert the identifier to a string
    my_device_identifier_str = id_util.IdentifierToString(my_device_identifier)

    # Convert the identifier string back to an identifier
    my_device_identifier2 = id_util.StringToIdentifier(my_device_identifier_str)

    # Compare identifiers
    assert id_util.IsIdentifierMatch(my_device_identifier, my_device_identifier2)




IdentifierUtil
--------------

.. autoclass:: RobotRaconteurCompanion.Util.IdentifierUtil.IdentifierUtil
    :members:
    
